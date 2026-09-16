"""
CASE 04: SAME IMAGE TO BOTH EYES
BASE: main_vr_scene_7.py

목적:
    머리를 움직일 때 공간이 기울거나 Z-depth가 휘어 보이는 현상이
    좌/우 눈 이미지 차이(eye transform, IPD, stereo mismatch)에서 오는지 확인한다.

이번 케이스에서 바꾼 것:
    - 실제로는 stereo side-by-side 렌더를 그대로 수행
    - OpenVR Submit 단계에서 왼쪽 눈 이미지를 양쪽 눈에 동일하게 제출
    - 즉, 양안 disparity만 제거하고 나머지 파이프라인은 baseline 유지

그대로 유지한 것:
    - robosuite Lift 환경 / XArm7
    - BASIC controller / env.step()
    - 오른손 teleoperation / gripper
    - 왼손 작업공간 이동
    - HMD pose 처리 방식
    - projection frustum
    - MuJoCo stereo side-by-side 렌더
    - OpenGL FBO/blit
    - OpenVR IVRCompositor::Submit
    - 렌더/입력/physics 루프 구조와 주기

판정:
    baseline에서는 공간이 휘는데 이 케이스에서는 크게 안정된다면,
    문제의 핵심 후보는 eye-to-head transform / IPD / stereo disparity 쪽이다.
    반대로 동일한 왜곡이 그대로 남으면 원인은 stereo mismatch보다
    head pose / projection / reprojection 쪽일 가능성이 높다.

주의:
    이 케이스에서는 양쪽 눈에 같은 영상이 들어가므로 입체감은 의도적으로 사라진다.
    "입체감이 없음"은 실패가 아니다. 월드의 기울기/휨이 줄었는지만 비교한다.

요구:
    pip install PyOpenGL glfw
    SteamVR + ALVR 연결 상태에서 실행 (WayVR은 끌 것)

조작:
    [머리]            시야 (트래킹)
    [오른손] 그립 홀드 : 로봇 추종 ON (클러치)
    [오른손] 트리거    : 그리퍼 닫기
    [왼손]  스틱      : 작업 공간 안에서 이동 (전후/좌우)
    [왼손]  트리거    : 위로,  그립 : 아래로
    [왼손]  X 버튼    : 시점 위치 초기화
    Ctrl+C           : 종료
"""

import argparse
import ctypes
import time

import glfw
import numpy as np
from OpenGL import GL
from scipy.spatial.transform import Rotation as R

import mujoco
import openvr
import robosuite as suite
from robosuite.controllers import load_composite_controller_config

try:
    import robosuite_models  # noqa: F401
except ImportError:
    pass


# --------------------------------------------------------------------------
# 좌표계: OpenVR(+X 오른쪽, +Y 위, -Z 전방) -> robosuite(+X 전방, +Y 왼쪽, +Z 위)
# --------------------------------------------------------------------------
VR2ROBOT = np.array([
    [0.0, 0.0, -1.0],
    [-1.0, 0.0, 0.0],
    [0.0, 1.0, 0.0],
])

POS_OUTPUT_MAX = 0.05
ROT_OUTPUT_MAX = 0.5
POS_SCALE = 1.5
ROT_SCALE = 1.0
POS_DEADZONE = 5e-4
ROT_DEADZONE = 2e-3

STICK_DEADZONE = 0.15
MOVE_SPEED = 1.2          # m/s, 작업 공간 이동
LIFT_SPEED = 0.8          # m/s, 상하

NEAR, FAR = 0.05, 50.0

# 기본 시점: 로봇 원점에서 -X쪽으로 물러나 테이블을 바라봄
DEFAULT_ORIGIN = np.array([-1.5, 0.0, 0.0])


# --------------------------------------------------------------------------
def mat34_to_numpy(m):
    """openvr.HmdMatrix34_t -> 4x4 numpy"""
    out = np.eye(4)
    for i in range(3):
        for j in range(4):
            out[i][j] = m[i][j]
    return out


def drain_gl_errors():
    """SteamVR submit이 남기는 에러를 비운다. 안 비우면 PyOpenGL이 예외를 던진다."""
    n = 0
    while GL.glGetError() != GL.GL_NO_ERROR and n < 32:
        n += 1
    return n


DEBUG = False
_seen_tags = set()


def dbg_gl(tag):
    """디버그 모드에서 대기 중인 GL 에러를 최초 1회 보고하고 비운다."""
    e = GL.glGetError()
    if e != GL.GL_NO_ERROR:
        if DEBUG and tag not in _seen_tags:
            _seen_tags.add(tag)
            print(f">>> GL 에러 0x{e:x} at {tag}")
        drain_gl_errors()


