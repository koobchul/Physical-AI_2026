"""
Oculus Quest 2 (SteamVR/OpenVR) -> robosuite teleoperation + VR 오버레이 출력
모노 / 스테레오(사이드바이사이드) 전환 지원.

조작:
    [오른손] 그립 홀드 : 로봇 추종 ON (클러치)
    [오른손] 트리거    : 그리퍼 닫기
    [왼손]  스틱 좌우  : 카메라 좌우 궤도 회전
    [왼손]  스틱 상하  : 카메라 상하 궤도 회전
    [왼손]  트리거     : 줌 인
    [왼손]  그립       : 줌 아웃
    [왼손]  X 버튼     : 입체 시야 ON/OFF 토글
    Ctrl+C            : 종료

실행:
    python main_vr.py              # 입체(기본)
    python main_vr.py --mono       # 평면
    python main_vr.py --ipd-gain 1.5

주의:
    - SteamVR 대시보드(메뉴 버튼)를 열면 컨트롤러 입력을 뺏긴다. 닫아둘 것.
    - GL 컨텍스트 오류 시 MUJOCO_GL=egl 또는 MUJOCO_GL=glfw 로 실행.
"""

import argparse
import ctypes
import faulthandler
import time

faulthandler.enable()   # 세그폴트 시 파이썬 스택을 찍는다

import numpy as np
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
# 좌표계 / 스케일
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

# 오버레이 패널 (한쪽 눈 기준 해상도)
PANEL_W, PANEL_H = 960, 720
PANEL_WIDTH_M = 2.2
PANEL_DISTANCE = 2.0
PANEL_HEIGHT = 1.4

# 카메라 조작
STICK_DEADZONE = 0.15
AZIMUTH_SPEED = 90.0
ELEVATION_SPEED = 60.0
ZOOM_SPEED = 1.2

DEFAULT_IPD = 0.064          # HMD에서 못 읽을 때 폴백
IPD_MIN, IPD_MAX = 0.0, 0.30 # 안전 범위

# SDK 버전에 따라 상수명이 없을 수 있어 폴백값을 둔다 (openvr.h: 14, 15)
SBS_PARALLEL = getattr(openvr, "VROverlayFlags_SideBySide_Parallel", 14)


def _mat34(rot, pos):
    m = openvr.HmdMatrix34_t()
    for i in range(3):
        for j in range(3):
            m[i][j] = float(rot[i][j])
        m[i][3] = float(pos[i])
    return m


