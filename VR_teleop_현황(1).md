# Quest 2 + robosuite VR 텔레오퍼레이션 — 현황 정리

## 목표

Oculus Quest 2로 robosuite(MuJoCo) 시뮬레이션 안의 로봇 팔을 조종한다.
헤드셋 안에서 머리 트래킹이 되는 입체 시야로 장면을 보면서, 오른손
컨트롤러로 엔드이펙터를 움직인다.

---

## 환경

| 항목 | 값 |
|---|---|
| OS | Ubuntu 24.04 LTS (X11 세션) |
| GPU | NVIDIA RTX PRO 5000 Blackwell 48GB |
| 드라이버 | 595.71.05 |
| 헤드셋 | Quest 2 (SteamVR 모델명 `Miramar`), 72Hz |
| 연결 | ALVR 유선(USB-C, ADB 터널) → SteamVR |
| Python | 3.10 (conda `robosuite` 환경) |
| 주요 패키지 | robosuite, mujoco, pyopenvr, PyOpenGL, glfw, scipy |

`robosuite_models`는 미설치. XArm7은 robosuite 본체에 있어 동작함.

---

## 최종 아키텍처

```
Quest 2  ──ALVR(USB)──▶  SteamVR  ──OpenVR──▶  main_vr_scene.py
                                                    │
  컨트롤러 입력 ◀── IVRSystem.getControllerState ────┤
  머리 포즈     ◀── WaitGetPoses ────────────────────┤
                                                    │
                          MuJoCo mjr_render (SBS)  ─┤
                          → glBlitFramebuffer      ─┤
                          → IVRCompositor::Submit ──┘
```

- `VRApplication_Scene`으로 초기화 (Scene 앱 = 화면 전체를 점유)
- MuJoCo를 `mjSTEREO_SIDEBYSIDE`로 한 텍스처에 좌우안 동시 렌더
- `scn.camera[0]`, `scn.camera[1]`(`mjvGLCamera`)를 OpenVR의 눈 포즈·
  투영값으로 매 프레임 덮어씀
- MuJoCo 오프스크린 렌더버퍼 → 자체 FBO 텍스처로 GPU 내부 blit (CPU 왕복 없음)
- `Submit` 2회, `VRTextureBounds_t`로 텍스처를 좌/우 절반으로 분할
- 루프 72Hz, 물리는 20Hz 누적 방식

### 좌표계 변환

```
OpenVR standing space : +X 오른쪽, +Y 위,   -Z 전방
robosuite / MuJoCo    : +X 전방,   +Y 왼쪽, +Z 위

VR2ROBOT = [[ 0, 0, -1],
            [-1, 0,  0],
            [ 0, 1,  0]]     (det = +1)
```

**두 곳에서 규칙이 다르므로 주의:**

| 용도 | 공식 | 이유 |
|---|---|---|
| 카메라 축 추출 | `C @ R_vr` | `R_vr`의 열이 이미 월드 표현이므로 왼쪽 곱 1회 |
| 컨트롤러 회전 델타 | `C @ R @ C.T` | 상대회전이므로 상사변환이 맞음 |

---

## 파일

| 파일 | 용도 |
|---|---|
| `main_vr_scene.py` | **최종본.** Scene 앱 + 머리 트래킹 스테레오 |
| `main_wlx.py` | 대안. 데스크톱 창 + WayVR 미러링 (평면) |
| `main_vr.py` | 구버전. OpenVR 오버레이 패널 방식 (실패) |
| `submit_probe.py` | Submit 경로 생존 확인 probe |
| `overlay_test.py` | 오버레이 경로 확인 probe |

### `main_vr_scene.py` 진단 옵션

```bash
--debug            GL 에러 위치 보고 + /tmp/mj_f0.png, /tmp/mj_f30.png 덤프
--print-pose       머리 요/피치/롤 주기 출력
--gpu-sync         렌더 후 glFinish로 실제 GPU 시간 측정
--no-vr-cam        머리 트래킹 끄고 고정 궤도 카메라로 렌더
--same-both-eyes   두 눈에 같은 이미지 (양안 불일치 격리)
--roll-test 30     카메라에 고정 롤 강제 주입
--no-msaa          멀티샘플 끄기
--eye-scale 0.45   눈당 렌더 해상도 배율
--fov-scale-x 0.5  가로 화각 추가 배율 (기본 FRUSTUM_X_SCALE 위에 곱해짐)
--two-pass         SBS 대신 각 눈을 모노로 따로 렌더
--width-scale 0.5  눈당 렌더 가로 픽셀 배율
```

---

## 해결된 문제들

### 1. 원본 코드의 기본 버그

