# Code

Implementation and experimental code for the Physical-AI_2026 project.

The current codebase primarily focuses on VR teleoperation, HMD tracking, stereo rendering, coordinate transformation, and robot control experiments.

---

## Directory Structure

~~~text
code/
│
├── vr_teleop/
│   ├── diagnostics/
│   ├── main_vr.py
│   ├── main_wlx.py
│   └── ...
│
├── case_01_headpose_relative_rotation.py
├── case_02_projection_frustum_aspect.py
├── case_03_symmetric_frustum_center.py
├── case_04_same_image_both_eyes.py
├── case_05_fresh_hmd_pose.py
├── case_06_frustum_width_from_render_aspect.py
├── case_07_full_6dof_head_translation.py
├── case_08_predicted_hmd_pose_30ms.py
├── case_09_static_camera_no_vr_override.py
├── case_10_eye_transform_translation_only.py
├── case_11_swap_left_right_submit.py
├── case_12_zero_ipd_eye_translation.py
├── case_13_world_up_lock_no_roll.py
├── case_14_flip_frustum_center_sign.py
├── case_15_flip_vertical_frustum_sign.py
└── README.md
~~~

---

## Main Components

### VR Tracking

Current tracking components include:

- HMD position
- HMD rotation
- VR controller position
- VR controller rotation
- 6DoF motion
- Predicted HMD pose

---

## Camera / Projection

Current experiments include:

- View matrix
- Projection matrix
- Stereo rendering
- Frustum configuration
- Aspect ratio
- Eye transformation
- Interpupillary distance
- Camera coordinate transformation

---

## Robot Control

The target control pipeline is:

~~~text
VR Controller Pose
        ↓
Coordinate Conversion
        ↓
Reference Pose
        ↓
Robot End-Effector Command
        ↓
Gripper Command
~~~

Current control components include:

- Position control
- Orientation control
- Relative motion
- Deadzone handling
- Gripper input
- VR-to-Robot coordinate transformation

---

## Diagnostic Cases

### Case 01 — Head Pose Relative Rotation

Tests relative HMD rotation behavior.

### Case 02 — Projection Frustum Aspect

Validates projection matrix and frustum aspect ratio.

### Case 03 — Symmetric Frustum Center

Tests symmetric stereo frustum configuration.

### Case 04 — Same Image Both Eyes

Renders identical images to both eyes for stereo debugging.

### Case 05 — Fresh HMD Pose

Tests real-time HMD pose updates.

### Case 06 — Frustum Width from Render Aspect

Validates frustum width using the render aspect ratio.

### Case 07 — Full 6DoF Head Translation

Tests full HMD translation and rotation.

### Case 08 — Predicted HMD Pose

Tests predicted HMD pose for rendering latency compensation.

### Case 09 — Static Camera / No VR Override

Uses a fixed virtual camera to isolate VR camera transformation issues.

### Case 10 — Eye Transform Translation Only

Applies only translation from the VR eye transform.

### Case 11 — Swap Left / Right Eye

Tests stereo rendering by swapping the submitted eye images.

### Case 12 — Zero IPD Eye Translation

Removes IPD-based eye translation for debugging.

### Case 13 — World Up Lock / No Roll

Suppresses HMD roll and locks the camera to the world-up direction.

### Case 14 — Flip Frustum Center Sign

Tests the horizontal frustum sign convention.

### Case 15 — Flip Vertical Frustum Sign

Tests the vertical frustum sign convention.

---

## Development Flow

~~~text
VR Tracking
    ↓
Stereo / Camera Validation
    ↓
Coordinate Transformation
    ↓
Robot Command Generation
    ↓
Simulation Validation
    ↓
Real Robot Integration
~~~

---

## Running the Code

Example:

~~~bash
cd code/vr_teleop
python main_vr.py
~~~

Actual commands may differ depending on the current experimental configuration.

---

## Development Guidelines

Before modifying code:

~~~bash
git pull
~~~

After modifications:

~~~bash
git status
git add .
git commit -m "Describe the code update"
git push
~~~

Avoid committing:

- Temporary files
- Large videos
- `.DS_Store`
- Credentials
- Passwords
- Private IP configuration
- Machine-specific secrets

