"""
Oculus Quest 2 -> robosuite teleoperation (wlx-overlay-s 버전)

OpenVR은 컨트롤러 입력만 읽는다. 화면은 평범한 데스크톱 창으로 띄우고,
wlx-overlay-s가 그 창을 VR 안에 미러링한다.
SetOverlayRaw 경로를 쓰지 않으므로 컴포지터를 건드리지 않는다.

사전 준비:
    1. SteamVR + ALVR로 헤드셋 연결 (Devices 탭이 Connected)
    2. wlx-overlay-s AppImage 실행
       - 화면 공유 팝업이 뜨면 요청 순서대로 화면 선택
       - 왼손 B/Y 더블탭으로 표시/숨김
    3. python main_wlx.py

조작:
    [오른손] 그립 홀드 : 로봇 추종 ON (클러치)
    [오른손] 트리거    : 그리퍼 닫기
    [왼손]  스틱 좌우  : 카메라 좌우 궤도 회전
    [왼손]  스틱 상하  : 카메라 상하 궤도 회전
    [왼손]  트리거     : 줌 인
    [왼손]  그립       : 줌 아웃
    창에서 q          : 종료 (또는 Ctrl+C)
    창에서 r          : 환경 리셋
"""

import argparse
import time

import cv2
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
AZIMUTH_SPEED = 90.0
ELEVATION_SPEED = 60.0
ZOOM_SPEED = 1.2

WINDOW = "robosuite teleop"


# --------------------------------------------------------------------------
# VR 입력 (오버레이 없음, 입력 전용)
# --------------------------------------------------------------------------
class QuestVRDevice:
    def __init__(self, pos_scale=POS_SCALE, rot_scale=ROT_SCALE):
        # 오버레이를 만들지 않으므로 Background로 충분하다.
        openvr.init(openvr.VRApplication_Background)
        self.vr = openvr.VRSystem()

        self.pos_scale = pos_scale
        self.rot_scale = rot_scale

        self.right_idx = None
        self.left_idx = None
        self.engaged = False
        self.ref_pos = None
        self.ref_rot = None

        self._grip_mask = 1 << openvr.k_EButton_Grip

    def _find(self, role):
        for i in range(openvr.k_unMaxTrackedDeviceCount):
            if self.vr.getTrackedDeviceClass(i) != openvr.TrackedDeviceClass_Controller:
                continue
            # 핸드 트래킹 유사 장치(role=0)는 건너뛴다
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
            self._find(openvr.TrackedControllerRole_RightHand)
            self._find(openvr.TrackedControllerRole_LeftHand)
            if self.right_idx is not None:
                return True
            if not warned:
                print("[VR] 컨트롤러 대기 중... ALVR Connected 상태와 착용 여부 확인.")
                warned = True
            time.sleep(0.5)
        print(f"[VR] {timeout:.0f}초간 컨트롤러 미발견. 진행하지만 조작은 불가.")
        return False

    def _poses(self):
        return self.vr.getDeviceToAbsoluteTrackingPose(
            openvr.TrackingUniverseStanding, 0.0,
            openvr.k_unMaxTrackedDeviceCount)

    # -- 오른손: 로봇 -------------------------------------------------------
    def get_action(self):
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

    # -- 왼손: 카메라 -------------------------------------------------------
    def get_view_input(self):
        if self.left_idx is None:
            self._find(openvr.TrackedControllerRole_LeftHand)
            if self.left_idx is None:
                return 0.0, 0.0, 0.0, 0.0

        ok, state = self.vr.getControllerState(self.left_idx)
        if not ok:
            return 0.0, 0.0, 0.0, 0.0

        sx, sy = float(state.rAxis[0].x), float(state.rAxis[0].y)
        if abs(sx) < STICK_DEADZONE:
            sx = 0.0
        if abs(sy) < STICK_DEADZONE:
            sy = 0.0
        return sx, sy, float(state.rAxis[1].x), float(state.rAxis[2].x)

    def close(self):
        openvr.shutdown()