- `R` 미임포트 (`scipy.spatial.transform.Rotation`)
- `waitGetPoses`에 컴포지터 객체를 인자로 전달
- `prev_pos = zeros`로 첫 프레임 델타가 컨트롤러 절대좌표만큼 튐
- 좌표계 변환 부재 (VR Y-up ↔ MuJoCo Z-up)
- 회전 델타를 오일러 뺄셈으로 계산 → 상대회전 axis-angle로 교체
- **액션 스케일 미적용**: OSC_POSE는 `[-1,1]` 정규화 입력이고
  `output_max=[0.05, 0.05, 0.05, 0.5, 0.5, 0.5]`.
  미터 단위 델타를 그대로 넣어 로봇이 사실상 안 움직였음

### 2. Linux에서 Quest 2 연결

- Meta Quest Link는 Windows 전용 → ALVR 사용
- ALVR 유선은 **ADB 포트 포워딩 터널** 위의 TCP. Meta 소프트웨어 불필요
- SteamVR 실행 옵션에 `vrmonitor.sh %command%` 필수 (없으면 검은 화면)
- 개발자 모드는 휴대폰 Meta Horizon 앱에서만 켤 수 있음
  (조직 생성 + SMS/결제수단 인증 선행)

### 3. `mujoco.Renderer` 생성 실패

`AttributeError: 'Renderer' object has no attribute '_gl_context'`는 부수 효과.
실제 원인은 요청 해상도 > 오프스크린 버퍼(기본 640×480).

```python
model.vis.global_.offwidth  = W
model.vis.global_.offheight = H   # Renderer/MjrContext 생성 전에
```

### 4. 검은 화면 (핵심 버그)

**원인: 프레임버퍼 바인딩.** `blit_from_mujoco`가 매 프레임 끝에
`glBindFramebuffer(GL_FRAMEBUFFER, 0)`으로 되돌려서, 2프레임째부터
MuJoCo가 숨겨진 100×100 glfw 창에 그리고 있었음.

```python
mujoco.mjr_setBuffer(mujoco.mjtFramebuffer.mjFB_OFFSCREEN, con)  # 매 프레임
mujoco.mjr_render(viewport, scn, con)
```

### 5. 카메라가 바닥을 봄

축 추출에 상사변환(`C R C^T`)을 써서, HMD가 항등일 때 forward가
`[0,0,-1]`(수직 하방)이 됨. `C @ R_vr`로 수정.

### 6. SteamVR GL Submit의 GL_INVALID_VALUE

**SteamVR의 GL 제출 경로는 매 프레임 `GL_INVALID_VALUE`(0x501)를 남김.**
제출 자체는 정상. 비우지 않으면 PyOpenGL이 다음 GL 호출에서 예외를 던지며
프로세스가 죽음.

```python
def drain_gl_errors():
    while GL.glGetError() != GL.GL_NO_ERROR: ...
```

`waitGetPoses` 직후와 `submit` 직후에 호출. **이게 이 프로그램의 생명줄.**

### 7. 화면이 세로로 2배 길어 보임 (최종 해결)

**원인: `mjvGLCamera.frustum_width`는 '반폭'이다.**

`frustum_top`/`frustum_bottom`이 ±h/2인 것과 같은 규약. 전체 폭
`(right - left)`를 넣어서 가로 화각이 정확히 2배가 됐고, 결과적으로
세로:가로가 2:1로 보였다.

```python
FRUSTUM_X_SCALE = 0.5   # 좌우 탄젠트를 중심 기준 0.5배
```

**진단의 결정적 단서:** 머리를 90도 롤했을 때 긴 쪽과 짧은 쪽이 뒤바뀜.
→ 왜곡이 월드가 아니라 화면(눈)에 고정 → 비등방 스케일 = 종횡비 문제 확정.
이 한 번의 관찰로 카메라 포즈 계열 가설이 전부 정리됐다.

그리고 이것이 "움직이면 평행사변형" 증상의 원인이기도 했다. 화면 공간에서
세로로 늘어난 상태로 월드가 회전하면 직사각형이 평행사변형으로 보인다.
정지 시에는 정상, 움직일 때만 나타나는 것도 이걸로 설명된다.

### 8. 프레임레이트 36 → 72

ALVR **Transcoding view resolution**을 낮춤 (2624×2860 → 1516×1652).
Emulated headset view resolution이 아님에 주의.

---

## 해결 과정에서 배제된 가설들

증상: 정지 시 정사각형, 움직이면 평행사변형. 직선은 유지. 단안에서도 발생.
최종 원인은 위 7번(frustum_width 반폭 규약).

### 배제된 원인

