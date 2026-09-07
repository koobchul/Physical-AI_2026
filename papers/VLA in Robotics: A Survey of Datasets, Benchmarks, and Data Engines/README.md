# Vision-Language-Action in Robotics: A Survey of Datasets, Benchmarks, and Data Engines

## 0. Paper Information

- Title: Vision-Language-Action in Robotics: A Survey of Datasets, Benchmarks, and Data Engines
- Authors: Ziyao Wang et al.
- Year: 2026
- Venue: TMLR 2026
- Paper:
- Code: https://github.com/ziyaow1010/vla-datasets-benchmarks
- Project:

---

## 1. One-line Summary

> VLA research를 Dataset, Benchmark, Data Engine의 세 축으로 분석하고, model architecture보다 data infrastructure와 evaluation이 앞으로의 핵심 병목이 될 수 있음을 제시한 data-centric survey.

---

## 2. Why this Paper?

### Problem

- 기존 VLA 연구는 model architecture 중심으로 발전해 왔지만, embodied learning을 뒷받침하는 data infrastructure에 대한 체계적인 분석은 부족함.
- Real-world data는 고품질이지만 수집 비용이 크고, synthetic data는 scalable하지만 physical realism과 sim-to-real 문제가 존재함.
- Benchmark마다 task, metric, evaluation protocol이 달라 genuine generalization을 비교하기 어려움.

### Motivation

- VLA의 real-world generalization을 위해서는 model뿐 아니라 training data, evaluation, scalable data generation을 함께 고려해야 함.
- Dataset, Benchmark, Data Engine을 하나의 framework 안에서 분석할 필요가 있음.

### Main Contribution

1. Dataset / Benchmark / Data Engine의 unified data-centric taxonomy 제시
2. Dataset을 embodiment, modality, action representation 관점에서 비교
3. Benchmark를 task complexity × environment structure의 두 축으로 분석
4. Data Engine을 Video-to-Data / Hardware-Assisted / Generative로 분류
5. VLA data infrastructure의 주요 한계와 future direction 정리

---

## 3. Key Concepts

### VLA

Vision-Language-Action model은 visual observation과 language instruction을 robot action으로 mapping한다.

```text
Vision + Language
       ↓
      VLA
       ↓
     Action
```

Sequential decision-making 관점에서는:

```text
a_t = π(o_t, l)
```

- `o_t`: visual observation
  - RGB
  - RGB-D / point cloud
  - video
- `l`: language instruction
  - high-level task goal
  - generally fixed during an episode
- `a_t`: robot control action

### Embodiment

Robot의 physical body / hardware configuration.

서로 다른 embodiment는 robot morphology, joint structure, action interface 등이 다르기 때문에 cross-embodiment learning에서 alignment 문제가 발생한다.

### Action Representation

```text
Action
├── Control Target
│   ├── End-Effector (EEF)
│   └── Joint / DoF
│
└── Parameterization
    ├── Absolute
    └── Relative / Delta
```

- EEF: Cartesian position + orientation을 제어
- Joint / DoF: individual joint states를 직접 제어
- Absolute: target state를 직접 지정
- Delta: 현재 state에 대한 incremental change

### Sim-to-Real

Simulation에서 학습하거나 생성한 knowledge / policy를 real-world robot으로 transfer하는 과정.

### Grounding

Language, vision, predicted states, actions를 실제 physical object / state / robot behavior와 올바르게 연결하는 것.

---
## 4. Taxonomy / Method

이 논문의 전체 구조는 세 가지 data infrastructure component로 정리된다.

```text
VLA Data Infrastructure
│
├── Dataset
│   ├── Real-World
│   └── Synthetic
│
├── Benchmark
│   ├── Table-top
│   └── Multi-scene
│
└── Data Engine
    ├── Video-to-Data
    ├── Hardware-Assisted
    └── Generative
```

### Dataset Comparison Axes

- Embodiment Diversity
- Modality Composition
- Action Space Formulation

### Benchmark Analysis Axes

```text
Task Complexity
Simple → Complex / Long-horizon

Environment Structure
Table-top → Multi-scene
```

### Data Engine Taxonomy

```text
Data Engine
├── Video-to-Data
├── Hardware-Assisted
└── Generative
```

---

## 5. Important Models / Datasets / Methods

### 5.1 Real-World Datasets

