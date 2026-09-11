# MimicGen

## 0. Paper Information

- Title: MimicGen: A Data Generation System for Scalable Robot Learning using Human Demonstrations
- Authors: Ajay Mandlekar, Soroush Nasiriany, Bowen Wen, Iretiayo Akinola, Yashraj Narang, Linxi Fan, Yuke Zhu, Dieter Fox
- Year: 2023
- Venue: Conference on Robot Learning (CoRL 2023)
- Paper: https://arxiv.org/abs/2310.17596
- Code: https://github.com/NVlabs/mimicgen
- Project: https://mimicgen.github.io/

---

## 1. One-line Summary

> MimicGen은 소수의 human demonstrations를 object-centric subtask로 분해한 뒤, 새로운 scene의 object pose에 맞게 trajectory를 변환·실행하여 대규모 robot demonstration dataset을 생성하는 data generation system

---

## 2. Why this Paper?

Problem
  -
- Imitation Learning은 많은 human demonstrations를 필요로 함
- 하지만 robot demonstration 수집에는 많은 시간과 비용이 필요함
- 다양한 scene, object, robot으로 확장할수록 필요한 데이터의 규모가 급격히 증가함

- robomimic example
  - single scene
  - single object
  - single robot
  - 200 demonstrations
  - success rate: 73.3%

Motivation
  -
- 대규모 robot dataset에는 서로 다른 데이터처럼 보이지만 실제로는 유사한 manipulation behavior가 반복될 수 있음

> How much of this data actually contains unique manipulation behaviors?

- ex. mug의 위치만 달라졌다면 새로운 demonstration을 다시 수집하기보다 기존 grasp trajectory를 새로운 위치에 맞게 재사용할 수 있음
- 기존 human demonstration을 새로운 context에 재활용하면 human data collection burden을 크게 줄임

Main Contribution
  - 
- 소수의 human demonstrations에서 대규모 demonstration dataset을 생성하는 MimicGen 제안
- demonstration을 object-centric subtask 단위로 분할
- 각 segment를 새로운 object pose에 맞게 spatial transformation
- transformed trajectory를 environment에서 직접 실행하고 성공한 trajectory만 저장
- 약 200개의 source human demonstrations에서 18개 task에 대해 50K+ demonstrations 생성
- scene configuration, object instance, robot arm 변화까지 실험
- MimicGen data가 추가 human demonstrations를 직접 수집하는 것과 비교해 경쟁력 있는 policy performance를 보임

---

## 3. Key Concepts

Imitation Learning
  - 
- expert demonstration으로부터 robot policy를 학습
```
    τ = (s0, a0, s1, a1, ..., sH)
```
  - s: state / observation
  - a: expert action

Markov Decision Process (MDP)
  - 
- robot manipulation을 sequential decision-making problem으로 표현
```
    State
      ↓
    Policy
      ↓
    Action
      ↓
    Environment
      ↓
    Next State
```
Behavioral Cloning (BC)
  - 
- Imitation Learning을 supervised learning 형태로 수행
```
    state s → expert action a
```
- MimicGen은 새로운 policy learning algorithm을 제안하기보다 BC가 학습할 demonstration dataset을 확장

Object-Centric Subtask
  - 
- 전체 task를 특정 object를 기준으로 하는 manipulation unit으로 분해

Example:
```
    Mug Grasp  → relative to Mug
    Mug Place  → relative to Coffee Machine
    Pod Grasp  → relative to Pod
    Pod Insert → relative to Coffee Machine
```

Object Pose
  - 
- object의 position과 orientation을 함께 나타냄
- MimicGen은 각 subtask 시작 시 relevant object의 pose를 이용해 source trajectory를 새로운 scene에 맞게 transform
- object pose는 data generation 단계에서 필요하며 final policy deployment에서는 필요하지 않음

Delta End-Effector Pose
  - 
- action을 end-effector의 변화량으로 표현
    - [Δx, Δy, Δz, Δrotation, gripper]
- 이를 통해 source trajectory를 새로운 object pose에 맞게 변환할 수 있음

Online Data Generation
  - 