---

## Notes

The `case_XX` scripts are diagnostic experiments.

They may be removed, reorganized, or merged after the VR rendering and teleoperation pipeline becomes stable.

# VR Diagnostic Experiment Checklist

## Common Checklist

각 Case를 실행할 때 아래 항목을 공통으로 확인한다.

### Environment

- Date:
- Machine:
- Git Commit:
- Conda Environment:
- SteamVR:
- ALVR:
- HMD:
- Script:
- Scene:
- Render Resolution:
- FPS:

---

### Before Running

- [ ] SteamVR 정상 실행
- [ ] ALVR 연결 정상
- [ ] Quest 2 tracking 정상
- [ ] Left / Right eye rendering 정상
- [ ] Python environment 확인
- [ ] 실행할 Case 파일 확인
- [ ] Baseline과 비교할 준비
- [ ] 실험 시작 시 HMD 위치 / 자세를 최대한 동일하게 설정

---

### During Experiment

#### HMD Rotation

- [ ] Yaw: 고개를 좌/우로 돌렸을 때 예상 방향으로 회전
- [ ] Pitch: 고개를 위/아래로 움직였을 때 예상 방향으로 회전
- [ ] Roll: 고개를 기울였을 때 예상 방향으로 회전
- [ ] 회전 방향 inversion 없음
- [ ] 회전 scale이 과도하거나 부족하지 않음
- [ ] 회전 중 camera drift 없음

#### HMD Translation

- [ ] Forward / Backward
- [ ] Left / Right
- [ ] Up / Down
- [ ] 이동 방향 inversion 없음
- [ ] 실제 머리 이동량과 virtual camera 이동량이 자연스러움
- [ ] head translation 시 scene이 비정상적으로 확대 / 축소되지 않음

#### Stereo Rendering

- [ ] Left eye / Right eye image가 정상
- [ ] 두 눈이 뒤바뀌지 않음
- [ ] Vertical mismatch 없음
- [ ] Horizontal disparity가 자연스러움
- [ ] Double vision 없음
- [ ] Depth perception이 자연스러움
- [ ] 가까운 물체 / 먼 물체의 깊이감이 자연스러움

#### Projection / Frustum

- [ ] 화면이 좌우로 찌그러지지 않음
- [ ] 화면이 상하로 찌그러지지 않음
- [ ] 중심점이 한쪽으로 치우치지 않음
- [ ] Head rotation 시 world geometry가 휘어 보이지 않음
- [ ] Head translation 시 geometry가 비정상적으로 움직이지 않음
- [ ] Near / Far clipping 문제 없음

#### Performance

- [ ] FPS 안정적
- [ ] HMD 움직임과 화면 사이 latency가 심하지 않음
- [ ] Judder 없음
- [ ] Flickering 없음
- [ ] Frame drop 없음
- [ ] 장시간 사용 시 drift 증가 여부 확인

---

# Case-specific Checklist

## Case 01 — Head Pose Relative Rotation

### Goal
Startup pose를 reference로 사용했을 때 relative HMD rotation이 정상적인지 확인.

### Check

- [ ] 시작할 때 현재 HMD orientation이 기준점이 됨

    -> starting : wall
    -> as i turn back, the usuall scene come out 

- [ ] 시작 방향과 관계없이 virtual camera가 자연스럽게 시작
- [ ] Yaw 방향 정상

--> 

- [ ] Pitch 방향 정상
- [ ] Roll 방향 정상
- [ ] 머리를 원래 자세로 돌리면 camera도 초기 orientation으로 복귀
- [ ] 시작 자세에 따른 persistent offset 없음

### Watch For

- 회전축 뒤바뀜
- sign inversion
- startup orientation offset
- world가 머리 움직임과 같이 따라오는 현상
- roll / pitch coupling

-> left, right tilting severe
-> seems like more larger 

---

## Case 02 — Projection Frustum Aspect

### Goal
Projection frustum과 render aspect ratio가 일치하는지 확인.

### Check

- [ X ] 원형 물체가 타원처럼 보이지 않음
- [ X ] 정사각형이 정상 비율로 보임 
- [ severe ] horizontal stretching 없음
- [ O ] vertical stretching 없음
- [ O ] Left / Right eye aspect 동일
- [ ] 화면 가장자리 distortion 확인