# --------------------------------------------------------------------------
# VR 입력
# --------------------------------------------------------------------------
class QuestVRDevice:
    def __init__(self, vr_system):
        self.vr = vr_system
        self.right_idx = None
        self.left_idx = None
        self.engaged = False
        self.ref_pos = None
        self.ref_rot = None
        self._grip_mask = 1 << openvr.k_EButton_Grip
        self._a_mask = 1 << openvr.k_EButton_A
        self._prev_a = False

    def find(self, role):
        for i in range(openvr.k_unMaxTrackedDeviceCount):
            if self.vr.getTrackedDeviceClass(i) != openvr.TrackedDeviceClass_Controller:
                continue
            if self.vr.getControllerRoleForTrackedDeviceIndex(i) != role:
                continue
            if role == openvr.TrackedControllerRole_RightHand:
                if self.right_idx != i:
                    print(f"[VR] 오른손 컨트롤러 (index={i})")
                self.right_idx = i
            else:
                if self.left_idx != i:
                    print(f"[VR] 왼손 컨트롤러 (index={i})")
                self.left_idx = i
            return i
        return None

    def wait_for_controllers(self, timeout=30.0):
        t0 = time.time()
        warned = False
        while time.time() - t0 < timeout:
            self.find(openvr.TrackedControllerRole_RightHand)
            self.find(openvr.TrackedControllerRole_LeftHand)
            if self.right_idx is not None:
                return True
            if not warned:
                print("[VR] 컨트롤러 대기 중... ALVR Connected 및 착용 여부 확인.")
                warned = True
            time.sleep(0.5)
        print("[VR] 컨트롤러 미발견. 진행하지만 조작은 불가.")
        return False

    # -- 오른손: 로봇 -------------------------------------------------------
    def get_action(self, poses):
        if self.right_idx is None:
            self.find(openvr.TrackedControllerRole_RightHand)
            if self.right_idx is None:
                self.engaged = False
                return np.zeros(3), np.zeros(3), -1.0, False

        pose = poses[self.right_idx]
        if not pose.bPoseIsValid:
            self.engaged = False
            return np.zeros(3), np.zeros(3), -1.0, False

        m = pose.mDeviceToAbsoluteTracking
        pos_vr = np.array([m[0][3], m[1][3], m[2][3]])
        rot_vr = np.array([[m[r][c] for c in range(3)] for r in range(3)])

        ok, state = self.vr.getControllerState(self.right_idx)
        if not ok:
            self.engaged = False
            return np.zeros(3), np.zeros(3), -1.0, False

        pos = VR2ROBOT @ pos_vr
        rot = VR2ROBOT @ rot_vr @ VR2ROBOT.T

        gripper = 1.0 if float(state.rAxis[1].x) > 0.5 else -1.0
        grip = bool(state.ulButtonPressed & self._grip_mask)

        if not grip:
            self.engaged = False
            return np.zeros(3), np.zeros(3), gripper, False

        if not self.engaged:
            self.engaged = True
            self.ref_pos, self.ref_rot = pos, rot
            return np.zeros(3), np.zeros(3), gripper, True

        d_pos = (pos - self.ref_pos) * POS_SCALE
        d_rot = R.from_matrix(rot @ self.ref_rot.T).as_rotvec() * ROT_SCALE
        self.ref_pos, self.ref_rot = pos, rot

        if np.linalg.norm(d_pos) < POS_DEADZONE:
            d_pos[:] = 0.0
        if np.linalg.norm(d_rot) < ROT_DEADZONE:
            d_rot[:] = 0.0
        return d_pos, d_rot, gripper, True

    # -- 왼손: 이동 ---------------------------------------------------------
    def get_move_input(self):
        """returns (stick_x, stick_y, up, down, reset_pressed)"""
        if self.left_idx is None:
            self.find(openvr.TrackedControllerRole_LeftHand)
            if self.left_idx is None:
                return 0.0, 0.0, 0.0, 0.0, False

        ok, state = self.vr.getControllerState(self.left_idx)
        if not ok:
            return 0.0, 0.0, 0.0, 0.0, False

        sx, sy = float(state.rAxis[0].x), float(state.rAxis[0].y)
        if abs(sx) < STICK_DEADZONE:
            sx = 0.0
        if abs(sy) < STICK_DEADZONE:
            sy = 0.0

        a_now = bool(state.ulButtonPressed & self._a_mask)
        reset = a_now and not self._prev_a
        self._prev_a = a_now

        return sx, sy, float(state.rAxis[1].x), float(state.rAxis[2].x), reset