| Dataset | Main Role |
|---|---|
| Open X-Embodiment (Padalkar et al., 2023) | Cross-embodiment aggregation and pretraining |
| RT-1 (Brohan et al., 2022) | Single-embodiment, consistent robot data |
| RT-2 (Brohan et al., 2023) | Web knowledge + robot control co-training |
| DROID (Khazatsky et al., 2024) | Diverse in-the-wild real-world collection |
| BridgeData V2 (Walke et al., 2023) | Standardized low-cost robot dataset |
| RH20T (Fang et al., 2023) | Tactile / force / audio multimodal data |
| Ego4D (Grauman et al., 2022) | Large-scale human interaction video |

### 5.2 Synthetic Datasets

| Dataset / Method | Main Role |
|---|---|
| SynGrasp-1B / GraspVLA (Deng et al., 2025) | Billion-scale synthetic grasp pretraining |
| RoboCasa (Nasiriany et al., 2024) | Household manipulation simulation |
| RoboGen (Wang et al., 2024c) | LLM-based automated task generation |
| MimicGen (Mandlekar et al., 2023) | Demonstration augmentation |

### 5.3 Benchmarks

#### Table-top

| Benchmark | Main Focus |
|---|---|
| Meta-World (Yu et al., 2021) | Simple atomic manipulation |
| LIBERO (Liu et al., 2023) | Short-horizon language-conditioned tasks |
| SimplerEnv (Li et al., 2024b) | Sim-to-real policy evaluation |
| RoboChallenge (Yakefu et al., 2025) | Real-world table-top evaluation |
| CALVIN (Mees et al., 2022) | Long-horizon language-conditioned manipulation |
| GemBench (Garcia et al., 2025) | Hierarchical / compositional generalization |
| COLOSSEUM (Pumacay et al., 2024) | Robustness under visual and physical perturbations |

#### Multi-scene

