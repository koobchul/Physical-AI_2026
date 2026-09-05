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

---
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

---
# Chapter 3. VLA Datasets

### Key Concepts

- VLA Dataset
  - 
  VLA model의 training material로 사용됨\
  embodiment, environment generalization에 직접적인 영향을 줌.

### Taxonomy

- Data Source
  - 
  - Real-World Datasets
  - Synthetic Datasets

- Comparison Axes
  - 
  - Embodiment Diversity
  - Action Representation
  - Modalities

### Strengths / Pros

### Limitations / Cons

### Trade-offs

- Fidelity ↔ Cost / Scalability

### Key Findings

- Dataset choice는 원하는 generalization objective와 deployment setting에 따라 달라져야 함.

### Important Models / Datasets / Methods

### Future Work / Open Challenges

### My Takeaway

- VLA dataset은 단순히 데이터 양이 아니라 어떤 robot / modality / action space를 포함하는지가 중요함.

---
# Chapter 3.1 Real-World Datasets

### Key Concepts

- high quality but also high cost

### Taxonomy

### Strengths / Pros

- 실제 contact dynamics와 friction을 반영
- Real image / authentic robot state / action 제공
- Simulation에서 재현하기 어려운 physically grounded signal 포함
- 높은 physical fidelity

### Limitations / Cons

- Human labor와 physical infrastructure가 필요하여 collection cost가 높음
- Large-scale collection이 어려움
- 특정 robot / task / environment에 coverage가 제한될 수 있음

### Trade-offs

- High Fidelity ↔ High Cost
- Data Quality ↔ Scalability

### Key Findings

- Cross-embodiment pretraining / large-scale transfer
  → Open X-Embodiment

- Specific robot fine-tuning
  → RT-1 / DROID / BridgeData V2

- Environmental robustness
  → DROID

- Contact-rich manipulation
  → RH20T

- Semantic knowledge transfer
  → RT-2 / Ego4D

### Important Models / Datasets / Methods

- Open X-Embodiment (Padalkar et al., 2023)
  - 
  most widely used pretraining datasets for VLA
- RT-1 (Brohan et al., 2022)
  - 
  - emphasize data hygiene and consistency
  - single-embodiment datasets

- BridgeData V2 (Walke dt al., 2023)
  - 
  - emphasize data hygiene and consistency
  - single-embodiment datasets


- DROID (Khazatsky et al., 2024)
  - 
  - increases visual and environmental variation to enhance preceptual robustness under real-world conditions
  - single-embodiment datasets
  - robustness to environmental variation is reuqired, distributed real-world collections provide diverse lighting and scene configurations


- RH20T (Fang et al., 2023)
  - 
  - multimodal datasets
  - incorporate tactile/force and audio signals, which are particularly beneficial for contact-rich manipulation where vision alone may be insufficient
  - contact-rich manipulation tasks
  - offer additional tactile or force signals that complement vision

- RT-2 (Brohan et al., 2023)
  - 
  - web-co-trained or human-centric sources
  - transferring semantic knowledge from large-scale human data is beneficial 


- Ego4D (Grauman et al., 2022) 
  - 
  - human video corpora 
  - web-co-trained or human-centric sources


### Future Work / Open Challenges

- Low-cost acquisition of high-quality real-world data
- Real-world data collection의 scalability 향상

### My Takeaway

- Real-world data는 physical fidelity가 높지만 수집 비용 때문에 scale 확보가 어렵다.
- 따라서 deployment 대상 robot과 generalization 목표에 따라 dataset을 선택해야 한다.

# Chapter 3.2 Synthetic Datasets

### Key Concepts

- synthetic data is significantly more scalable and cost-effective, it often exhibits lower realism compared to real-world datasets
- common strategy for synthetic data generation is procedural randomization within simulation environments
- synthetic data is frequently used to bootstrap policies before subsequent calibration with real-world data
- synthetic data is typically used for large-scale pretraining or augmentation. with real-world data required for final calibration and deployment

### Taxonomy

