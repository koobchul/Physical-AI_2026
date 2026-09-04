# VLA Survey

## 0. Paper Information

- Title: Vision-Language-Action in Robotics: A Survey of Datasets. Benchmarks, and Data Engines
- Authors: Ziyao et. al
- Year: 2026
- Paper: TMLR 2026
- Code: 
- Project:

---

## Chapter 0. Abstract

### Overview

- VLA를 model-centric이 아닌 data-centric 관점에서 분석
- 핵심 축: Datasets, Benchmarks, Data Engines

### Key Concepts

### Taxonomy

- Datasets
  - 
  - Embodiment Diversity
  - Modality Composition
  - Action Space Formulation

- Benchmarks
  - 
  - Task Complexity
  - Environment Structure

- Data Engines
  - 
  - Simulation-based
  - Video Reconstruction
  - Automated Task Generation

### Strengths / Pros

- VLA 연구를 model architecture가 아닌 data infrastructure 관점에서
  체계적으로 분석
- Datasets, Benchmarks, Data Engines를 하나의 framework 안에서 연결

### Limitations / Cons

- Embodied Learning의 근간이 되는 data infrastructure는
  기존 VLA 연구에서 상대적으로 충분히 검토되지 않음
- 기존 benchmarks가 compositional generalization과
  long-horizon reasoning을 충분히 평가하지 못함
- Data engines는 physical grounding 및 sim-to-real transfer에 한계가 있음

### Trade-offs

- Fidelity <-> Cost
  - Real-world data는 fidelity가 높지만 수집 비용이 큼
  - Synthetic data는 대규모 생성에 유리하지만 현실성과 transfer에 한계가 있음

### Key Findings

- VLA 발전의 핵심 병목은 model architecture뿐 아니라 data infrastructure와 evaluation에도 존재

### Important Models / Datasets / Methods

### Future Work / Open Challenges

- Representation Alignment
- Multimodal Supervision
- Reasoning Assessment
- Scalable Data Generation

### My Takeaway

- 앞으로 VLA 성능 향상에는 데이터 품질·생성·평가 체계가 핵심이 될 수 있음.

---

# Chapter 1. Introduction

### Key Concepts

- VLA:
  visual observations + language instructions -> actions

- Generalization:
  objects, environments, task variations에 걸쳐 동작하는 능력

- Robot Demonstration:
  human demonstrations를 이용하여 action policy를 학습하기 위한 데이터

- Sim-to-Real:
  simulation에서 학습한 policy를 real-world robot에 transfer하는 방법


### Taxonomy

- Datasets
  - 
  VLA model 학습을 위한 curated demonstrations
  - Synthetic datasets
  - Real-world datasets

- Benchmarks
  - 
  performance와 generalization을 평가하기 위한
    standardized evaluation protocols, task settings, metrics
  - Task settings
  - Episode horizon
  - Task complexity

- Data Engines
  - 
  VLA training data를 collect, generate, augment하기 위한 scalable system/pipeline
  - Video-to-data pipelines
  - Hardware-assisted data collection systems
  - Generative data engines

### Strengths / Pros

- VLA는 visual observation과 language instruction을 직접 action으로 mapping 가능
- 기존 fixed-task manipulation system과 달리
  object / environment / task variation에 대한 generalization을 목표로 함
- Datasets, Benchmarks, Data Engines의 3-way taxonomy를 통해
  각 요소의 역할과 design choice를 체계적으로 비교 가능

### Limitations / Cons

- Reliable VLA system 구축은 여전히 어려움
- Real-world demonstration은 수집 비용이 높고
  task/environment coverage가 제한적
- Synthetic / simulation data는 scalable하지만
  real-world conditions를 충분히 반영하지 못할 수 있음
- Scene, robot, task가 바뀌면 성능이 저하될 수 있음
- Standardized evaluation protocol이 부족함
- 논문마다 task definition, success criteria, data split이 달라
  method 간 비교가 어려움
- 성능 향상이 genuine generalization인지 판단하기 어려움

### Trade-offs

- Real-world Data
  - High physical realism
  - High collection cost / limited scale

- Synthetic / Simulation Data
  - High scalability
  - Lower physical realism / Sim-to-Real gap


### Key Findings

- VLA의 핵심 병목이 model design만의 문제가 아니라
  data와 evaluation의 문제로 이동하고 있음

- Three structural challenges:
  1. Representation alignment across embodiments
  2. Reliable evaluation of long-horizon compositional tasks
  3. Scalable data generation that preserves physical realism

### Important Models / Datasets / Methods

- Imitation Learning
- Robot Demonstration
- Sim-to-Real Transfer
- VLM backbone


### Future Work / Open Challenges