# --------------------------------------------------------------------------
# 스테레오 렌더 타깃 (MuJoCo offscreen -> 자체 텍스처 -> Submit)
# --------------------------------------------------------------------------
class StereoTarget:
    def __init__(self, eye_w, eye_h):
        self.eye_w, self.eye_h = eye_w, eye_h
        self.w, self.h = eye_w * 2, eye_h

        self.tex = GL.glGenTextures(1)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.tex)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_CLAMP_TO_EDGE)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_CLAMP_TO_EDGE)
        GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGBA8, self.w, self.h, 0,
                        GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, None)
        GL.glBindTexture(GL.GL_TEXTURE_2D, 0)

        self.fbo = GL.glGenFramebuffers(1)
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, self.fbo)
        GL.glFramebufferTexture2D(GL.GL_FRAMEBUFFER, GL.GL_COLOR_ATTACHMENT0,
                                  GL.GL_TEXTURE_2D, self.tex, 0)
        status = GL.glCheckFramebufferStatus(GL.GL_FRAMEBUFFER)
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, 0)
        if status != GL.GL_FRAMEBUFFER_COMPLETE:
            raise RuntimeError(f"FBO 미완성: 0x{status:x}")

        self.texture = openvr.Texture_t()
        self.texture.handle = ctypes.c_void_p(int(self.tex))
        self.texture.eType = openvr.TextureType_OpenGL
        self.texture.eColorSpace = openvr.ColorSpace_Auto

        # 좌우 절반. 상하가 뒤집혀 보이면 vMin/vMax를 서로 바꿀 것.
        self.bounds_l = openvr.VRTextureBounds_t(0.0, 0.0, 0.5, 1.0)
        self.bounds_r = openvr.VRTextureBounds_t(0.5, 0.0, 1.0, 1.0)

    def blit_from_mujoco(self, con):
        """MuJoCo 오프스크린 렌더버퍼 -> 자체 텍스처 (GPU 내부 복사)"""
        dbg_gl("blit 진입 전")
        src = con.offFBO
        if getattr(con, "offSamples", 0) > 0:
            # 멀티샘플이면 MuJoCo의 resolve 버퍼를 한 번 거친다
            GL.glBindFramebuffer(GL.GL_READ_FRAMEBUFFER, con.offFBO)
            GL.glBindFramebuffer(GL.GL_DRAW_FRAMEBUFFER, con.offFBO_r)
            GL.glBlitFramebuffer(0, 0, self.w, self.h, 0, 0, self.w, self.h,
                                 GL.GL_COLOR_BUFFER_BIT, GL.GL_NEAREST)
            dbg_gl("MSAA resolve blit")
            src = con.offFBO_r

        GL.glBindFramebuffer(GL.GL_READ_FRAMEBUFFER, src)
        GL.glBindFramebuffer(GL.GL_DRAW_FRAMEBUFFER, self.fbo)
        GL.glBlitFramebuffer(0, 0, self.w, self.h, 0, 0, self.w, self.h,
                             GL.GL_COLOR_BUFFER_BIT, GL.GL_NEAREST)
        dbg_gl("최종 blit")
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, 0)

    def dump(self, path):
        """현재 텍스처 내용을 파일로 저장. 검은 화면 원인 격리용."""
        import cv2
        GL.glBindFramebuffer(GL.GL_READ_FRAMEBUFFER, self.fbo)
        raw = GL.glReadPixels(0, 0, self.w, self.h, GL.GL_RGBA,
                              GL.GL_UNSIGNED_BYTE)
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, 0)
        img = np.frombuffer(raw, dtype=np.uint8).reshape(self.h, self.w, 4)
        img = img[::-1]                       # GL은 아래->위
        nonzero = int((img[:, :, :3] > 8).sum())
        cv2.imwrite(path, img[:, :, [2, 1, 0]])
        print(f">>> blit 후 덤프: {path}  (밝은 픽셀 {nonzero})")

    def submit(self, comp, same_both=False):
        if same_both:
            # 두 눈에 왼눈 이미지를 그대로. 양안 불일치가 원인인지 가른다.
            comp.submit(openvr.Eye_Left, self.texture, self.bounds_l)
            comp.submit(openvr.Eye_Right, self.texture, self.bounds_l)
        else:
            comp.submit(openvr.Eye_Left, self.texture, self.bounds_l)
            comp.submit(openvr.Eye_Right, self.texture, self.bounds_r)
        drain_gl_errors()   # SteamVR이 남기는 GL_INVALID_VALUE 비우기


