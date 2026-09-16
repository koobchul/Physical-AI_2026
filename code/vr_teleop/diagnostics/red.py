import openvr, time
openvr.init(openvr.VRApplication_Overlay)
vr = openvr.VRSystem()

for i in range(openvr.k_unMaxTrackedDeviceCount):
    c = vr.getTrackedDeviceClass(i)
    if c != openvr.TrackedDeviceClass_Invalid:
        name = vr.getStringTrackedDeviceProperty(i, openvr.Prop_ModelNumber_String)
        print(f"idx={i} class={c} model={name}")

# 작은 단색 오버레이가 뜨는지
import numpy as np, ctypes
ov = openvr.VROverlay()
h = ov.createOverlay("test.overlay", "test")
ov.setOverlayWidthInMeters(h, 1.0)
ov.showOverlay(h)
buf = np.zeros((256, 256, 4), dtype=np.uint8)
buf[..., 0] = 255; buf[..., 3] = 255 # 빨간 사각형
ov.setOverlayRaw(h, buf.ctypes.data_as(ctypes.c_void_p), 256, 256, 4)
time.sleep(10)
openvr.shutdown()