- 기존 데이터를 단순히 offline으로 변형하는 것이 아니라 transformed trajectory를 environment에서 실제 실행
- 성공한 interaction만 새로운 demonstration으로 저장

---

## 4. Method / Overview

MimicGen은 크게 두 단계로 구성

   - Parse Source Demonstrations
   - Generate New Demonstrations

1. Parse Source Demonstrations
    - 
Human trajectory:
```
    τ
    ↓
    τ1 → τ2 → ... → τM
```
- 각 τi는 하나의 object-centric subtask에 대응.
- subtask 종료 조건을 이용해 trajectory를 segment로 분할.

2. Generate New Demonstrations
   - 
각 subtask마다:
```
    Reference Segment Selection
              ↓
       Current Object Pose
              ↓
      Segment Transformation
              ↓
         Interpolation
              ↓
           Execute
```
- source segment의 absolute trajectory를 그대로 복사하는 것이 아니라 object-relative motion을 보존하도록 새로운 scene에 맞게 transform

모든 subtask 수행 후:
```
    Success → Save
    Failure → Discard
```
---

## 5. MimicGen Pipeline

Source Demonstrations
  - 
- 대부분의 task에서 약 10개의 human demonstrations 사용
- 각 demonstration을 동일한 object-centric subtask sequence로 분해
```
    Demo 1: τ1¹ → τ2¹ → ... → τM¹
    Demo 2: τ1² → τ2² → ... → τM²
    ...
    Demo N: τ1ᴺ → τ2ᴺ → ... → τMᴺ
```
- τ_i^j
  - j: demonstration index
  - i: subtask index

Reference Segment Selection
  -
- 현재 subtask와 대응되는 source segment 중 하나를 선택
- random selection 또는 object pose 기반 nearest-neighbor selection 사용 가능

Object-Centric Transformation
  - 
- absolute trajectory를 복사하는 것이 아니라 object와 end-effector 사이의 relative motion을 보존
```
    Source Object
          ↘
            Source Trajectory

    New Object
          ↘
            Transformed Trajectory
```
- 핵심:

> Preserve object-relative manipulation behavior.

Interpolation
  - 
- 현재 end-effector pose와 transformed segment의 시작점 사이를 연결
```
    Current End-Effector Pose
              ↓
         Interpolation
              ↓
       Transformed Segment
```
- 단순한 interpolation을 사용하기 때문에 collision-free motion을 보장하지는 않음

Execution
  - 
- transformed target poses를 다시 delta-pose action으로 변환
- source segment의 gripper open/close action을 함께 사용
- simulator 또는 physical robot에서 실제 실행
- 각 subtask에 대해 위 과정을 반복

Success Filtering
  - 
- 모든 subtask 실행 후 task success 여부 확인
- 성공한 trajectory만 dataset에 저장
- 실패한 generation attempt는 discard

Data Generation Rate
  - 
> Data Generation Rate  = Successful Generated Trajectories / Total Generation Attempts

---

## 6. Task / Environment Setup

Simulators
  - 
- Robosuite -> MuJoCo backend
- Factory -> Isaac Gym backend

Task Categories
  - 
- Basic
  - Stack
  - Stack Three

- Contact-Rich
  - Square
  - Threading
  - Coffee
  - Three Piece Assembly
  - Hammer Cleanup
  - Mug Cleanup

- Long-Horizon
  - Kitchen
  - Nut Assembly
  - Pick Place
  - Coffee Preparation

- Mobile Manipulation
  - Mobile Kitchen

- High-Precision Assembly
  - Nut-and-Bolt Assembly
  - Gear Assembly
  - Frame Assembly

Task Variants
  - 
```
    D = Initial State Distribution
    O = Object
    R = Robot
```
   - D0: default / source distribution
   - D1: broader distribution
   - D2: more difficult distribution

Object Variants
  - 
   - O1: unseen mug
   - O2: 12 different mugs

Robot Variants
  - 
- Panda
- Sawyer
- IIWA
- UR5e

---

## 7. Important Models / Datasets / Methods

- Behavioral Cloning (Pomerleau et al., NeurIPS 1989)
  -
    - main Imitation Learning framework
    - supervised learning: state → expert action