def dump_mujoco_direct(path, viewport, con):
    """MuJoCo 오프스크린을 mjr_readPixels로 직접 읽는다. blit을 건너뛴다."""
    import cv2
    rgb = np.empty((viewport.height, viewport.width, 3), dtype=np.uint8)
    mujoco.mjr_readPixels(rgb, None, viewport, con)
    rgb = rgb[::-1]
    nonzero = int((rgb > 8).sum())
    cv2.imwrite(path, rgb[:, :, ::-1])
    print(f">>> MuJoCo 직접 덤프: {path}  (밝은 픽셀 {nonzero})")


# --------------------------------------------------------------------------
# OpenVR 눈 파라미터 -> mjvGLCamera
# --------------------------------------------------------------------------
class EyeRig:
    def __init__(self, vr_system, roll_test=0.0, lock_translation=True):
        self.vr = vr_system
        self.roll_test = roll_test
        self.lock_translation = lock_translation
        self._head_pos_ref = None
        self.eye_to_head = [
            mat34_to_numpy(vr_system.getEyeToHeadTransform(openvr.Eye_Left)),
            mat34_to_numpy(vr_system.getEyeToHeadTransform(openvr.Eye_Right)),
        ]
        self.frustum = []
        for eye in (openvr.Eye_Left, openvr.Eye_Right):
            l, r, t, b = vr_system.getProjectionRaw(eye)
            # 런타임마다 top/bottom 부호 규약이 달라서 크기로 정렬한다
            left, right = min(l, r), max(l, r)
            bottom, top = min(t, b), max(t, b)
            self.frustum.append((left, right, bottom, top))
        for i in range(2):
            l, r, b, t = self.frustum[i]
            e = self.eye_to_head[i]
            # 회전 성분이 항등에서 얼마나 벗어나는지 (칸팅)
            cant = np.degrees(np.arccos(
                np.clip((np.trace(e[:3, :3]) - 1) / 2, -1, 1)))
            print(f"[VR] eye{i} frustum L={l:+.4f} R={r:+.4f} "
                  f"B={b:+.4f} T={t:+.4f}  offset={e[0,3]*1000:+.1f}mm "
                  f"cant={cant:.2f}deg")
        print(f"[VR] eye-to-head 간격: "
              f"{abs(self.eye_to_head[0][0,3] - self.eye_to_head[1][0,3])*1000:.1f} mm")

    def check_aspect(self, eye_w, eye_h):
        """렌더 종횡비가 눈 frustum 종횡비와 맞는지 확인.
        어긋나면 고개를 돌릴 때 월드가 헤엄치듯 일그러진다."""
        for i, (left, right, bottom, top) in enumerate(self.frustum):
            fa = (right - left) / (top - bottom)
            ra = eye_w / eye_h
            mark = "OK" if abs(fa - ra) / fa < 0.02 else "불일치!"
            print(f"[VR] eye{i} frustum 종횡비 {fa:.4f} / 렌더 {ra:.4f}  {mark}")

    def apply(self, scn, hmd_pose_vr, origin):
        """HMD 회전을 안정적으로 적용한다.

        기본 모드에서는 첫 유효 HMD 위치를 고정하고 회전만 실시간 반영한다.
        이 방식은 초기 눈높이는 그대로 보존하면서 positional jitter가 Z-depth로
        전달되는 것을 막는다. --full-6dof 사용 시 실제 위치 이동도 반영한다.
        """
        hmd = np.array(hmd_pose_vr, dtype=float, copy=True)

        # 추적 행렬의 회전부를 수치적으로 직교화한다.
        # 아주 작은 scale/shear 성분이 카메라 up/forward에 누적되는 것을 방지한다.
        rot = hmd[:3, :3]
        u, _, vt = np.linalg.svd(rot)
        rot = u @ vt
        if np.linalg.det(rot) < 0:
            u[:, -1] *= -1
            rot = u @ vt
        hmd[:3, :3] = rot

        if self._head_pos_ref is None:
            self._head_pos_ref = hmd[:3, 3].copy()
            mode = "회전 추적 + 시작 위치 고정" if self.lock_translation else "full 6DoF"
            print(f"[VR] HMD 기준 위치 저장: {self._head_pos_ref} / {mode}")

        if self.lock_translation:
            # 위치를 0으로 만들지 않는다. 시작할 때의 실제 높이/위치를 그대로 고정한다.
            hmd[:3, 3] = self._head_pos_ref

        mid = np.zeros(3)
        fwd_mid = np.zeros(3)

        for i in range(2):
            eye_world_vr = hmd @ self.eye_to_head[i]
            pos = VR2ROBOT @ eye_world_vr[:3, 3] + origin

            axes = VR2ROBOT @ eye_world_vr[:3, :3]
            forward = -axes[:, 2]
            up = axes[:, 1]

            # 완전한 정규직교 camera frame으로 만든다.
            forward = forward / max(np.linalg.norm(forward), 1e-12)
            up = up - forward * np.dot(up, forward)
            up = up / max(np.linalg.norm(up), 1e-12)

            if self.roll_test:
                up = R.from_rotvec(
                    forward * np.radians(self.roll_test)).apply(up)
                up = up - forward * np.dot(up, forward)
                up = up / max(np.linalg.norm(up), 1e-12)

            cam = scn.camera[i]
            cam.pos[:] = pos.astype(np.float32)
            cam.forward[:] = forward.astype(np.float32)
            cam.up[:] = up.astype(np.float32)

            left, right, bottom, top = self.frustum[i]
            cam.frustum_near = NEAR
            cam.frustum_far = FAR
            cam.frustum_bottom = bottom * NEAR
            cam.frustum_top = top * NEAR
            cam.frustum_center = 0.5 * (left + right) * NEAR
            try:
                cam.frustum_width = (right - left) * NEAR
            except AttributeError:
                pass

            mid += pos * 0.5
            fwd_mid += forward * 0.5

        try:
            if scn.nlight > 0:
                scn.lights[0].pos[:] = mid.astype(np.float32)
                scn.lights[0].dir[:] = fwd_mid.astype(np.float32)
        except Exception:
            pass

        return mid, fwd_mid

    @staticmethod
    def roll_of(forward, up):
        """월드 +Z를 기준으로 한 카메라 롤(도). 고개를 기울이면 변해야 한다."""
        z = np.array([0.0, 0.0, 1.0])
        up0 = z - forward * np.dot(forward, z)      # 롤 없는 up
        n = np.linalg.norm(up0)
        if n < 1e-6:                                 # 똑바로 위/아래를 볼 때
            return float("nan")
        up0 /= n
        s = np.dot(np.cross(up0, up), forward)
        c = np.dot(up0, up)
        return np.degrees(np.arctan2(s, c))