# --------------------------------------------------------------------------
class OrbitCamera:
    def __init__(self, lookat=(0.0, 0.0, 0.9)):
        self.cam = mujoco.MjvCamera()
        self.cam.type = mujoco.mjtCamera.mjCAMERA_FREE
        self.cam.lookat[:] = lookat
        self.cam.distance = 1.8
        self.cam.azimuth = 135.0
        self.cam.elevation = -25.0

    def update(self, sx, sy, zoom_in, zoom_out, dt):
        self.cam.azimuth += sx * AZIMUTH_SPEED * dt
        self.cam.elevation = float(np.clip(
            self.cam.elevation + sy * ELEVATION_SPEED * dt, -89.0, 89.0))
        zoom = (zoom_out - zoom_in) * ZOOM_SPEED * dt
        self.cam.distance = float(np.clip(
            self.cam.distance * (1.0 + zoom), 0.4, 6.0))


def _raw_model_data(env):
    model = getattr(env.sim.model, "_model", env.sim.model)
    data = getattr(env.sim.data, "_data", env.sim.data)
    return model, data


def draw_hud(bgr, engaged, gripper, fps):
    """조작 상태를 화면에 표시. VR 안에서 클러치 상태를 알아야 한다."""
    color = (80, 220, 80) if engaged else (80, 80, 220)
    label = "FOLLOW" if engaged else "PAUSED"
    cv2.rectangle(bgr, (0, 0), (bgr.shape[1], 44), (30, 30, 30), -1)
    cv2.putText(bgr, label, (16, 32), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
    grip_txt = "GRIP: CLOSE" if gripper > 0 else "GRIP: OPEN"
    cv2.putText(bgr, grip_txt, (170, 32), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                (220, 220, 220), 2)
    cv2.putText(bgr, f"{fps:4.1f} fps", (bgr.shape[1] - 130, 32),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (180, 180, 180), 2)
    return bgr


# --------------------------------------------------------------------------
def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--width", type=int, default=1280)
    p.add_argument("--height", type=int, default=960)
    p.add_argument("--robot", default="XArm7")
    p.add_argument("--fullscreen", action="store_true")
    return p.parse_args()


def main():
    args = parse_args()

    controller_config = load_composite_controller_config(controller="BASIC")
    env = suite.make(
        env_name="Lift",
        robots=args.robot,
        controller_configs=controller_config,
        has_renderer=False,            # robosuite 뷰어 대신 직접 창을 띄운다
        has_offscreen_renderer=False,
        use_camera_obs=False,
        control_freq=20,
        horizon=10000,
    )
    env.reset()

    low, high = env.action_spec
    dt = 1.0 / env.control_freq

    model, data = _raw_model_data(env)
    model.vis.global_.offwidth = args.width
    model.vis.global_.offheight = args.height
    renderer = mujoco.Renderer(model, height=args.height, width=args.width)
    camera = OrbitCamera()

    cv2.namedWindow(WINDOW, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(WINDOW, args.width, args.height)
    if args.fullscreen:
        cv2.setWindowProperty(WINDOW, cv2.WND_PROP_FULLSCREEN,
                              cv2.WINDOW_FULLSCREEN)

    vr = QuestVRDevice()
    vr.wait_for_controllers()
    print("시작합니다. wlx-overlay-s에서 이 창이 보이는지 확인하세요.")

    prev_engaged = False
    fps = 0.0
    try:
        while True:
            t0 = time.time()

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

            sx, sy, zin, zout = vr.get_view_input()
            camera.update(sx, sy, zin, zout, dt)

            renderer.update_scene(data, camera=camera.cam)
            rgb = renderer.render()
            bgr = np.ascontiguousarray(rgb[:, :, ::-1])
            draw_hud(bgr, engaged, gripper, fps)
            cv2.imshow(WINDOW, bgr)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
            if key == ord("r") or done:
                env.reset()
                vr.engaged = False

            elapsed = time.time() - t0
            fps = 1.0 / max(elapsed, 1e-6)
            remain = dt - elapsed
            if remain > 0:
                time.sleep(remain)

    except KeyboardInterrupt:
        print("\n종료합니다.")
    finally:
        for cleanup in (cv2.destroyAllWindows, vr.close, renderer.close, env.close):
            try:
                cleanup()
            except Exception as e:
                print(f"[cleanup] {cleanup.__qualname__}: {e}")


if __name__ == "__main__":
    main()