# --------------------------------------------------------------------------
# VR 입력
# --------------------------------------------------------------------------
class QuestVRDevice:
    def __init__(self, pos_scale=POS_SCALE, rot_scale=ROT_SCALE):
        openvr.init(openvr.VRApplication_Overlay)
        self.vr = openvr.VRSystem()

        self.pos_scale = pos_scale
        self.rot_scale = rot_scale

        self.right_idx = None
        self.left_idx = None
        self.engaged = False
        self.ref_pos = None
        self.ref_rot = None

        self._grip_mask = 1 << openvr.k_EButton_Grip
        self._a_mask = 1 << openvr.k_EButton_A   # Touch 왼손 = X 버튼
        self._prev_a = False

        self._find(openvr.TrackedControllerRole_RightHand)
        self._find(openvr.TrackedControllerRole_LeftHand)
        if self.right_idx is None:
            print("[VR] 오른쪽 컨트롤러 미인식. 전원 확인. (연결 시 자동 재인식)")

    # -- 내부 --------------------------------------------------------------
    def _find(self, role):
        for i in range(openvr.k_unMaxTrackedDeviceCount):
            if self.vr.getTrackedDeviceClass(i) != openvr.TrackedDeviceClass_Controller:
                continue
            if self.vr.getControllerRoleForTrackedDeviceIndex(i) == role:
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

    def _poses(self):
        return self.vr.getDeviceToAbsoluteTrackingPose(
            openvr.TrackingUniverseStanding, 0.0,
            openvr.k_unMaxTrackedDeviceCount)

    def get_hmd_ipd(self):
        try:
            ipd = float(self.vr.getFloatTrackedDeviceProperty(
                openvr.k_unTrackedDeviceIndex_Hmd,
                openvr.Prop_UserIpdMeters_Float))
            if 0.04 < ipd < 0.09:
                return ipd
        except Exception:
            pass
        return DEFAULT_IPD

    # -- 오른손: 로봇 조작 --------------------------------------------------
    def get_action(self):
        """returns (d_pos[m], d_rot[axis-angle], gripper[-1|1], engaged)"""
        if self.right_idx is None:
            self._find(openvr.TrackedControllerRole_RightHand)
            if self.right_idx is None:
                self.engaged = False
                return np.zeros(3), np.zeros(3), -1.0, False

        pose = self._poses()[self.right_idx]
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

        d_pos = (pos - self.ref_pos) * self.pos_scale
        d_rot = R.from_matrix(rot @ self.ref_rot.T).as_rotvec() * self.rot_scale
        self.ref_pos, self.ref_rot = pos, rot

        if np.linalg.norm(d_pos) < POS_DEADZONE:
            d_pos[:] = 0.0
        if np.linalg.norm(d_rot) < ROT_DEADZONE:
            d_rot[:] = 0.0
        return d_pos, d_rot, gripper, True

    # -- 왼손: 카메라 조작 --------------------------------------------------
    def get_view_input(self):
        """returns (stick_x, stick_y, zoom_in, zoom_out, toggle_pressed)"""
        if self.left_idx is None:
            self._find(openvr.TrackedControllerRole_LeftHand)
            if self.left_idx is None:
                return 0.0, 0.0, 0.0, 0.0, False

        ok, state = self.vr.getControllerState(self.left_idx)
        if not ok:
            return 0.0, 0.0, 0.0, 0.0, False

        # Oculus Touch(SteamVR 레거시): axis0=스틱, axis1=트리거, axis2=그립
        sx, sy = float(state.rAxis[0].x), float(state.rAxis[0].y)
        if abs(sx) < STICK_DEADZONE:
            sx = 0.0
        if abs(sy) < STICK_DEADZONE:
            sy = 0.0

        a_now = bool(state.ulButtonPressed & self._a_mask)
        toggle = a_now and not self._prev_a      # 눌린 순간에만 1회
        self._prev_a = a_now

        return sx, sy, float(state.rAxis[1].x), float(state.rAxis[2].x), toggle

    def wait_for_controllers(self, timeout=30.0):
        """컨트롤러가 잡힐 때까지 대기. 잡히면 True."""
        t0 = time.time()
        warned = False
        while time.time() - t0 < timeout:
            self._find(openvr.TrackedControllerRole_RightHand)
            self._find(openvr.TrackedControllerRole_LeftHand)
            if self.right_idx is not None:
                return True
            if not warned:
                print("[VR] 컨트롤러 대기 중... "
                      "ALVR이 Connected 상태인지, 헤드셋을 착용했는지 확인하세요.")
                warned = True
            time.sleep(0.5)
        print(f"[VR] {timeout:.0f}초 동안 컨트롤러를 찾지 못했습니다. "
              "일단 진행하지만 조작은 되지 않습니다.")
        return False

    def close(self):
        openvr.shutdown()