# --------------------------------------------------------------------------
def raw_model_data(env):
    model = getattr(env.sim.model, "_model", env.sim.model)
    data = getattr(env.sim.data, "_data", env.sim.data)
    return model, data


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--eye-scale", type=float, default=0.45,
                   help="헤드셋 권장 해상도 대비 배율. 종횡비는 자동으로 맞춰짐")
    p.add_argument("--eye-width", type=int, default=0,
                   help="직접 지정 (0이면 --eye-scale 사용). 종횡비 주의")
    p.add_argument("--eye-height", type=int, default=0)
    p.add_argument("--robot", default="XArm7")
    p.add_argument("--no-msaa", action="store_true",
                   help="멀티샘플 끄기 (blit 문제 시)")
    p.add_argument("--debug", action="store_true",
                   help="GL 에러 위치 보고 + 30프레임째 덤프")
    p.add_argument("--same-both-eyes", action="store_true",
                   help="두 눈에 같은 이미지를 보낸다. 입체는 사라지지만 "
                        "양안 불일치가 왜곡의 원인인지 가른다")
    p.add_argument("--print-pose", action="store_true",
                   help="머리 요/피치/롤을 주기적으로 출력")
    p.add_argument("--roll-test", type=float, default=0.0,
                   help="카메라에 고정 롤(도)을 강제로 넣는다. 30 정도로 주고 "
                        "화면이 기우는지 본다. 안 기울면 MuJoCo가 롤을 버리는 것")
    p.add_argument("--gpu-sync", action="store_true",
                   help="렌더 후 glFinish로 GPU 완료를 기다려 실제 GPU 시간을 측정")
    p.add_argument("--no-vr-cam", action="store_true",
                   help="머리 트래킹 카메라 덮어쓰기를 건너뛰고 기본 궤도 카메라로 렌더 "
                        "(검은 화면 원인 격리용)")
    p.add_argument("--full-6dof", action="store_true",
                   help="HMD 위치 이동까지 카메라에 반영. 기본은 시작 위치를 고정하고 회전만 추적")
    p.add_argument("--use-frustum-aspect", action="store_true",
                   help="SteamVR native render-target 비율 대신 projection frustum 비율 사용")
    return p.parse_args()