-> starting : wall
->

### Watch For

- 화면 좌우 압축 -> not that much
- 화면 상하 압축 -> severe
- FOV가 지나치게 넓거나 좁음 

---

## Case 03 — Symmetric Frustum Center

### Goal
Symmetric frustum을 사용했을 때 stereo center 문제가 개선되는지 확인.

### Check

- [ ] 두 눈의 image center가 자연스럽게 정렬
- [ ] 화면 중심 object가 두 눈에서 과도하게 이동하지 않음
- [ ] depth perception 유지
- [ ] head rotation 시 center drift 없음

### Watch For

- 눈 사이 depth collapse
- cross-eyed 느낌
- center offset 감소 / 증가

same as case 2

---

## Case 04 — Same Image Both Eyes

### Goal
Stereo geometry 문제가 left/right rendering 자체에서 발생하는지 격리.

### Check

- [ ] 두 눈에 동일한 image가 표시됨
- [ ] double vision이 사라지는지 확인
- [ ] discomfort가 감소하는지 확인
- [ ] 기존 stereo case와 비교

### Interpretation

- 동일 image에서 문제가 사라짐
  → stereo eye transform / projection 문제 가능성

- 동일 image에서도 문제가 지속됨
  → HMD camera pose / rendering pipeline 문제 가능성

---

## Case 05 — Fresh HMD Pose

### Goal
각 frame에서 최신 HMD pose를 사용할 때 tracking 품질 확인.

### Check

- [ ] 빠른 head motion에서 latency 감소
- [ ] head rotation response 개선
- [ ] translation response 개선
- [ ] pose jitter 증가 여부
- [ ] frame synchronization 확인

---

## Case 06 — Frustum Width from Render Aspect

### Goal
Render aspect로 계산한 frustum width가 올바른 geometry를 만드는지 확인.

### Check

- [ X ] horizontal FOV 자연스러움
- [ X ] vertical FOV와 비율 일치
- [ X ] geometry distortion 감소
- [ X ] Left / Right eye 동일한 scale 유지

---

## Case 07 — Full 6DoF Head Translation

### Goal
HMD rotation + XYZ translation 전체를 virtual camera에 적용.

### Check

- [ ] 좌우 이동
- [ ] 앞뒤 이동
- [ ] 위아래 이동
- [ ] yaw
- [ ] pitch
- [ ] roll
- [ ] translation + rotation 동시 수행

### Important

실제 머리를 왼쪽으로 움직였을 때
virtual world가 오른쪽으로 자연스럽게 parallax되는지 확인.

### Watch For

- translation scale 과다
- axis swap
- forward/backward inversion
- camera가 orbit처럼 움직이는 현상

---

## Case 08 — Predicted HMD Pose

### Goal
Predicted pose가 motion-to-photon latency를 줄이는지 확인.

### Check

- [v] 빠른 yaw에서 latency 감소
- [v] 빠른 pitch에서 latency 감소
- [v] head stop 후 overshoot 여부
- [ ] jitter 증가 여부
- [ ] prediction 적용 전 / 후 체감 비교
- The floor moves together as we move the headset. 
- Therefore, the floor(Hexagon becomes)
-Still retengular.
- Little buffering. 

### Record

- Prediction time:
- FPS:
- Subjective latency:
- Overshoot:

---

## Case 09 — Static Camera / No VR Override

### Goal
VR pose transformation을 완전히 제거하여 baseline rendering 확인.

### Check

- [v] HMD를 움직여도 virtual camera 고정
- [no distortion] geometry distortion 존재 여부
- [nothing] stereo image 자체의 이상 여부
- [ ] projection 문제와 tracking 문제 분리


### Interpretation

Static camera는 정상인데 VR tracking case가 이상함
→ HMD pose / coordinate transform 문제 가능성

---

## Case 10 — Eye Transform Translation Only

### Goal
Eye transform에서 translation만 적용하여 rotation component 문제 여부 확인.

### Check