- Procedural Randomization
  - SynGrasp-1B / GraspVLA

- Simulation Environment / Rollout
  - RoboCasa

- Automated Task Generation
  - RoboGen

- Demonstration Augmentation
  - MimicGen

### Strengths / Pros

- Real-world data보다 scalable하고 cost-effective
- Trajectory 수를 쉽게 증가시킬 수 있음
- Scene configuration을 다양하게 변경 가능
- Task success / failure를 simulator에서 자동 판정 가능
- Human demonstration을 augmentation하여 dataset size를 확장 가능

### Limitations / Cons

- Rendering artifact로 인해 real image와 차이가 발생
- Contact / friction 등의 physical dynamics 재현이 부정확할 수 있음
- Simulator의 physical realism에 fidelity가 제한됨
- Generated grasp pose / task가 physically implausible할 수 있음
- Sim-to-Real gap 존재

### Trade-offs

- Scalability ↔ Fidelity
- Low Cost ↔ Physical Realism

### Key Findings

- Synthetic data는 large-scale pretraining / augmentation에 적합
- 그러나 final deployment를 위해서는 real-world calibration이 주로 필요
- Synthetic data alone보다는
  Synthetic Pretraining → Real-world Calibration 구조가 현실적

### Important Models / Datasets / Methods

- GraspVLA (Deng et al., 2025)
  - 
  large-scale synthetic grasp dataset SynGrasp1B
  
  SynGrasp1B 
  - 
  - Billion-scale synthetic robotic grasping dataset
  - 10,000+ objects / 240 categories
  - Simulation에서 grasp poses와 trajectories를 자동 생성
  - Extensive domain randomization 사용
  - 장점: 매우 scalable하고 real-world collection cost가 없음
  - 핵심 문제: Sim-to-Real / physical realism

- RoboCasa (Nasiriany et al., 2024)
  - 
  - Simulator-based household manipulation environment
  - Diverse kitchen environments
  - Asset libraries
  - Structured task suites
  - Large-scale synthetic rollout / demonstration collection 

- RoboGen (Wang et al., 2024c)
  - 
  - LLM으로 task proposal
  - Simulation code 자동 생성
  - Manual task authoring 감소
  - Task diversity 확장

- MimicGen (Mandlekar et al., 2023)
  - 
  - further scale simulator data 
  - preturbing object poses and initial condition from a small set of human seed demonstrations
  - increasing dataset size while preserving underlying task structure
  - augmentation method
  - scale limited human demonstrations within simulation by perturbing object configurations and initial conditions

- VLA finetuning datasets
    - 
    - LIBERO (Liu et al.2023)
    - CALVIN (Meeset al., 2022)
    - Meta-World (Yu et al., 2021)
    - RLBench (James et al., 2020)
    - BEHAVIOR-1K (Li et al., 2024a)
    - VLABench (Zhang et al., 2024b) 



### Future Work / Open Challenges

- Improve physical realism of simulation
- Reduce Sim-to-Real gap
- Generate more physically plausible trajectories / grasp poses
- Better validation and filtering of automatically generated data

### My Takeaway

- Synthetic data는 대규모 VLA pretraining을 가능하게 하지만
  physical realism과 Sim-to-Real 문제가 핵심 한계다.
- 따라서 synthetic data로 scale을 확보하고,
  real-world data로 최종 calibration하는 전략이 중요하다.


---

# Chapter 4. VLA Benchmarks

### Key Concepts

- VLA Benchmark
  - VLA model의 performance와 generalization ability를 평가하기 위한 evaluation dataset
  - representative tasks + well-defined evaluation metrics로 구성

- Two Analytical Dimensions
  - Task Complexity
    - manipulation objective의 compositional / temporal difficulty
  - Environment Structure
    - scene diversity / spatial variability

- Benchmark는 evaluation protocol뿐 아니라
  training/testing split을 가진 structured data resource로도 사용될 수 있음

### Taxonomy

- Task Complexity
  - Simple / Short-horizon
  - Complex / Long-horizon compositional