- BC-RNN (Mandlekar et.al, CoRL 2021)
  - 
  - main policy architecture used in the experiments
  - recurrent Behavioral Cloning policy from robomimic

- Robomimic (Mandlekar et al., CoRL 2021) 
  - 
  - imitation learning framework / benchmark
  - source dataset 및 policy learning에 활용

- robosuite (Zhu et al., arXiv 2020)
  - 
    - MuJoCo 기반 robot manipulation simulation framework

- Factory (Narang et al., RSS 2022)
  -
    - Isaac Gym 기반 high-precision assembly environment

- Diffusion Policy (Chi et al., RSS 2023)
  - 
    - real-world Stack dataset에 추가 실험
    ```
        BC-RNN: 36%
        Diffusion Policy: 76%
    ```
    - MimicGen data는 특정 policy architecture에 종속되지 않음을 보여줌

---

## 8. Experiments

Experimental Setup
  - 
- 대부분의 task:
  - 10 source human demonstrations
  - D0에서 source data 수집
  - task variant마다 1000개의 successful MimicGen demonstrations 생성

- Policy:
  - Behavioral Cloning
  - BC-RNN

- Main evaluation:
  - image-based policy
  - front-view camera
  - wrist-view camera
  - robot proprioception
Main Results
  - 
| Task | Source | MimicGen D0 |
|---|---:|---:|
| Stack | 26.0% | 100.0% |
| Stack Three | 0.7% | 92.7% |
| Square | 11.3% | 90.7% |
| Threading | 19.3% | 98.0% |
| Coffee | 74.0% | 100.0% |
| Three Piece Assembly | 1.3% | 82.0% |
| Kitchen | 54.7% | 100.0% |
| Coffee Preparation | 12.7% | 97.3% |

Broader Initial State Distribution
  -
- narrow source distribution D0의 demonstrations만으로도 D1, D2의 더 넓은 object configuration에서 데이터를 생성할 수 있음

Object Transfer
  -
- 하나의 source mug에서:
  - unseen mug
  - 12개의 mug set

  으로 demonstration 생성

- image policy success:
  - O1: 90.7%
  - O2: 75.3%

Robot Transfer
  - 
- Panda에서 수집한 demonstrations를 이용해:
  - Sawyer
  - IIWA
  - UR5e

  의 데이터를 생성

- robot마다 data generation rate는 달랐지만 trained policy performance는 비교적 유사함

Human Data vs MimicGen Data
   - 
```
    200 Human Demonstrations

    vs

    200 MimicGen Demonstrations
    generated from 10 Human Demonstrations
```
- 많은 task에서 policy performance가 comparable

Number of Source Demonstrations
  - 
- 1 / 10 / 50 / 200 demos 비교
- source demonstrations를 계속 증가시켜도 policy performance가 크게 향상되지는 않음
- 단, 1 demo는 일부 task에서 부족할 수 있음

Number of Generated Demonstrations
  - 
```
    200 → 1000
    large improvement

    1000 → 5000
    diminishing returns
```
Data Generation Rate vs Policy Performance
  - 
- data generation success rate와 downstream policy performance는 반드시 비례하지 않음.

Example:
```
    Gear Assembly D1
    Data Generation Rate: 8.2%
    Policy Success Rate: 76.0%
```
Real Robot
  - 
- Tasks:
  - Stack
  - Coffee

- Data generation success:
  - Stack: 82.3%
  - Coffee: 52.1%

- BC-RNN policy success:
  - Stack: 36%
  - Coffee: 14%

- simulation보다 real-world policy performance가 크게 낮음.
- hardware safety를 위한 긴 interpolation trajectory가 원인 중 하나로 분석됨.

---

## 9. Strengths / Pros

- 매우 적은 human demonstrations로 대규모 dataset 생성 가능
- 기존 Imitation Learning pipeline과 쉽게 결합 가능
- 특정 policy architecture에 종속되지 않음
- 다양한 scene configuration으로 확장 가능
- object instance 변경 가능
- robot hardware 변경 가능
- long-horizon, contact-rich, high-precision task까지 검증
- transformed trajectory를 실제 environment에서 실행하여 physically consistent한 data 생성
- data-centric Robot Learning의 효과를 명확하게 보여줌