- [v] stereo separation 정상
- [v] depth perception 정상
- [ ] eye rotation 제거 시 image alignment 개선 여부
- [v] head rotation 시 artifact 변화 확인
- horizontally narrower
- no buffering
- high resolution
- preferred
---

## Case 11 — Swap Left / Right Eye

### Goal
Left / Right eye assignment이 뒤집혀 있는지 확인.

### Check

- [ ] 기존보다 depth가 자연스러워지는지 확인
- [v] 기존보다 훨씬 불편해지는지 확인
- [ ] near object depth 방향 확인

### Interpretation

Swap 후 정상
→ 기존 eye submission이 반대였을 가능성

Swap 후 더 악화
→ 기존 eye order가 맞을 가능성

---

## Case 12 — Zero IPD Eye Translation

### Goal
IPD translation이 stereo 문제의 원인인지 확인.

### Check

- [v] double vision 변화
- [higher] depth perception 변화
- [ ] image center alignment 변화
- [ ] eye strain 변화

-lagged
longer vercially
### Watch For



IPD 제거 후 flat image처럼 보이는 것은 정상적인 결과일 수 있음.

---

## Case 13 — World Up Lock / No Roll

### Goal
HMD roll이 camera instability의 원인인지 확인.

### Check

- [v] 고개를 좌우로 기울여도 horizon 유지
- [v] yaw / pitch는 정상 작동
- [v] world-up 안정성 향상 여부
- [v] 기존 case 대비 motion comfort 확인

distortion 
vertically narrower(this must be done first)
low to normal latency
Preffered

### Interpretation

No-roll에서 크게 개선됨
→ camera frame / roll handling 문제 가능성

---

## Case 14 — Flip Frustum Center Sign

### Goal
Horizontal asymmetric frustum sign convention 확인.

### Check

- [x] stereo center alignment 개선 여부
- [x] horizontal double vision 감소 여부
- [ ] depth perception 개선 여부
- [ ] Left / Right edge distortion 변화
distortion 
normal latency

### Result

- Original sign:
- Flipped sign:
- Better:

---

## Case 15 — Flip Vertical Frustum Sign

### Goal
Vertical frustum offset sign convention 확인.

### Check

- [ ] vertical eye mismatch 감소
- [ ] horizon alignment 개선
- [ ] image가 위 / 아래로 갈라지는 현상 감소
- [ ] head pitch 시 distortion 감소

### Result

- Original sign:
- Flipped sign:
- Better:

high latency
distortion
single vision


---

# Experiment Result Template

각 Case가 끝날 때 아래 형식으로 기록한다.

## Case XX — Experiment Result

### Date

-

### Script

`case_XX_....py`

### Goal

-

### Expected

-

### Observed

-

### Result

- [ ] PASS
- [ ] PARTIAL
- [ ] FAIL

### Visual Quality

- Stereo:
- Depth:
- Distortion:
- Tracking:
- Comfort:

### Performance

- FPS:
- Latency:
- Frame Drop:
- Jitter:

### Issues

-

### Suspected Cause

-

### Comparison with Baseline

-

### Evidence

- Screenshot:
- Video:
- Terminal Log:

### Conclusion

-

### Next Action

-

---

# Final Comparison

모든 Case가 끝난 뒤 정리한다.

| Case | Main Variable | Result | Improvement | Main Issue |
|---|---|---|---|---|
| 01 | Relative HMD Rotation | | | |
| 02 | Frustum Aspect | | | |
| 03 | Symmetric Frustum | | | |
| 04 | Same Image Both Eyes | | | |
| 05 | Fresh HMD Pose | | | |
| 06 | Render Aspect | | | |
| 07 | Full 6DoF | | | |
| 08 | Predicted Pose | | | |
| 09 | Static Camera | | | |
| 10 | Eye Translation Only | | | |
| 11 | Swap Eyes | | | |
| 12 | Zero IPD | | | |
| 13 | No Roll | | | |
| 14 | Horizontal Frustum Sign | | | |
| 15 | Vertical Frustum Sign | | | |

---

## Final Decision

### Best Configuration

-

### Cases That Improved Rendering

-

### Cases That Made Rendering Worse

-

### Root Cause Candidates

1.
2.
3.

### Configuration to Keep

-

### Configuration to Remove

-

### Next Development Step

-