- Environment Structure
  - Table-top
  - Multi-scene

### Strengths / Pros

- standardized comparison 가능
- 어떤 VLA capability를 benchmark가 강조하는지 체계적으로 비교 가능
- controlled train/test split을 통해 learning / transfer ability 평가 가능

### Limitations / Cons

- Real-robot evaluation은 costly하고 operationally complex
- Task complexity와 environment structure가 동시에 변하는 경우가 많음
- Perception / language grounding / control이 tightly coupled되어
  failure attribution이 어려움

### Trade-offs

- Controlled / Simple Environment
  ↔ Realistic / Diverse Environment

- Evaluation Interpretability
  ↔ Task & Environment Complexity

### Key Findings

- VLA benchmark difficulty는 task complexity와
  environment structure를 함께 고려해야 함
- 두 요소가 동시에 변하면 multiple difficulty sources가 entangled됨
- True generalization이 어렵기 때문에 많은 benchmark가
  explicit training / testing split을 제공

### Important Models / Datasets / Methods

- LIBERO (Liu et al., 2023)
- Meta-World (Yu et al., 2021)

simulator-based suites 

### Future Work / Open Challenges

### My Takeaway

---
# Chapter 4.1 Table-top Benchmarks

### Key Concepts

- evaluate VLA models under constrained table-top tasks

- most common tasks that are clean enough

- simple short-horizon tasks
  - 
  include benchmarks that focus on atomic manipulation tasks executed within short action horizons under constrained table-top environments

  - Meta-World (Yu et al., 2021)
    - 
    comprises 50 simple manipulation tasks\
    simplify visual perception and scene understanding

  - LIBERO (Liu et al., 2023)
    - 
    most tasks correspind to atomic skills \
    completed within limited steps \
    - LIBERO-plus (Fei et al., 2026)
    - LIBERO-PRO (Zhou et al., 2025)
    - LIBERO-X (Wang et al., 2026)

  - SimplerEnv (Lu et al., 2024b)
    - 
    evaluates policies on short-horizon table-top manupulation tasks \
    deliberately maintains environments that are only sufficiently realistic to preserve sim-to-real ranking consistency

  - RoboChallenge (Yakefu et al., 2025) 
    - 
    - provide a real-world table-top robotic platform
    
- complex long-horizon tasks
  - 
  generating compositional tasks while maintaining a simplified interaction setting

  - CALVIN (Mees et al., 2022)
    - 
    reuqiting agents to execute extended sequences of unconstrained language instructions across multiple tabletop environments\
    most challenging protocol requiring zero-shot generalization to an unseen environment\
    isolating sustained grounding and temporal credit assignment as primary challenges

  - GemBench (Garcia et al., 2025)
    -
    systematically assessing hierarchicl generalization across novel objet placements, unseen instances, and compositional long-hosizon tasks within the RLBench simulator 

  - COLOSEUM (Pumacay et al., 2024)
    - 
    evaluates robustness under controlled table-top settings by introducing systematic visual and physical perturbations across 14 axes\
    demonstrating significant degradation when multiple perturbation factors are applied simultaneously

  emphasize reasoning difficulty, compositional grounding, and robustness under controlled environmental conditions rathe than expanding environment scale or visual diversity

### Taxonomy

- Simple Short-horizon
  - Meta-World
  - LIBERO
  - SimplerEnv
  - RoboChallenge

- Complex Long-horizon / Compositional
  - CALVIN
  - GemBench
  - COLOSSEUM

### Strengths / Pros

- 환경이 constrained되어 evaluation reproducibility가 높음
- Real-world에서도 비교적 reproduction이 쉬움
- Immediate action correctness와 low-level control stability 평가에 적합
- 환경 변수를 제한하여 reasoning / grounding 문제를 더 분리해서 관찰 가능

### Limitations / Cons

- Simple benchmark는 long-horizon reasoning을 충분히 stress하지 못함
- Complex environmental variation이 제한적
- 실제 open-world environment를 완전히 반영하지 못함

### Trade-offs