| Benchmark | Main Focus |
|---|---|
| BEHAVIOR-1K (Li et al., 2024a) | Long-horizon everyday activities |
| VLABench (Zhang et al., 2024b) | Multi-step compositional reasoning |
| Open X-Embodiment (O'Neill et al., 2025) | Cross-embodiment behavioral diversity |

### 5.4 Video-to-Data Engines

| Method | Main Idea |
|---|---|
| H2R (Li et al., 2026) | Human hand pose → robot motion retargeting |
| RoboWheel (Zhang et al., 2025b) | Physics-aware cross-embodiment retargeting |
| Video2Policy (Ye et al., 2025) | Video reconstruction + GPT-4o task code generation |
| X-Humanoid (Yang et al., 2025) | Human video → humanoid demonstration |
| GenMimic (Ni et al., 2025) | Generated human video → robot trajectory |
| UniSim (Yang et al., 2024) | Interactive video world model |

### 5.5 Hardware-Assisted Engines

| Method | Main Idea |
|---|---|
| ALOHA (Zhao et al., 2023) | Low-cost bimanual teleoperation |
| GELLO (Wu et al., 2024) | Low-cost 3D-printed teleoperation interface |
| UMI (Chi et al., 2024) | GoPro gripper + SLAM for in-the-wild collection |
| DexCap (Wang et al., 2024a) | EMF gloves + RGB-D for dexterous manipulation |
| Lucid-XR (Ravan et al., 2025) | VR physics simulation + diffusion rendering |

### 5.6 Generative Data Engines

```text
Generative Data Engine
│
├── Trajectory Reuse
│   ├── MimicGen (Mandlekar et al., 2023)
│   ├── DynaMimicGen (Pomponi et al., 2025)
│   └── DemoGen (Xue et al., 2025)
│
├── LLM-driven Generation
│   ├── GenSim (Wang et al., 2024b)
│   ├── RoboGen (Wang et al., 2024c)
│   └── RoboTwin 2.0 (Chen et al., 2025)
│
├── Visual Augmentation
│   ├── ROSIE (Yu et al., 2023)
│   ├── RoboEngine (Yuan et al., 2025)
│   └── EMMA (Dong et al., 2025)
│
└── Predictive World Models
    ├── PointWorld (Huang et al., 2026)
    ├── IRASim (Zhu et al., 2025)
    ├── 3D-VLA (Zhen et al., 2024)
    └── Genie (Bruce et al., 2024)
```

---

## 6. Strengths

- VLA를 model-centric이 아니라 data-centric perspective에서 체계적으로 정리
- Dataset, Benchmark, Data Engine을 하나의 framework 안에서 연결
- Data source뿐 아니라 embodiment, modality, action representation까지 함께 고려
- Benchmark difficulty를 task complexity와 environment structure로 분리하여 분석
- Data generation scalability와 physical grounding 사이의 문제를 명확하게 제시
- VLA 분야 전체의 dataset / benchmark / data engine landscape를 빠르게 파악하기 좋음

---

## 7. Limitations

### Survey Scope

- Robotic manipulation에 초점을 맞춤
- Autonomous driving / navigation은 제외
- 주로 robot arm과 gripper 기반 manipulation을 다룸

### Taxonomy Overlap

Dataset, Benchmark, Data Engine의 역할은 실제 연구에서는 완전히 분리되지 않는다.

- LIBERO, CALVIN, Meta-World 등은 benchmark이면서 training data로도 사용
- MimicGen은 synthetic dataset 생성 방식이면서 data engine 역할도 수행

### Field-level Limitations Identified by the Survey

```text
Dataset
└── Fidelity–Cost Trade-off

Benchmark
└── Insufficient Reasoning Evaluation

Data Engine
└── Scaling Generation Without Scaling Grounding
```

---

## 8. Trade-offs

### Dataset

```text
Real-World Data
  High Fidelity
        ↕
  High Cost / Limited Scale

Synthetic Data
  High Scalability
        ↕
  Lower Physical Realism
```

### Cross-Embodiment Data

```text
Embodiment Diversity
        ↕
Interface Consistency
```

### Benchmark

```text
Controlled / Reproducible
          ↕
Realistic / Diverse
```

### Hardware-Assisted Collection

```text
Precision
    ↕
Scalability
```

### Generative Data Engine

```text
Generation Scale
        ↕
Grounding Reliability
```

---

## 9. Key Findings

1. VLA의 핵심 병목은 model architecture만의 문제가 아니다.

2. Dataset scale만 증가시켜도 generalization이 자동으로 확보되지는 않는다.

3. Real-world data는 fidelity가 높지만 비용이 크고, synthetic data는 scalable하지만 sim-to-real과 physical realism 문제가 있다.

4. Benchmark는 단순 success rate뿐 아니라 long-horizon reasoning과 failure source를 진단할 수 있어야 한다.

5. Data generation capacity는 빠르게 증가하고 있지만 physical grounding, verification, embodiment alignment는 그 속도를 따라가지 못하고 있다.

6. Dataset, Benchmark, Data Engine을 독립적으로 발전시키기보다 함께 co-design할 필요가 있다.

---

## 10. Future Work / Open Challenges

### Representation Alignment

서로 다른 robot embodiment와 action interface를 하나의 transferable representation으로 정렬하는 문제.

### Multimodal Supervision

Vision뿐 아니라:

- tactile
- force
- audio
- depth
- proprioception

등의 physically grounded signal을 scalable하게 수집하는 문제.

### Reasoning Assessment

Future benchmark는 단순 success / failure보다 다음을 구분해서 평가할 필요가 있다.

- planning
- memory
- temporal reasoning
- skill composition
- recovery
- compositional generalization

### Scalable Data Generation

많은 데이터를 생성하는 것뿐 아니라 다음을 유지해야 한다.

- physical plausibility
- embodiment alignment
- temporal consistency
- real-world transferability

### High-Fidelity Simulation

Promising direction:

```text
Real-world Scene
      ↓
High-Fidelity Reconstruction
      ↓
Physics-Aware Simulation
      ↓
Large-scale Synthetic Data
      ↓
VLA Training / Evaluation
      ↓
Real Robot
```

### World Models

Long-term direction:

- realistic environment reconstruction
- future-state prediction
- closed-loop planning
- reduced dependence on physical robot data collection

---

## 11. My Takeaway

- VLA는 단순히 Vision + Language → Action을 구현하는 model architecture 문제가 아니다.
- 앞으로의 핵심은 robot data를 얼마나 많이 확보하느냐보다 얼마나 physically grounded하고 transferable하게 확보하느냐에 있다.
- Real-world와 synthetic data는 대체 관계라기보다 complementary한 관계에 가깝다.

```text
Synthetic Data
→ Scale

Real-World Data
→ Fidelity / Calibration

Together
→ Robust Deployment
```

- Benchmark 역시 final success rate만 보는 방식에서 벗어나 reasoning과 generalization failure를 진단하는 방향으로 발전해야 한다.
- 가장 중요한 전체 메시지는 다음과 같다.

> VLA progress requires Dataset, Benchmark, and Data Engine to scale together without losing physical grounding.

---

# 12. Section Notes

## 12.1 Introduction

VLA는 natural language instruction을 기반으로 visual observation에서 robot action을 직접 생성하는 generalist robot learning paradigm이다.

기존 fixed-task robot system과 달리 다음에 대한 generalization을 목표로 한다.

- object
- environment
- task
- embodiment

이 논문은 VLA의 핵심 문제가 model design뿐 아니라 data와 evaluation으로 이동하고 있다고 본다.

---

## 12.2 Preliminaries

Survey scope는 robotic manipulation이다.

핵심 VLA formulation:

```text
a_t = π(o_t, l)
```

Action space는 서로 다른 두 축으로 구분된다.

```text
Control Target
├── EEF
└── Joint / DoF

Parameterization
├── Absolute
└── Relative / Delta
```

Dataset과 Data Engine의 핵심 차이:

```text
Dataset
= static data resource

Data Engine
= dynamic data generation process
```

---

## 12.3 VLA Datasets

### Real-World

장점:

- high physical fidelity
- authentic robot interaction

한계:

- expensive
- difficult to scale

Dataset selection은 deployment objective에 따라 달라진다.

```text
Cross-Embodiment
→ Open X-Embodiment

Specific Robot
→ RT-1 / DROID / BridgeData V2

Contact-rich
→ RH20T
```

### Synthetic

장점:

- scalable
- cost-effective
- automatic generation / randomization

한계:

- rendering gap
- inaccurate physics
- sim-to-real gap

Practical pattern:

```text
Synthetic Pretraining
        ↓
Real-world Fine-tuning / Calibration
        ↓
Deployment
```

---

## 12.4 VLA Benchmarks

Benchmark difficulty는 두 축으로 분석할 수 있다.

```text
Task Complexity
Simple → Long-horizon / Compositional

Environment Structure
Table-top → Multi-scene
```

### Table-top

장점:

- reproducible
- controlled
- failure analysis가 비교적 쉬움

한계:

- open-world diversity가 제한됨

### Multi-scene

장점:

- diverse environments
- long-horizon reasoning
- realistic interaction

한계:

- task complexity와 environment variability가 함께 증가
- failure attribution이 어려움

---

## 12.5 VLA Data Engines

### Video-to-Data

```text
Human Video
    ↓
Pose / Scene Reconstruction
    ↓
Retargeting
    ↓
Robot Training Data
```

핵심 문제:

- visual embodiment gap
- reconstruction noise
- action error

### Hardware-Assisted

Teleoperation이나 sensing interface를 이용하여 physically grounded demonstration을 직접 수집한다.

```text
High Precision Lab Collection
          ↕
Portable In-the-Wild Scalability
```

### Generative

네 가지 주요 전략:

```text
Trajectory Reuse
LLM-driven Generation
Visual Augmentation
Predictive World Models
```

각 방식은 scalability를 높이지만 physical grounding과 real-world transfer가 핵심 한계다.

---

## 12.6 Limitations and Future Directions

### Dataset

```text
High Fidelity
+ Large Scale
+ Low Cost
+ Embodiment Diversity
```

네 요소를 동시에 만족시키기 어려움.

### Benchmark

현재 benchmark는 model이 실패했다는 것은 보여주지만 왜 실패했는지는 충분히 설명하지 못함.

### Data Engine

가장 중요한 scaling imbalance:

```text
Data Generation
      ↑↑↑

Physical Grounding
Verification
Embodiment Alignment
      ↑
```

데이터 생성 속도가 grounding과 validation 능력보다 빠르게 증가하고 있다.

### Future

핵심 목표:

```text
Synthetic Scalability
        +
Real-world Fidelity
```

High-fidelity simulation과 learned world model이 이를 연결할 가능성이 있음.

---

## 12.7 Conclusion

이 논문의 central challenge는 단순한 data scarcity가 아니다.

핵심은 heterogeneous robot platform에서 다음을 연결하는 unified abstraction이 부족하다는 것이다.

```text
Perception
    ↓
Language Grounding
    ↓
Embodied Control
```

따라서 future VLA progress는 다음 세 요소의 co-design에 달려 있다.

```text
Dataset
+
Benchmark
+
Data Engine
```

최종 목표는:

> Scalable yet physically grounded supervision.