# --------------------------------------------------------------------------
# VR 오버레이 화면 (모노 / 스테레오 SBS)
# --------------------------------------------------------------------------
class VROverlayScreen:
    def __init__(self, stereo=True, key="robosuite.view", name="robosuite"):
        self.ov = openvr.VROverlay()
        self.handle = self.ov.createOverlay(key, name)
        self.ov.setOverlayWidthInMeters(self.handle, PANEL_WIDTH_M)
        self.ov.setOverlayTransformAbsolute(
            self.handle,
            openvr.TrackingUniverseStanding,
            _mat34(np.eye(3), [0.0, PANEL_HEIGHT, -PANEL_DISTANCE]),
        )
        self.ov.showOverlay(self.handle)

        self.stereo = None
        self._buf = None
        self._fail_count = 0
        self.set_stereo(stereo)

    def set_stereo(self, stereo):
        """모노/스테레오 전환. 버퍼와 오버레이 플래그를 함께 갱신."""
        if stereo == self.stereo:
            return
        self.stereo = bool(stereo)

        try:
            self.ov.setOverlayFlag(self.handle, SBS_PARALLEL, self.stereo)
        except Exception as e:
            print(f"[VR] SBS 플래그 설정 실패({e}). 모노로 동작합니다.")
            self.stereo = False

        w = PANEL_W * 2 if self.stereo else PANEL_W
        # 컴포지터가 버퍼를 비동기로 읽으므로 두 개를 번갈아 쓴다.
        # 하나만 쓰면 업로드 중에 덮어써져 화면이 찢어지고 RequestFailed가 난다.
        self._bufs = [np.empty((PANEL_H, w, 4), dtype=np.uint8) for _ in range(2)]
        for b in self._bufs:
            b[..., 3] = 255
        self._buf_idx = 0
        print("[VR] 입체 시야 " + ("ON" if self.stereo else "OFF"))

    def update(self, eye_images):
        """eye_images: 모노면 [rgb], 스테레오면 [left_rgb, right_rgb]"""
        buf = self._bufs[self._buf_idx]
        self._buf_idx ^= 1

        # mujoco.Renderer는 위->아래. 상하 반전되어 보이면 img[::-1] 사용.
        if self.stereo:
            buf[:, :PANEL_W, :3] = eye_images[0]
            buf[:, PANEL_W:, :3] = eye_images[1]
        else:
            buf[..., :3] = eye_images[0]

        try:
            self.ov.setOverlayRaw(
                self.handle,
                buf.ctypes.data_as(ctypes.c_void_p),
                buf.shape[1], buf.shape[0], 4,
            )
        except openvr.error_code.OverlayError as e:
            self._fail_count += 1
            if self._fail_count == 1 or self._fail_count % 200 == 0:
                print(f"[VR] 오버레이 갱신 실패 x{self._fail_count}: {type(e).__name__}")
            return
        if self._fail_count:
            print("[VR] 오버레이 갱신 복구됨")
            self._fail_count = 0

    def close(self):
        try:
            self.ov.destroyOverlay(self.handle)
        except Exception:
            pass


# --------------------------------------------------------------------------
# 궤도 카메라 (+ 스테레오 눈 분리)
# --------------------------------------------------------------------------
class OrbitCamera:
    def __init__(self, lookat=(0.0, 0.0, 0.9)):
        self.lookat = np.array(lookat, dtype=float)
        self.distance = 1.8
        self.azimuth = 135.0
        self.elevation = -25.0
        self._cams = [self._new_cam(), self._new_cam()]

    @staticmethod
    def _new_cam():
        c = mujoco.MjvCamera()
        c.type = mujoco.mjtCamera.mjCAMERA_FREE
        return c

    def update(self, sx, sy, zoom_in, zoom_out, dt):
        self.azimuth += sx * AZIMUTH_SPEED * dt
        self.elevation = float(np.clip(
            self.elevation + sy * ELEVATION_SPEED * dt, -89.0, 89.0))
        zoom = (zoom_out - zoom_in) * ZOOM_SPEED * dt
        self.distance = float(np.clip(self.distance * (1.0 + zoom), 0.4, 6.0))

    def _fill(self, cam, lookat):
        cam.lookat[:] = lookat
        cam.distance = self.distance
        cam.azimuth = self.azimuth
        cam.elevation = self.elevation
        return cam

    def eye_cameras(self, stereo, separation):
        """스테레오면 [왼눈, 오른눈], 아니면 [중앙] 반환."""
        if not stereo:
            return [self._fill(self._cams[0], self.lookat)]

        # MuJoCo 자유 카메라: forward = (cos el cos az, cos el sin az, sin el)
        # right = normalize(forward x world_up) = (sin az, -cos az, 0)
        az = np.radians(self.azimuth)
        right = np.array([np.sin(az), -np.cos(az), 0.0])
        half = right * (separation * 0.5)
        # 눈이 뒤바뀐 느낌이면 half의 부호를 반대로.
        return [
            self._fill(self._cams[0], self.lookat - half),   # 왼눈
            self._fill(self._cams[1], self.lookat + half),   # 오른눈
        ]