---

## 10. Limitations / Cons

- object-centric subtask sequence를 미리 알고 있어야 함
- data generation 단계에서 object pose가 필요함
- 각 subtask가 하나의 reference object에 의존한다고 가정
- simple interpolation 사용
- collision-free trajectory를 보장하지 않음
- task success만을 기준으로 generated data를 filtering하므로 undesirable motion이 포함될 수 있음
- successful generation만 저장하므로 dataset bias가 발생할 수 있음
- object transfer는 주로 geometrically similar rigid objects에 한정
- quasi-static manipulation 중심
- multi-arm manipulation은 지원하지 않음

---

## 11. Trade-offs

Human Data Collection vs Prior Knowledge
  - 
- human demonstrations는 크게 줄일 수 있음
- but 추가 정보 필요함
  - subtask structure
  - object pose

Simplicity vs Motion Quality
  - 
- simple transformation / interpolation은 구현과 scaling이 쉬움
- 하지만 collision 및 unnatural motion에 취약

Generation Success vs Diversity
  - 
- action noise는 generation success를 감소시킬 수 있음
- 반면 trajectory diversity를 높여 policy learning에는 도움이 될 수 있음

> 높은 generation success가 반드시 더 좋은 training data를 의미하지는 않음

Dataset Size vs Performance
  - 
- generated data가 많을수록 초기에는 성능이 크게 향상
- 일정 규모 이후 diminishing returns 발생

Online Generation vs Offline Augmentation
  - 
- Online:
  - physically consistent
  - environment interaction 필요
  - 생성 비용 증가

- Offline:
  - 빠르고 저렴
  - physical plausibility 보장 어려움

---

## 12. Key Findings

- 소수의 human demonstrations만으로 대규모 robot dataset을 생성할 수 있음
- 약 200개의 human demonstrations에서 50K+ demonstrations 생성
- small source dataset보다 MimicGen-generated dataset으로 학습한 policy가 크게 우수함
- 동일한 수의 human data와 MimicGen data가 comparable한 policy performance를 보일 수 있음
- source human demonstrations를 계속 늘리는 것이 항상 큰 성능 향상으로 이어지지는 않음
- generated dataset 역시 일정 규모 이후 diminishing returns가 존재
- narrow source distribution에서 broader initial-state distribution으로 data coverage를 확장할 수 있음
- demonstration behavior를 different objects 및 robot arms로 transfer할 수 있음
- data generation rate와 downstream policy performance는 반드시 비례하지 않음
- 단순한 dataset size보다 diversity와 coverage가 중요할 수 있음

---

## 13. Future Work / Open Challenges

- multi-object relational subtask 지원
- better interpolation 및 motion planning
- collision-aware trajectory generation
- generated data filtering 및 curation 개선
- dataset bias 감소
- more diverse object categories 지원
- deformable / soft object manipulation
- dynamic manipulation
- multi-arm manipulation
- improved mobile manipulation
- stronger Sim-to-Real transfer

Important question:

> 제한된 human demonstration budget을 기존 task의 추가 데이터에 사용할 것인가, 아니면 새로운 task / behavior / workspace region의 데이터를 수집하는 데 사용할 것인가?

---

## 14. My Takeaway

- MimicGen의 핵심은 새로운 policy architecture가 아니라 scalable robot data generation

- 기존 human demonstrations에 이미 존재하는 manipulation behavior를 새로운 context에 재사용할 수 있음

- 핵심 아이디어:
```
    Human Demonstrations
            +
    Object-Centric Transformation
            +
    Environment Interaction
            ↓
    Scalable Robot Data Generation
```
- Robot Learning에서는 model뿐만 아니라 dataset의 다음 특성도 매우 중요함
  - diversity
  - coverage
  - quality
  - composition

- 단순히 더 많은 human demonstrations를 모으는 것보다 기존 demonstration을 효과적으로 활용하는 data engine이 중요할 수 있음

---

## 15. Connection to My Research

Possible research pipeline:
  -