- Simplicity / Reproducibility
  ↔ Environmental Realism / Diversity

### Key Findings

- Short-horizon 성능이 좋아도 long-horizon task에서는 성능이 크게 저하될 수 있음
- Instruction chain이 길어질수록 sustained grounding과 temporal reasoning이 어려워짐
- Multiple perturbation이 동시에 적용되면 robustness가 크게 감소

### Important Models / Datasets / Methods

### Future Work / Open Challenges

### My Takeaway

---

# Chapter 4.2 Multi-scene Benchmarks

### Key Concepts

- aim to evaluate embodied angents under substantially more complex task and environment conditions

- emphasize interaction across diverse scenes, long-horizon execution, and compositional reasoning, reflecting a shift toward more realistic and semantically rich embodied tasks

- BEHAVIOR-1K (Li et al., 2024a)
  - 
  evaluates everyday human activities that unfold over long durations and require coordination of multiple manipulation skills\
  spans full-room and multi-room environments and supports realistic physical interactions involving rigid objects, deformable materials, and fluids

- VLABench (Zhang et al., 2024b)
  - 
  increases task complexity by constructing composite language-conditioned tasks that intergrate multiple skills with long-horizion multi-step reasoning and intermediate reasoning grounded inscene semantics

- Open X-Embodiment (O'Neill et al., 2025)
  - 
  adopts a complementary scale-driven perspective by aggeragting data from heterogeneous real-world robots and environments, emphasizing behaviroal breadth and cross-embodiment transfer\
  rather than enforcing a unified task structure or explictly designed long-horizion objectives

difficulty arises from the joing expansion of task horizon and environmental varibaility, stressing compositional reasoning, robustness, and generalization across scencs and embodiments

### Taxonomy

- Long-horizon Everyday Activities
  - BEHAVIOR-1K

- Compositional Language-conditioned Tasks
  - VLABench

- Scale / Cross-Embodiment Generalization
  - Open X-Embodiment

### Strengths / Pros

- Diverse scenes와 realistic interaction 평가 가능
- Long-horizon execution 평가 가능
- Compositional reasoning과 semantic grounding 평가 가능
- Cross-scene / cross-embodiment generalization 평가에 유리

### Limitations / Cons

- Task horizon과 environment variability가 동시에 증가하여
  failure attribution이 더 어려움
- Evaluation complexity와 computational / operational cost가 증가
- 서로 다른 benchmark 간 difficulty를 직접 비교하기 어려울 수 있음

### Trade-offs

- Realism / Diversity
  ↔ Interpretability / Controlled Evaluation

### Key Findings

- Multi-scene benchmark의 difficulty는
  task horizon + environmental variability의 동시 증가에서 발생
- VLA가 compositional reasoning, robustness,
  cross-scene / cross-embodiment generalization을 동시에 요구받음

### Important Models / Datasets / Methods

### Future Work / Open Challenges

- Long-horizon compositional reasoning 평가 개선
- Scene / embodiment variation에 대한 robust generalization
- 복잡한 benchmark에서도 failure source를 분리할 수 있는 evaluation design

### My Takeaway

- Multi-scene benchmark는 실제 환경과 더 가까운 VLA 능력을 평가할 수 있지만,
  task complexity와 environment variability가 동시에 증가해
  실패 원인 분석이 어려워진다.

---

# Chapter 5. VLA Data Engines

### Key Concepts

- VLA data engine
  - 
  scalable system or pipeline designed to continuously generate, transform, or augment training data for VLA model

### Taxonomy

- 

### Strengths / Pros

- 

### Limitations / Cons

- 

### Trade-offs

- 

### Key Findings

- 

### Important Models / Datasets / Methods

### Future Work / Open Challenges

- 

### My Takeaway

---

# Chapter 

### Overview

- 

### Key Concepts

### Taxonomy

- 

### Strengths / Pros

- 

### Limitations / Cons

- 

### Trade-offs

- 

### Key Findings

- 

### Important Models / Datasets / Methods

### Future Work / Open Challenges

- 

### My Takeaway
