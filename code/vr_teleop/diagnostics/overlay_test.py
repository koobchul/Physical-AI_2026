"""
OpenVR 오버레이 최소 테스트.
MuJoCo 없이 OpenVR만 사용. 헤드셋 정면 1m에 색 패널을 고정한다.

실행: python overlay_test.py
기대: 헤드셋 정면에 빨강 -> 초록 -> 파랑으로 바뀌는 사각형이 15초간 보임.
"""

import ctypes
import time

import numpy as np
import openvr

W = H = 256

openvr.init(openvr.VRApplication_Overlay)
vr = openvr.VRSystem()

# --- 1. SteamVR이 어떤 장치를 보고 있는지 --------------------------------
print("--- tracked devices ---")
CLASS_NAME = {
    openvr.TrackedDeviceClass_HMD: "HMD",
    openvr.TrackedDeviceClass_Controller: "Controller",
    openvr.TrackedDeviceClass_GenericTracker: "Tracker",
    openvr.TrackedDeviceClass_TrackingReference: "BaseStation",
}
found_controller = False
for i in range(openvr.k_unMaxTrackedDeviceCount):
    c = vr.getTrackedDeviceClass(i)
    if c == openvr.TrackedDeviceClass_Invalid:
        continue
    try:
        model = vr.getStringTrackedDeviceProperty(i, openvr.Prop_ModelNumber_String)
    except Exception:
        model = "?"
    role = ""
    if c == openvr.TrackedDeviceClass_Controller:
        found_controller = True
        role = f" role={vr.getControllerRoleForTrackedDeviceIndex(i)}"
    print(f"idx={i:2d} {CLASS_NAME.get(c, c):12s} model={model}{role}")

if not found_controller:
    print(">>> 컨트롤러가 하나도 없습니다. 헤드셋이 연결/착용 상태가 아닙니다.")
print()

# --- 2. 오버레이 생성 ----------------------------------------------------
ov = openvr.VROverlay()
handle = ov.createOverlay("test.overlay.viz", "overlay test")
print(f"overlay handle = {handle}")

ov.setOverlayWidthInMeters(handle, 0.6)
ov.setOverlayAlpha(handle, 1.0)

# 헤드셋 기준 정면 1m. HMD 공간에서 전방은 -Z.
m = openvr.HmdMatrix34_t()
for r in range(3):
    for c in range(4):
        m[r][c] = 0.0
m[0][0] = m[1][1] = m[2][2] = 1.0
m[2][3] = -1.0
ov.setOverlayTransformTrackedDeviceRelative(
    handle, openvr.k_unTrackedDeviceIndex_Hmd, m)

ov.showOverlay(handle)
print(f"isOverlayVisible = {ov.isOverlayVisible(handle)}")

# --- 3. 텍스처를 계속 밀어넣으며 색 변경 --------------------------------
# 컴포지터가 버퍼를 비동기로 읽어가므로, 방금 넘긴 버퍼를 덮어쓰면 안 된다.
# 두 개를 번갈아 쓴다.
bufs = [np.zeros((H, W, 4), dtype=np.uint8) for _ in range(2)]
for b in bufs:
    b[..., 3] = 255
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]

t0 = time.time()
n_ok = n_fail = 0
last_err = None
idx = 0
try:
    while time.time() - t0 < 15.0:
        r, g, b = colors[int((time.time() - t0) / 2.0) % 3]
        buf = bufs[idx]
        idx ^= 1
        buf[..., 0], buf[..., 1], buf[..., 2] = r, g, b
        try:
            ov.setOverlayRaw(
                handle, buf.ctypes.data_as(ctypes.c_void_p), W, H, 4)
            n_ok += 1
        except Exception as e:
            n_fail += 1
            last_err = e
        time.sleep(0.1)          # 10Hz. 20Hz에서 실패가 잦았다면 여기가 원인
finally:
    print(f"\nsetOverlayRaw  성공 {n_ok} / 실패 {n_fail}")
    if last_err is not None:
        print(f"마지막 에러: {type(last_err).__name__}: {last_err}")
    print(f"isOverlayVisible = {ov.isOverlayVisible(handle)}")
    ov.destroyOverlay(handle)
    openvr.shutdown()