```
    VR / Real Teleoperation
            ↓
    Small Human Demonstration Dataset
            ↓
    Simulation-Based Data Generation
            ↓
    Large and Diverse Robot Dataset
            ↓
    Imitation Learning
            ↓
    Diffusion Policy / VLA
            ↓
    Real Robot
```
- VR teleoperation data를 최종 대규모 training dataset 자체로 보기보다 scalable data generation을 위한 seed data로 사용할 수 있음
- simulation에서 human behavior를 확장한 뒤 real robot policy learning으로 연결할 수 있음

Potential Questions:
  -
- object-centric subtask와 trajectory segmentation을 자동으로 학습할 수 있는가?
- ground-truth object pose dependency를 줄일 수 있는가?
- 어떤 generated trajectory가 downstream policy learning에 실제로 유용한가?
- novelty / uncertainty / diversity를 이용해 generated data를 선택하거나 weighting할 수 있는가?
- simulation-generated data와 real teleoperation data를 어떻게 조합해야 real robot generalization을 높일 수 있는가?

---
## 16. Appendix: Section Notes

<details>
<summary>Section-by-Section Reading Notes</summary>

### Section 1. Introduction

- human demonstrations are costly and time-consuming
- large robot datasets에는 반복적인 manipulation behavior가 많이 포함될 수 있음

> How much of this data actually contains unique manipulation behaviors?

- MimicGen:
  - small human demonstrations
  - object-centric segmentation
  - spatial transformation
  - segment stitching
  - environment execution
  - successful demonstration collection

- 50K+ demonstrations
- 18 tasks
- ~200 source human demonstrations

### Section 2. Related Work

- 관련 data collection approaches:
  - trial-and-error
  - simulation demonstrators
  - large-scale human teleoperation
  - offline data augmentation
  - replay-based Imitation Learning

- MimicGen은 replay mechanism을 final policy가 아니라 data generation mechanism으로 사용
- offline augmentation과 달리 environment interaction을 통해 새로운 trajectory를 생성

### Section 3. Problem Setup

- robot manipulation task를 MDP로 표현

- Behavioral Cloning:

      s → a

- Goal:

      small D_src
          ↓
        MimicGen
          ↓
      large D

- Assumption 1: delta end-effector pose action space
- Assumption 2: known sequence of object-centric subtasks
- Assumption 3: object pose available at the beginning of each subtask during data generation

### Section 4. Method

#### 4.1 Parsing

    τ = (τ1, τ2, ..., τM)

- human trajectory를 object-centric segments로 분해

#### 4.2 Transformation

각 subtask:

    Select Segment
        ↓
    Transform using Object Pose
        ↓
    Interpolate
        ↓
    Execute

- absolute trajectory가 아니라 object-relative motion을 보존
- 모든 subtask 수행 후 성공한 demonstration만 저장

### Section 5. Experiment Setup

- most tasks:
  - 10 source human demonstrations
  - 1000 generated demonstrations per task variant

- environments:
  - robosuite / MuJoCo
  - Factory / Isaac Gym

- policy:
  - BC-RNN

### Section 6. Experiments

- source dataset 대비 MimicGen dataset에서 큰 policy improvement
- broader initial state distribution 지원
- object transfer 가능
- robot transfer 가능
- different demonstrators에도 비교적 robust
- 200 MimicGen demos가 200 human demos와 comparable
- generated dataset 증가에는 diminishing returns 존재
- data generation rate와 policy performance는 반드시 비례하지 않음
- real robot에서도 data generation 가능하지만 policy performance는 simulation보다 낮음

### Section 7. Limitations

- known subtask sequence 필요
- object pose 필요
- one reference object per subtask
- naive interpolation
- collision-free guarantee 없음
- generated data bias 가능
- rigid / quasi-static task 중심
- multi-arm 미지원

### Section 8. Conclusion

- MimicGen은 적은 human data를 large-scale robot learning dataset으로 확장하는 방법을 제시
- generated data는 추가 human demonstration을 직접 수집하는 것과 경쟁력 있는 성능을 보임
- human effort를 반복적인 behavior 수집보다 새로운 task, behavior, workspace region을 수집하는 데 사용하는 것이 더 효율적일 수 있음

> MimicGen motivates a more data-centric perspective on Imitation Learning.

</details>