| 가설 | 검증 방법 | 결과 |
|---|---|---|
| 렌더 성능 부족 | 해상도 8배 축소 | fps 변화 없음 (34→36) |
| GPU 렌더 병목 | `--gpu-sync` | `render=0.9ms`. 결백 |
| 종횡비 불일치 | frustum 비율에서 직접 유도 | `OK` 확인. 증상 유지 |
| 카메라 롤 미적용 | `--roll-test 30` | MuJoCo 정상 적용 |
| 머리 포즈 오류 | `--print-pose` | yaw/pitch/roll 모두 정상 추종 |
| 컴포지터 리프로젝션 | `--no-vr-cam` 정지 이미지 | **워프 없음.** 이미지 고정 |
| 양안 불일치 | 한쪽 눈 감기 | 단안에서도 왜곡 유지 |
| 투영 왜곡 | 직선 관찰 | 직선 유지 = 투영 문제 아님 |
| Foveated encoding | ALVR에서 끔 | 차이 없음 |
| SteamVR 모션 스무딩 | — | ALVR은 지원 안 함 |
| 좌우안 bounds 교환 | 수동 교체 | 차이 없음 |

### 현재 성능 프로파일 (72fps 상태)

```
wait=10.5  scene=0.1  render=0.9  blit=0.3  submit=0.2  input=0.2  physics=1.8
wait 제외 합계 3.4 ms / 예산 13.9 ms
```

**우리 코드는 예산의 25%만 사용.** 코드 최적화 여지 없음.

### 진단을 오래 끈 이유

증상이 "움직일 때만" 나타나서 **지연/리프로젝션 문제로 오인**했다.
실제로는 정적인 종횡비 오류였고, 회전이 그것을 눈에 띄게 만든 것뿐이었다.

교훈: "움직일 때만 이상하다"가 반드시 시간축 문제를 뜻하지는 않는다.
**머리를 90도 롤해보면** 왜곡이 월드에 붙어 있는지 화면에 붙어 있는지
한 번에 갈린다. 이 테스트를 먼저 했어야 했다.

---

## 남은 과제

### Total latency 40~60ms

encode/network는 각 5ms 미만인데 총합이 크다. 편안한 VR 기준은 20ms 이하.
현재 조작에 지장은 없으나 개선 여지가 있다.
리프로젝션이 전혀 걸리지 않는 것도 확인됐다(`--no-vr-cam`에서 정지 이미지가
머리를 따라 움직이지 않음).

### 선택: WiVRn + Monado 이전

SteamVR을 버리고 OpenXR 런타임으로 교체.

근거: 이 GPU에서 SteamVR 텍스처 경로가 **세 번** 깨졌다.
1. `SetOverlayRaw` — 화면 깨짐, 컴포지터 정지
2. WayVR DMA-buf GPU 캡처 — `no target node available`
3. GL `Submit` — 매 프레임 `GL_INVALID_VALUE`

Monado는 Vulkan 네이티브 + 오픈소스라 신형 하드웨어 대응이 빠르고
문제 추적이 가능하다.

작업량:
- robosuite 물리·제어: **변경 없음**
- 좌표 변환·클러치·스케일: **재사용**
- 컨트롤러 입력: `pyopenxr`로 재작성 (~100줄)
- 스테레오 렌더: `xrEndFrame` + 스왑체인으로 교체 (~250줄)
  구조는 동일 (`mjvGLCamera` 덮어쓰기 + SBS + blit)

### 선택: 환경 개선

- **X11 → Wayland 세션.** X11에서 제로카피 GPU 캡처 미지원 등 제약 다수
- NVIDIA 드라이버 버전 변경 시도 (595.71.05는 매우 최신)

### 별개 트랙: 손가락 트래킹

- 현재 XArm7의 2지 그리퍼는 자유도 1개 → 손 트래킹 의미 없음
- Allegro Hand(16DOF) 등 다지 핸드로 교체가 선행되어야 함
- `oculus_reader`는 손 관절을 제공하지 않음 (컨트롤러 포즈·버튼만)
- OpenXR의 `XR_EXT_hand_tracking`이 26관절 제공 → WiVRn 이전 시 함께 해결
- 리타게팅은 `dex_retargeting` 패키지 권장

---

## 알아두면 좋은 것들

- `robosuite`의 `legs`/`torso`/`head`/`base` 컨트롤러 경고는 **정상**.
  BASIC 설정에 정의된 파트를 XArm7이 갖고 있지 않아 건너뛴다는 안내일 뿐
- SteamVR 대시보드가 열려 있으면 컨트롤러 입력을 독점한다. 절대 열지 말 것
- ALVR은 헤드셋 근접 센서가 눌린 상태여야 트래킹이 돈다. 벗어두면 멈춤
- `InitError_Init_AnotherAppLaunching`은 이전 프로세스가 아직 살아 있다는 뜻
- Scene 앱 비정상 종료 후 SteamVR 303 에러가 나면 좀비 프로세스 정리:
  `pkill -9 vrcompositor vrserver vrmonitor vrdashboard vrwebhelper`