def main():
    global DEBUG
    args = parse_args()
    DEBUG = args.debug

    # CASE 04 핵심 변경:
    # 렌더는 baseline과 동일하게 좌/우안을 만들되,
    # Submit 단계에서는 왼쪽 눈 영상을 양쪽 눈에 동일하게 보낸다.
    args.same_both_eyes = True

    # --- OpenVR (Scene 앱) ---------------------------------------------
    openvr.init(openvr.VRApplication_Scene)
    vr_system = openvr.VRSystem()
    comp = openvr.VRCompositor()

    device = QuestVRDevice(vr_system)
    eyes = EyeRig(vr_system, roll_test=args.roll_test, lock_translation=not args.full_6dof)

    # 화면이 세로로 길고 좁아지는 문제를 피하기 위해 기본은 SteamVR가 권장한
    # render-target의 가로/세로 비율을 그대로 유지한다.
    rec_w, rec_h = vr_system.getRecommendedRenderTargetSize()
    if args.eye_width > 0 and args.eye_height > 0:
        EW, EH = args.eye_width, args.eye_height
    else:
        EH = max(256, int(rec_h * args.eye_scale) // 8 * 8)
        if args.use_frustum_aspect:
            l, r, b, t = eyes.frustum[0]
            aspect = (r - l) / (t - b)
            EW = max(256, int(round(EH * aspect)) // 8 * 8)
            aspect_mode = "projection frustum"
        else:
            EW = max(256, int(rec_w * args.eye_scale) // 8 * 8)
            aspect_mode = "SteamVR native"
    print(f"[VR] 권장 눈당 {rec_w}x{rec_h} -> 렌더 {EW}x{EH} "
          f"(종횡비 {EW/EH:.4f}, {locals().get('aspect_mode', 'manual')})")
    eyes.check_aspect(EW, EH)

    # 여기서 컨트롤러를 기다리지 않는다. 이 대기가 robosuite/GL 초기화를 최대 30초
    # 막을 수 있었다. get_action/get_move_input이 실행 중 자동으로 컨트롤러를 찾는다.
    print("=" * 68)
    print("CASE 04: SAME IMAGE TO BOTH EYES")
    print("baseline 유지 + Submit에서 왼쪽 눈 이미지를 양쪽 눈에 동일 제출")
    print("※ 입체감이 사라지는 것은 정상. 공간 휨/기울기만 비교하세요.")
    print("=" * 68)
    print("[VR] robosuite를 즉시 시작합니다. 컨트롤러는 실행 중 자동 감지됩니다.")

    # --- GL 컨텍스트 ----------------------------------------------------
    if not glfw.init():
        raise RuntimeError("glfw init 실패")
    glfw.window_hint(glfw.VISIBLE, False)
    window = glfw.create_window(100, 100, "vr", None, None)
    glfw.make_context_current(window)
    print("GL:", GL.glGetString(GL.GL_RENDERER).decode())

    # --- robosuite ------------------------------------------------------
    env = suite.make(
        env_name="Lift",
        robots=args.robot,
        controller_configs=load_composite_controller_config(controller="BASIC"),
        has_renderer=False,
        has_offscreen_renderer=False,
        use_camera_obs=False,
        control_freq=20,
        horizon=10000,
    )
    env.reset()
    low, high = env.action_spec
    control_dt = 1.0 / env.control_freq

    model, data = raw_model_data(env)
    model.vis.global_.offwidth = EW * 2
    model.vis.global_.offheight = EH
    if args.no_msaa:
        model.vis.quality.offsamples = 0

    con = mujoco.MjrContext(model, mujoco.mjtFontScale.mjFONTSCALE_150)
    mujoco.mjr_setBuffer(mujoco.mjtFramebuffer.mjFB_OFFSCREEN, con)

    # 요청한 크기가 실제로 반영됐는지 확인. 여기가 어긋나면 blit이 엉뚱한 걸 읽는다.
    off_w = getattr(con, "offWidth", -1)
    off_h = getattr(con, "offHeight", -1)
    off_s = getattr(con, "offSamples", -1)
    print(f"[MJ] 요청 {EW*2}x{EH} / 실제 오프스크린 {off_w}x{off_h} "
          f"samples={off_s}")
    if (off_w, off_h) != (EW * 2, EH):
        print(">>> 오프스크린 크기가 요청과 다릅니다. 이게 검은 화면의 원인입니다.")

    scn = mujoco.MjvScene(model, maxgeom=20000)
    scn.stereo = mujoco.mjtStereo.mjSTEREO_SIDEBYSIDE

    # Lift의 바닥 반사 때문에 cube가 바닥에도 하나 더 있는 것처럼 보일 수 있다.
    # reflection만 끄며 실제 물리/큐브/테이블에는 영향이 없다.
    try:
        scn.flags[mujoco.mjtRndFlag.mjRND_REFLECTION] = 0
        print("[MJ] floor reflection OFF")
    except Exception as e:
        print(f"[MJ] reflection flag 건너뜀: {e}")

    opt = mujoco.MjvOption()
    base_cam = mujoco.MjvCamera()
    base_cam.type = mujoco.mjtCamera.mjCAMERA_FREE
    base_cam.lookat[:] = [0.0, 0.0, 0.9]
    base_cam.distance = 2.0

    target = StereoTarget(EW, EH)
    viewport = mujoco.MjrRect(0, 0, EW * 2, EH)

    poses_t = openvr.TrackedDevicePose_t * openvr.k_unMaxTrackedDeviceCount
    poses = poses_t()

    origin = DEFAULT_ORIGIN.copy()
    accum = 0.0
    d_pos_acc = np.zeros(3)
    d_rot_acc = np.zeros(3)
    gripper = -1.0
    engaged = False
    prev_engaged = False
    prev_t = time.time()
    n_frames = 0
    t_start = time.time()
    prof = {k: 0.0 for k in
            ("wait", "scene", "render", "blit", "submit", "input", "physics")}

    drain_gl_errors()
    print("시작. 오른손 그립을 잡고 있는 동안 로봇이 따라옵니다.")

    try:
        while True:
            _t = time.time()
            comp.waitGetPoses(poses, None)      # 72Hz 동기화
            drain_gl_errors()
            prof["wait"] += time.time() - _t

            now = time.time()
            frame_dt = now - prev_t
            prev_t = now

            hmd_pose = poses[openvr.k_unTrackedDeviceIndex_Hmd]

            # --- 렌더 & 제출을 먼저 -------------------------------------
            # 포즈 획득과 제출 사이에 물리 연산을 끼우면 그만큼 낡은 포즈가
            # 나가서 리프로젝션 워프(시야 휨)가 심해진다. 최대한 빨리 낸다.
            _t = time.time()
            mujoco.mjv_updateScene(model, data, opt, None, base_cam,
                                   mujoco.mjtCatBit.mjCAT_ALL, scn)
            if hmd_pose.bPoseIsValid and not args.no_vr_cam:
                eyes.apply(scn, mat34_to_numpy(hmd_pose.mDeviceToAbsoluteTracking),
                           origin)

            # blit이 매 프레임 끝에 GL_FRAMEBUFFER를 0으로 되돌리므로,
            # 렌더 직전에 오프스크린을 다시 잡아준다. 이걸 빼면 2프레임째부터
            # 숨겨진 100x100 glfw 창에 그리게 된다.
            mujoco.mjr_setBuffer(mujoco.mjtFramebuffer.mjFB_OFFSCREEN, con)
            prof["scene"] += time.time() - _t

            if args.print_pose and n_frames % 20 == 0:
                c = scn.camera[0]
                f = np.array(c.forward, dtype=float)
                u = np.array(c.up, dtype=float)
                yaw = np.degrees(np.arctan2(f[1], f[0]))
                pitch = np.degrees(np.arcsin(np.clip(f[2], -1, 1)))
                roll = EyeRig.roll_of(f, u)
                print(f"[pose] valid={int(hmd_pose.bPoseIsValid)} "
                      f"yaw={yaw:7.1f}  pitch={pitch:6.1f}  roll={roll:7.1f}")

            _t = time.time()
            mujoco.mjr_render(viewport, scn, con)
            if args.gpu_sync:
                # mjr_render는 GL 명령을 큐에 넣고 바로 반환한다. glFinish로
                # GPU 완료를 기다려야 실제 렌더 비용이 render 항목에 잡힌다.
                # (평소엔 끄는 게 빠르다. 측정용 옵션.)
                GL.glFinish()
            dbg_gl("mjr_render 직후")
            prof["render"] += time.time() - _t

            if DEBUG and n_frames == 30:
                c = scn.camera[0]
                print(f">>> scn.stereo={scn.stereo} ngeom={scn.ngeom} "
                      f"nlight={scn.nlight} currentBuffer="
                      f"{getattr(con, 'currentBuffer', '?')} (1=offscreen) "
                      f"cam0.pos={np.array(c.pos)}")
                print(f">>> fwd={np.array(c.forward)} up={np.array(c.up)}")
                print(f">>> frustum n={c.frustum_near} f={c.frustum_far} "
                      f"b={c.frustum_bottom:.4f} t={c.frustum_top:.4f} "
                      f"c={c.frustum_center:.4f} "
                      f"w={getattr(c, 'frustum_width', 'N/A')}")
            if DEBUG and n_frames in (0, 30):
                tag = "f0" if n_frames == 0 else "f30"
                dump_mujoco_direct(f"/tmp/mj_{tag}.png", viewport, con)

            # 각 눈 절반에 상태 표시
            label = "FOLLOW" if engaged else "PAUSED"
            grip_txt = "GRIP CLOSE" if gripper > 0 else "GRIP OPEN"
            for half in range(2):
                vp = mujoco.MjrRect(half * EW, 0, EW, EH)
                mujoco.mjr_overlay(mujoco.mjtFont.mjFONT_NORMAL,
                                   mujoco.mjtGridPos.mjGRID_TOPLEFT,
                                   vp, label, grip_txt, con)

            _t = time.time()
            target.blit_from_mujoco(con)
            if DEBUG and n_frames == 30:
                target.dump("/tmp/vr_frame.png")
            prof["blit"] += time.time() - _t

            _t = time.time()
            target.submit(comp, same_both=args.same_both_eyes)
            prof["submit"] += time.time() - _t

            # --- 제출 이후에 입력 + 물리 ---------------------------------
            _t = time.time()
            d_pos, d_rot, gripper, engaged = device.get_action(poses)
            d_pos_acc += d_pos
            d_rot_acc += d_rot
            if engaged != prev_engaged:
                print("[VR] 추종 " + ("ON" if engaged else "OFF"))
                prev_engaged = engaged

            sx, sy, up, down, reset = device.get_move_input()
            if reset:
                origin = DEFAULT_ORIGIN.copy()
                print("[VR] 시점 초기화")

            if hmd_pose.bPoseIsValid and (sx or sy or up or down):
                hm = mat34_to_numpy(hmd_pose.mDeviceToAbsoluteTracking)
                axes = VR2ROBOT @ hm[:3, :3]     # 카메라와 같은 규칙
                fwd = -axes[:, 2]
                fwd[2] = 0.0
                right = axes[:, 0].copy()
                right[2] = 0.0
                n1, n2 = np.linalg.norm(fwd), np.linalg.norm(right)
                if n1 > 1e-6 and n2 > 1e-6:
                    origin += (fwd / n1 * sy + right / n2 * sx) * MOVE_SPEED * frame_dt
                origin[2] += (up - down) * LIFT_SPEED * frame_dt

            # 물리 20Hz. 따라잡기는 2스텝까지만 (끊길 때 폭주 방지).
            prof["input"] += time.time() - _t
            _t = time.time()
            accum += frame_dt
            steps = 0
            while accum >= control_dt and steps < 2:
                action = np.zeros(env.action_dim)
                action[:3] = d_pos_acc / POS_OUTPUT_MAX
                action[3:6] = d_rot_acc / ROT_OUTPUT_MAX
                action[-1] = gripper
                _, _, done, _ = env.step(np.clip(action, low, high))
                d_pos_acc[:] = 0.0
                d_rot_acc[:] = 0.0
                accum -= control_dt
                steps += 1
                if done:
                    env.reset()
                    device.engaged = False
            if accum > control_dt * 3:
                accum = control_dt      # 너무 밀리면 버린다
            prof["physics"] += time.time() - _t

            n_frames += 1
            if n_frames % 180 == 0:
                elapsed = time.time() - t_start
                fps = 180.0 / elapsed
                parts = "  ".join(f"{k}={v/180*1000:.1f}" for k, v in prof.items())
                busy = sum(v for k, v in prof.items() if k != "wait") / 180 * 1000
                print(f"[VR] {fps:.1f} fps  (프레임당 ms) {parts}")
                print(f"     wait 제외 합계 {busy:.1f} ms / 예산 13.9 ms   "
                      f"origin=({origin[0]:.2f}, {origin[1]:.2f}, {origin[2]:.2f})")
                for k in prof:
                    prof[k] = 0.0
                t_start = time.time()

    except KeyboardInterrupt:
        print("\n종료합니다.")
    finally:
        for name, fn in (("glfw", glfw.terminate),
                         ("openvr", openvr.shutdown),
                         ("env", env.close)):
            try:
                fn()
            except Exception as e:
                print(f"[cleanup] {name}: {e}")


if __name__ == "__main__":
    main()
