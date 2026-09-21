# VR Teleoperation & Robot Learning

## 1. VR Teleoperation — Final Configuration

### Final Execution Command

2026-09-18 로봇 연구실에서 성공한 최종 실행 명령어.

```bash
python main_vr_scene.py --fov-scale-x 0.5
```

### TODO — 2026-09-22

- [ ] 성공 당시 사용한 `main_vr_scene.py`의 실제 경로 확인
- [ ] `--fov-scale-x` 인자 구현 여부 확인
- [ ] GitHub 코드와 비교
- [ ] 최종 성공 코드 보존 및 GitHub 반영
- [ ] README 및 SETUP 문서의 실행 명령어 통일

**Note:** 현재 확인한 GitHub 코드에는 `--fov-scale`만 정의되어 있으므로 실제 성공한 코드 버전을 먼저 확인할 것.

---

## 2. Overall Research Pipeline

```text
Step 1. Task Selection
        ↓
Step 2. VR Teleoperation
        ↓
Step 3. Synthetic Data Generation
        ↓
Step 4. Policy Learning
        ↓
Step 5. Evaluation & Generalization
```

### Step 1. Task Selection

- 어떤 Robot Manipulation Task를 학습할 것인가?
- Object Lifting → Pick-and-Place

### Step 2. VR Teleoperation

- Quest 2를 이용한 Human Demonstration 수집
- 초기 목표: 5~10개의 성공적인 Demonstration
- Robot State, Action, Object Pose 기록

### Step 3. Synthetic Data Generation

- Object Position / Goal Position Randomization
- Object-centric Trajectory Transformation
- Simulation Rollout 및 성공 여부 검증
- 초기 목표: 100개 → 1,000개 이상의 Synthetic Demonstration

### Step 4. Policy Learning

- Behavior Cloning (BC)
- Diffusion Policy
- Flow Matching-based Policy

초기에는 BC를 Baseline으로 사용하고, 이후 다른 Policy로 확장하는 방안을 검토한다.

### Step 5. Evaluation

- Task Success Rate
- Unseen Object / Goal Position
- Synthetic Data의 양에 따른 성능 비교
- 실제 xArm7을 이용한 Sim-to-Real 평가

---

## 3. RQ 1 — Which Task?

> 5~10회의 Teleoperation을 어떤 Task로 수행할 것인가?

### Task A. Object Lifting

- 현재 robosuite `Lift` 환경 활용
- VR Controller → 가상 xArm7 제어 검증
- 물체 접근 → 파지 → 들어 올리기
- Demonstration Logging 구현

**Purpose:** VR Teleoperation 및 데이터 수집 시스템 검증

### Task B. Pick-and-Place

- 물체 접근 → 파지 → 이동 → 배치
- Object / Goal Position을 다양하게 설정
- 5~10회의 성공적인 Human Demonstration 수집

**Purpose:** Synthetic Data Generation 및 Policy Learning을 위한 기준 Task

---

## 4. RQ 2 — How to Generate Synthetic Data?

> 소수의 Human Demonstration을 어떻게 1,000개 이상의 Synthetic Demonstration으로 확장할 것인가?

### Candidate A. MimicGen-style Data Generation

- Object-centric Trajectory Transformation
- Object / Goal Position Randomization
- Simulation Rollout
- Task Success Validation

```text
5~10 Human Demonstrations
          ↓
Object-centric Transformation
          ↓
Environment Randomization
          ↓
Simulation Rollout
          ↓
100~1,000+ Synthetic Demonstrations
```

**Reference:** [MimicGen](https://arxiv.org/abs/2310.17596)

### Candidate B. Generative Model

- Diffusion Model
- Flow Matching

기존 Demonstration을 학습하여 새로운 Action Sequence 또는 Trajectory를 생성하는 방법을 검토한다.

단, 5~10개의 Demonstration만으로 생성 모델을 충분히 학습할 수 있는지는 별도의 검증이 필요하다.

**Initial Plan:** MimicGen 방식의 데이터 생성 파이프라인을 먼저 구축하고, 이후 생성 모델 기반 방법으로 확장한다.

---

## 5. RQ 3 — Policy Learning

> 생성된 Synthetic Data로 어떤 Robot Policy를 학습할 것인가?

| Method | Purpose |
|---|---|
| Behavior Cloning | 초기 Baseline |
| Diffusion Policy | Action Sequence Generation |
| Flow Matching | Continuous Action Generation |

초기에는 동일한 BC 모델을 사용하여 Human-only 데이터와 Synthetic Data를 추가한 데이터의 학습 성능을 비교한다.

---

## 6. RQ 4 — Evaluation

> Synthetic Data가 실제로 Robot Learning에 도움이 되는가?

| Experiment | Training Data |
|---|---|
| E1 | Human Demo 10개 |
| E2 | Human Demo 10개 + Synthetic Demo 100개 |
| E3 | Human Demo 10개 + Synthetic Demo 1,000개 |

**Evaluation Metrics**

- Task Success Rate
- Unseen Object / Goal Position Success Rate
- Synthetic Data Generation Success Rate
- Real Robot Success Rate (향후)

---

## 7. Next Steps

- [ ] VR Controller → 가상 xArm7 제어 검증
- [ ] Object Lifting 성공
- [ ] Demonstration Logging 구현
- [ ] Pick-and-Place Task 구성
- [ ] Human Demonstration 5~10개 수집
- [ ] MimicGen 방식의 Synthetic Data Generation 구현
- [ ] BC Baseline 학습 및 평가

**Research Goal:** 소수의 VR Demonstration을 활용한 Synthetic Robot Data Generation 및 Data-efficient Robot Policy Learning.