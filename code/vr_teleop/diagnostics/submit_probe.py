"""
SteamVR OpenGL Submit 경로 생존 확인 probe.
MuJoCo 없이 GL 텍스처 하나를 만들어 컴포지터에 제출한다.

필요: pip install PyOpenGL glfw

기대 결과:
    헤드셋 왼쪽 눈에 빨강, 오른쪽 눈에 파랑이 10초간 꽉 찬다.
    (한쪽 눈씩 감아서 확인)

    -> 보이면 Submit 경로 정상. 본 구현으로 진행 가능.
    -> 검은 화면이거나 지지직거리면 이 GPU/드라이버에서 GL 제출도 깨진 것.
"""

import ctypes
import os
import time

import glfw
import numpy as np
import openvr
from OpenGL import GL

# --- OpenVR: Scene 앱으로 초기화 ------------------------------------------
openvr.init(openvr.VRApplication_Scene)
vr = openvr.VRSystem()
comp = openvr.VRCompositor()

w, h = vr.getRecommendedRenderTargetSize()
print(f"per-eye render target (권장): {w} x {h}")

# 권장 해상도가 너무 크면 제출이 실패할 수 있으므로 작게 내려서 테스트.
# 제출 시 bounds로 스케일되므로 크기가 달라도 화면은 꽉 찬다.
w = h = int(os.environ.get("PROBE_SIZE", "1024"))
print(f"probe 텍스처: 눈당 {w} x {h} (PROBE_SIZE 환경변수로 변경)")

# --- GL 컨텍스트 (보이지 않는 창) -----------------------------------------
if not glfw.init():
    raise RuntimeError("glfw init 실패")
glfw.window_hint(glfw.VISIBLE, False)
window = glfw.create_window(100, 100, "probe", None, None)
if not window:
    raise RuntimeError("glfw 창 생성 실패")
glfw.make_context_current(window)

print("GL_VENDOR  :", GL.glGetString(GL.GL_VENDOR).decode())
print("GL_RENDERER:", GL.glGetString(GL.GL_RENDERER).decode())
print("GL_VERSION :", GL.glGetString(GL.GL_VERSION).decode())

# --- 좌우 나란히 텍스처 (왼쪽 빨강 / 오른쪽 파랑) -------------------------
img = np.zeros((h, 2 * w, 4), dtype=np.uint8)
img[:, :w] = (220, 40, 40, 255)
img[:, w:] = (40, 80, 220, 255)
img = np.ascontiguousarray(img)

tex = GL.glGenTextures(1)
GL.glBindTexture(GL.GL_TEXTURE_2D, tex)
GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_CLAMP_TO_EDGE)
GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_CLAMP_TO_EDGE)
GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGBA8, 2 * w, h, 0,
                GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, img)
GL.glBindTexture(GL.GL_TEXTURE_2D, 0)
GL.glFinish()

err = GL.glGetError()
if err != GL.GL_NO_ERROR:
    print(f">>> GL 에러 0x{err:x} (텍스처 생성 단계)")

# --- Submit 준비 ----------------------------------------------------------
texture = openvr.Texture_t()
texture.handle = ctypes.c_void_p(int(tex))
texture.eType = openvr.TextureType_OpenGL
texture.eColorSpace = openvr.ColorSpace_Auto

# 한 텍스처를 좌/우 절반으로 나눠 각 눈에 제출
bounds_left = openvr.VRTextureBounds_t(0.0, 0.0, 0.5, 1.0)
bounds_right = openvr.VRTextureBounds_t(0.5, 0.0, 1.0, 1.0)

poses_t = openvr.TrackedDevicePose_t * openvr.k_unMaxTrackedDeviceCount
poses = poses_t()

seen = set()


def gl_check(tag):
    """대기 중인 GL 에러를 소모하고 최초 1회만 보고한다."""
    e = GL.glGetError()
    if e != GL.GL_NO_ERROR and tag not in seen:
        seen.add(tag)
        print(f">>> GL 에러 0x{e:x} ({e}) 발생 지점: {tag}")
    return e


# --- 제출 루프 ------------------------------------------------------------
print("\n10초간 제출합니다. 헤드셋을 착용하고 한쪽 눈씩 감아 확인하세요.")
gl_check("루프 진입 전")

t0 = time.time()
n_ok = n_fail = 0
last_err = None
try:
    while time.time() - t0 < 10.0:
        comp.waitGetPoses(poses, None)   # HMD 주사율에 맞춰 블로킹
        gl_check("waitGetPoses 직후")
        try:
            comp.submit(openvr.Eye_Left, texture, bounds_left)
            gl_check("submit(Left) 직후")
            comp.submit(openvr.Eye_Right, texture, bounds_right)
            gl_check("submit(Right) 직후")
            n_ok += 1
        except Exception as e:
            n_fail += 1
            last_err = e
            gl_check("submit 예외 직후")
        # glFlush는 대기 중인 에러가 있으면 PyOpenGL이 예외로 올리므로
        # 위 gl_check가 이미 에러를 소모한 뒤에 호출한다.
        try:
            GL.glFlush()
        except Exception as e:
            if "flush" not in seen:
                seen.add("flush")
                print(f">>> glFlush 예외: {e}")
finally:
    fps = n_ok / max(time.time() - t0, 1e-6)
    print(f"\nsubmit 성공 {n_ok} / 실패 {n_fail}  ({fps:.1f} fps)")
    if last_err is not None:
        print(f"마지막 에러: {type(last_err).__name__}: {last_err}")
    e = GL.glGetError()
    if e != GL.GL_NO_ERROR:
        print(f">>> GL 에러 0x{e:x} (루프 종료 시점)")
    GL.glDeleteTextures(1, [tex])
    glfw.terminate()
    openvr.shutdown()