def _raw_model_data(env):
    model = getattr(env.sim.model, "_model", env.sim.model)
    data = getattr(env.sim.data, "_data", env.sim.data)
    return model, data


# --------------------------------------------------------------------------
def parse_args():
    p = argparse.ArgumentParser()
    g = p.add_mutually_exclusive_group()
    g.add_argument("--stereo", dest="stereo", action="store_true",
                   help="입체 시야 (기본)")
    g.add_argument("--mono", dest="stereo", action="store_false",
                   help="평면 패널")
    p.set_defaults(stereo=True)
    p.add_argument("--ipd-gain", type=float, default=1.0,
                   help="입체감 배율. 1.0=실제 IPD. 크게 하면 깊이감이 과장됨")
    p.add_argument("--robot", default="XArm7")
    return p.parse_args()


def main():
    args = parse_args()

    controller_config = load_composite_controller_config(controller="BASIC")
    env = suite.make(
        env_name="Lift",
        robots=args.robot,
        controller_configs=controller_config,
        has_renderer=False,
        has_offscreen_renderer=False,
        use_camera_obs=False,
        control_freq=20,
        horizon=10000,
    )
    env.reset()

    low, high = env.action_spec
    dt = 1.0 / env.control_freq

    model, data = _raw_model_data(env)

    # MuJoCo 기본 오프스크린 버퍼는 640x480. 패널 해상도에 맞춰 키운다.
    # (이걸 안 하면 Renderer 생성이 실패하고, __del__에서 _gl_context
    #  AttributeError가 나면서 진짜 원인이 가려진다.)
    model.vis.global_.offwidth = PANEL_W
    model.vis.global_.offheight = PANEL_H

    renderer = mujoco.Renderer(model, height=PANEL_H, width=PANEL_W)
    camera = OrbitCamera()

    vr = QuestVRDevice()
    vr.wait_for_controllers()
    separation = float(np.clip(vr.get_hmd_ipd() * args.ipd_gain, IPD_MIN, IPD_MAX))
    print(f"[VR] 눈 간격 {separation*1000:.1f} mm")

    screen = VROverlayScreen(stereo=args.stereo)
    stereo = screen.stereo
    print("헤드셋 앞 패널에 시뮬레이션이 뜹니다. "
          "오른손 그립을 잡고 있는 동안만 로봇이 따라옵니다.")

    prev_engaged = False
    try:
        while True:
            t0 = time.time()

            # --- 오른손: 로봇 ---
            d_pos, d_rot, gripper, engaged = vr.get_action()
            if engaged != prev_engaged:
                print("[VR] 추종 " + ("ON" if engaged else "OFF"))
                prev_engaged = engaged

            action = np.zeros(env.action_dim)
            action[:3] = d_pos / POS_OUTPUT_MAX
            action[3:6] = d_rot / ROT_OUTPUT_MAX
            action[-1] = gripper
            action = np.clip(action, low, high)

            _, _, done, _ = env.step(action)

            # --- 왼손: 시점 ---
            sx, sy, zin, zout, toggle = vr.get_view_input()
            camera.update(sx, sy, zin, zout, dt)
            if toggle:
                stereo = not stereo
                screen.set_stereo(stereo)
                stereo = screen.stereo   # 플래그 실패 시 되돌려진 값 반영

            # --- 렌더 -> 오버레이 ---
            images = []
            for cam in camera.eye_cameras(stereo, separation):
                renderer.update_scene(data, camera=cam)
                images.append(renderer.render())
            screen.update(images)

            if done:
                env.reset()
                vr.engaged = False

            remain = dt - (time.time() - t0)
            if remain > 0:
                time.sleep(remain)

    except KeyboardInterrupt:
        print("\n종료합니다.")
    finally:
        # 뒤처리에서 난 예외가 원래 예외를 가리지 않게 한다
        for cleanup in (screen.close, vr.close, renderer.close, env.close):
            try:
                cleanup()
            except Exception as e:
                print(f"[cleanup] {cleanup.__qualname__}: {e}")


if __name__ == "__main__":
    main()