- Representation alignment across different embodiments
- Long-horizon compositional task evaluation
- Scalable data generation while preserving physical realism
- Standardized VLA evaluation protocols
- Better generalization across robots, scenes, and tasks

### My Takeaway

- VLA는 단순히 Vision + Language를 Action으로 연결하는 모델 문제가 아니라,
  robot data를 어떻게 수집하고 평가할 것인지가 핵심 문제다.
- 특히 real-world data는 품질이 좋지만 비싸고,
  simulation은 scalable하지만 physical realism과 Sim-to-Real 문제가 있다.
- 따라서 앞으로 VLA 연구에서는 Model뿐 아니라
  Dataset + Benchmark + Data Engine을 함께 보는 것이 중요하다.

# Chapter 2. Preliminaries

### Key Concepts

- Survey Scope
  - Robotic Manipulation에 초점
  - Robot arm + optionally gripper
  - Autonomous driving / navigation은 제외

- VLA as Sequential Decision-Making
  - a_t = π(o_t, l)

  - Visual observation o_t
    - RGB image
    - RGB-D / Point Cloud
    - Video sequence

  - Language instruction l
    - High-level task goal
    - 일반적으로 episode 동안 고정

  - Action a_t
    - Robot control command

- VLA Benchmark
  - trained policy를 predefined tasks / environments에서 평가
  - 주요 metric: Success Rate (SR)

- Data Engine
  - fixed/static dataset과 달리,
    training data를 continuously generate / transform / augment하는 pipeline
  - 새로운 embodiment, task, environment에 맞춰
    data diversity를 확장하는 것이 목적

### Taxonomy

Action Representation
  - 
- Control Target
  - End-Effector (EEF) Space
    - Cartesian position + orientation
  - Joint (DoF) Space
    - Individual joint states를 직접 제어

- Parameterization
 - Absolute Action
    - chosen action space에서 target state 지정
  - Relative / Delta Action
    - 현재 state에 대한 incremental change


Benchmarks
 - 
- Task Structure
  - Short-horizon atomic manipulation
  - Long-horizon compositional task

- Environment Structure
  - Constrained tabletop
  - Diverse multi-scene environments


Data Engines
 - 
- Video-to-Data Engines
  - Human video → robot-executable supervision

- Hardware-Assisted Engines
  - Teleoperation / sensing interface를 통해 demonstration 수집

- Generative Data Engines
  - Simulation / generative model을 이용하여
    task, trajectory, environment 생성


### Strengths / Pros

### Limitations / Cons

### Trade-offs

### Key Findings

### Important Models / Datasets / Methods

- Figure 1은 2023–2025 VLA data-centric works의 전체 landscape를 보여줌
- 개별 모델/데이터셋은 이후 Chapter에서 자세히 정리

### Future Work / Open Challenges

### My Takeaway

- 이 논문에서 VLA는 단순한 multimodal model이 아니라
  visual observation + language instruction을 robot action으로 mapping하는
  sequential decision-making problem으로 정의됨.
- 특히 Action Space는
  `EEF vs Joint`와 `Absolute vs Delta`라는 서로 다른 두 축으로 구분됨.
- Data Engine은 한번 만들어 놓는 Dataset과 달리
  지속적으로 robot data를 생성·변환·확장하는 시스템이라는 점이 핵심.

# Chapter 3. VLA Datasets

### Key Concepts

- Datasets
  - 
  - Real-world datasets
  - Synthetic datasets

analyze differences in embodiment diversity, action representation, and modalities

### Taxonomy

### Strengths / Pros

### Limitations / Cons

### Trade-offs

### Key Findings

### Important Models / Datasets / Methods

### Future Work / Open Challenges

### My Takeaway


# Chapter 3.1 Real-World Datasets

### Key Concepts

- high quality but also high cost

### Taxonomy

### Strengths / Pros

### Limitations / Cons

- difficult to scale due to substantial human labor requirments and infrastructure expenses

### Trade-offs

### Key Findings

### Important Models / Datasets / Methods

- Open X-Embodiment (Padalkar et al., 2023)
  - 
  most widely used pretraining datasets for VLA
- RT-1 (Brohan et al., 2022)
  - 
  emphasize data hygiene and consistency

- BridgeData V2 (Walke dt al., 2023)
  - 
  emphasize data hygiene and consistency

- DROID (Khazatsky et al., 2024)
  - 
  increases visual and environmental variation to enhance preceptual robustness under real-world conditions

- RH20T (Fang et al., 2023)
  - 
  multimodal datasets
  
  incorporate tactile/force and audio signals, which are particularly beneficial for contact-rich manipulation where vision alone may be insufficient

- RT-2-style co-training (Brohan et al., 2023)
  - 

- Ego4D (Grauman et al., 2022) 
  - 
  human video corpora 
### Future Work / Open Challenges

### My Takeaway