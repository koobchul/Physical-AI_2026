# Vision-Language-Action Models for Robotics: A Review Towards Real-World Applications

## 0. Paper Information

- Title: Vision-Language-Action Models for Robotics: A Review Towards Real-World Applications
- Authors: Kento Kawaharazuka, Jihoon Oh, Jun Yamada, Ingmar Posner, Yuke Zhu
- Year: 2025
- Venue: arXiv preprint (cs.RO)
- Paper: arXiv:2510.07077
- Code:
- Project: https://vla-survey.github.io

---

## 1. One-line Summary

> A full-stack survey of Vision-Language-Action models covering architectural evolution, multimodal representations, training, data, robot platforms, evaluation, and real-world deployment.

---

## 2. Why this Paper?

### Problem

- Earlier robotic systems often decouple LLMs/VLMs from low-level robot policies.
- Such systems typically rely on fixed motion primitives or task-specific imitation policies.
- This limits generalization to unseen tasks, objects, environments, and robot embodiments.
- VLA research is still in an early stage, and architectures and training methodologies are not yet standardized.

### Motivation

- VLA models aim to directly connect vision and language understanding with executable robot actions.
- Generalist robot policies could reduce task-specific data collection and training costs.
- Practical VLA deployment requires understanding not only model architectures, but also data, hardware, evaluation, and deployment constraints.

### Main Contribution

- Provides a comprehensive full-stack review of VLA systems.
- Covers:
  - architectural evolution
  - architectures and building blocks
  - modality-specific processing
  - training paradigms
  - data collection
  - datasets
  - data augmentation
  - robot platforms
  - evaluation benchmarks
  - real-world applications
- Provides practical recommendations for applying VLA models to real robotic systems.

---

## 3. Key Concepts

### VLA Definition

A VLA model:

- takes visual observations and natural language instructions as required inputs
- may additionally incorporate proprioception, depth, tactile sensing, audio, or 3D information
- directly generates robot control commands

High-level VLM/LLM systems that merely select from pre-trained skills or motion primitives are excluded from the survey's definition of VLA.

### Generalist Robot Policy

A VLA aims to generalize across:

- tasks
- objects
- environments
- embodiments

### Full-stack View of VLA

```text
Vision + Language + Other Modalities
                ↓
        Representation
                ↓
        VLA Architecture
                ↓
          Action Policy
                ↓
        Robot Execution
                ↓
       Real-world Evaluation
```

```text
VLA System
├── Model
│   ├── Architecture
│   ├── Modality
│   └── Training
│
├── Data
│   ├── Collection
│   ├── Dataset
│   └── Augmentation
│
└── Deployment
    ├── Robot Platform
    ├── Evaluation
    ├── Safety
    └── Real-world Application
```

---

## 4. Taxonomy / Method

### 4.1 Challenges

- Data requirements and scarcity
- Embodiment transfer
- Computational and training cost

### 4.2 Architectural Evolution

```text
CNN-based VLA
      ↓
Transformer
      ↓
Pre-trained VLM Backbone
      ↓
Diffusion Policy
      ↓
Diffusion Transformer
      ↓
Flow Matching
      ↓
Latent Action Learning
      ↓
Hierarchical Policy
```

### 4.3 Main Architecture Types

```text
VLA Architecture
├── Sensorimotor Model
├── World Model
└── Affordance-based Model
```

### 4.4 Learning Paradigms

```text
Training
├── Supervised Learning / Imitation Learning
├── Self-Supervised Learning
└── Reinforcement Learning
```

### 4.5 Data

```text
Data
├── Robot Demonstrations
├── Human Demonstrations
├── Human Videos
├── Simulation
└── Web-scale Vision-Language Data
```

---

## 5. Important Models / Datasets / Methods

### Important VLA Models

| Model | Main Focus |
|---|---|
| CLIPort | Early vision-language robotic manipulation |
| Gato | Generalist transformer agent |
| VIMA | Multimodal prompt-conditioned manipulation |
| RT-1 | Large-scale real-world transformer policy |
| RT-2 | Pre-trained VLM backbone for robotic control |
| RT-X | Cross-embodiment robot learning |
| OpenVLA | Open-source VLM-based VLA |
| Octo | Diffusion Policy for generalist robot control |
| RDT-1B | Diffusion Transformer for bimanual manipulation |
| π0 | Flow-matching VLA for continuous action generation |
| LAPA | Latent action learning from unlabeled videos |
| π0.5 | Hierarchical VLA with discrete and continuous actions |
| GR00T N1 | Generalist hierarchical humanoid VLA |

### Important Datasets

| Dataset | Main Characteristic |
|---|---|
| RT-1 | 130K real-world robot demonstrations |
| Open X-Embodiment (OXE) | 1.4M episodes across diverse robot embodiments |
| DROID | Standardized distributed Franka robot dataset |
| RoboMIND | Large-scale data across diverse robot embodiments |
| AgiBot World | Approximately 1M real-world robot trajectories |
| Ego4D | Large-scale egocentric human video |
| Ego-Exo4D | Egocentric and exocentric human interaction data |
| EPIC-KITCHENS | Large-scale human-object interaction videos |

### Important Evaluation Benchmarks

| Benchmark | Main Focus |
|---|---|
| LIBERO | Language-conditioned manipulation |
| CALVIN | Long-horizon language-conditioned manipulation |
| RLBench | Large-scale manipulation benchmark |
| THE COLOSSEUM | Robustness under environmental variations |
| ManiSkill | 3D manipulation and diverse embodiments |
| RoboCasa | Photorealistic household manipulation |
| SIMPLER | Real-to-sim VLA evaluation |
| RoboArena | Distributed real-world robot evaluation |

---

## 6. Strengths

- Provides a full-stack view covering both software and hardware aspects of VLA systems.
- Connects architecture design with practical real-world deployment.
- Organizes a rapidly growing literature using clear architecture and training taxonomies.
- Covers not only models, but also:
  - robot platforms
  - datasets
  - data collection
  - data augmentation
  - evaluation
- Provides explicit recommendations for practitioners.

---

## 7. Limitations

### Current Limitations of VLA Systems

- Large-scale vision-language-action datasets remain scarce and expensive.
- High-quality robot demonstrations are difficult to collect at scale.
- Policies still struggle to transfer across different robot embodiments.
- Human videos generally lack explicit robot action labels.
- Training and inference require substantial computation.
- Real-world inference is constrained by latency and memory usage.
- Most RL-based VLA methods remain limited to simulation or simplified real-world settings.
- Real-world evaluation protocols are not yet standardized.
- Current systems still lack sufficient:
  - safety
  - robustness
  - failure recovery
  - continual learning capability

---

## 8. Trade-offs

### Discrete vs. Continuous Action

```text
Discrete Action Tokens
+ compatible with LLM-style next-token prediction
+ relatively simple training
- longer token sequences
- lower control frequency
- less smooth motion

Continuous Actions
+ smooth and precise control
+ better suited for real-time robotics
- require specialized action-generation modules
```

### Diffusion vs. Flow Matching

```text
Diffusion
+ stable continuous action generation
+ expressive multimodal action distributions
- requires multiple denoising steps
- relatively high inference latency

Flow Matching
+ continuous and smooth actions
+ fewer inference steps
+ better real-time responsiveness
```

### Frozen Backbone vs. Full Fine-tuning

```text
Frozen Backbone
+ lower GPU memory usage
+ faster training
+ preserves pre-trained knowledge
- weaker robot-domain adaptation

Full Fine-tuning
+ strong task/domain adaptation
+ potentially higher task-specific performance
- expensive
- risk of catastrophic forgetting
```

### Robot Data vs. Human Data

```text
Robot Data
+ directly grounded in executable actions
- expensive and difficult to scale

Human Data
+ highly scalable
+ abundant
- embodiment mismatch
- usually lacks robot action labels
```

### Simulation vs. Real-world Data

```text
Simulation
+ scalable
+ safe
+ controllable
- sim-to-real gap

Real-world Data
+ realistic physical interaction
+ directly relevant to deployment
- expensive
- slow to collect
- safety constraints
```

---

## 9. Key Findings

- Large-scale and diverse datasets are critical for VLA generalization.
- Pre-trained VLM backbones provide strong semantic priors and improve generalization.
- VLA architectures are shifting from discrete action prediction toward continuous action generation.
- Diffusion and flow matching have become major approaches for continuous robot control.
- Flow matching is particularly attractive for real-time control because it requires fewer inference steps.
- Hierarchical architectures are emerging as an important design pattern for long-horizon tasks.
- High-level reasoning and low-level motor execution increasingly operate at different levels of abstraction.
- World models are becoming important for:
  - planning
  - future observation prediction
  - long-horizon reasoning
  - synthetic data generation
- Latent action learning enables the use of human videos without explicit action labels.
- Optical flow and feature-point trajectories provide embodiment-agnostic intermediate representations.
- VLA inputs are expanding beyond RGB and language toward:
  - depth
  - 3D information
  - tactile sensing
  - force
  - audio
- RL is increasingly used to improve or fine-tune existing VLA policies rather than train VLA systems from scratch.
- Real-world evaluation remains much less standardized than simulation evaluation.

---

## 10. Future Work / Open Challenges

### Data Modality

- Scale multimodal datasets containing:
  - tactile sensing
  - force
  - audio
  - depth
  - 3D information
- Develop standardized sensing configurations across robot platforms.

### Reasoning and Memory

- Improve long-horizon reasoning.
- Introduce persistent memory and temporal abstraction.
- Allow robots to retain and retrieve task-relevant information over long trajectories.

### Continual Learning

- Enable VLA models to continue learning after deployment.
- Address:
  - catastrophic forgetting
  - safe online learning
  - lifelong adaptation

### Reinforcement Learning

- Improve sample efficiency.
- Reduce unsafe real-world exploration.
- Use:
  - learned world models
  - digital twins
  - real-to-sim environments
  for safer and more scalable RL fine-tuning.

### Safety

- Detect humans and unexpected obstacles.
- Combine learned VLA policies with reliable model-based controllers.
- Develop hybrid learning and control architectures.

### Failure Detection and Recovery

- Detect execution failures.
- Re-plan actions or subtasks.
- Develop hierarchical recovery mechanisms.

### Evaluation

- Establish statistically rigorous evaluation protocols.
- Use:
  - sufficient evaluation trials
  - controlled conditions
  - confidence intervals
- Improve reproducibility across real robots.

### Applications

Potential applications include:

- healthcare
- assistive robotics
- industrial automation
- autonomous driving
- household robotics

Current systems still lack sufficient robustness and reliability for unrestricted real-world deployment.

---

## 11. My Takeaway

- VLA research is moving beyond simply connecting a VLM to robot actions.
- The current direction is toward hierarchical full-stack systems that combine:

```text
Large-scale Multimodal Data
          ↓
      Pre-trained VLM
          ↓
   High-level Reasoning
          ↓
World Model / Affordance
          ↓
Continuous Action Policy
(Diffusion / Flow Matching)
          ↓
      Robot Control
          ↓
RL / Recovery / Continual Learning
```

- The primary bottleneck is not only model architecture, but also:
  - scalable robot data
  - embodiment transfer
  - evaluation
  - safety
  - deployment reliability
- Human data, simulation, synthetic data, and real robot data are likely to be used together rather than independently.
- World models, latent actions, hierarchical policies, and RL are likely to play increasingly important roles in future VLA systems.

---

## 12. Section Notes

### Section I. Introduction

- Earlier systems separate LLM/VLM reasoning from low-level robot control.
- VLA directly connects vision, language, and action.
- Main goals:
  - task generalization
  - object generalization
  - environment generalization
  - embodiment transfer
- This survey defines a VLA as a model that directly generates robot control commands.

### Section II. Challenges

Three major challenges:

1. Data requirements and scarcity
2. Embodiment transfer
3. Computational and training cost

### Section III. VLA Design Strategy and Transition

Historical progression:

```text
CLIPort
↓
Gato / VIMA
↓
RT-1
↓
RT-2 / RT-X / OpenVLA
↓
Octo
↓
RDT-1B
↓
π0
↓
LAPA
↓
π0.5 / GR00T N1
```

Main architectural transition:

```text
CNN
→ Transformer
→ VLM Backbone
→ Diffusion
→ Diffusion Transformer
→ Flow Matching
→ Latent Action
→ Hierarchical Policy
```

### Section IV. Architectures and Building Blocks

Three major architectures:

```text
Sensorimotor Model
World Model
Affordance-based Model
```

Sensorimotor models include seven major variants:

1. Transformer + Discrete Action Token
2. Transformer + Diffusion Action Head
3. Diffusion Transformer
4. VLM + Discrete Action Token
5. VLM + Diffusion Action Head
6. VLM + Flow Matching Action Head
7. VLM + Diffusion Transformer

World models:

1. Action generation using future observation prediction
2. Latent action learning from human videos
3. Sensorimotor models with implicit world models

Affordance-based models:

1. VLM-based affordance prediction and action generation
2. Affordance extraction from human demonstrations
3. Integration of affordance prediction into sensorimotor VLA

Major action representations:

```text
Discrete Binning
→ Token-to-Continuous Decoding
→ Diffusion
→ Flow Matching
→ Latent Action
```

Additional modalities:

- audio
- tactile
- force
- depth
- multi-view images
- voxel
- point cloud

Emerging directions:

- hierarchical architectures
- Chain-of-Thought reasoning

### Section V. Training Strategy and Implementation

Main training paradigms:

```text
Supervised / Imitation Learning
Self-Supervised Learning
Reinforcement Learning
```

Typical training pipeline:

```text
Web-scale VLM
      ↓
Pre-training
(robot + human + multimodal data)
      ↓
Post-training
(high-quality robot/task-specific data)
```

Important trends:

- large-scale multi-task pre-training
- gradient insulation
- backbone freezing
- LoRA
- action-head-only fine-tuning
- inference acceleration

RL is mainly used for:

1. improving an existing VLA
2. training low-level control beneath a high-level VLA

### Section VI. Datasets

Data collection:

```text
Teleoperation
Proxy Devices
Human Data Collection
```

Representative systems:

- ALOHA: leader-follower teleoperation
- UMI: handheld proxy device with visual SLAM
- Ego4D / Ego-Exo4D: egocentric human data

Dataset categories:

```text
Human Dataset
Simulation Dataset
Real Robot Dataset
```

Major real-world datasets:

- RT-1
- Open X-Embodiment
- DROID
- RoboMIND
- AgiBot World

Data augmentation:

- Vision:
  - generative image editing
  - object/background modification
- Language:
  - paraphrasing
  - automatic annotation
- Action:
  - DAgger
  - corrective data generation

### Section VII. Real-world Robot Applications

Robot platforms:

- Manipulator
- Hand / Gripper
- Mobile Robot
- Quadruped Robot
- Humanoid Robot

Most VLA research still focuses on robotic manipulation.

Real-world evaluation is difficult because of:

- embodiment differences
- safety
- limited reproducibility

Therefore, simulation benchmarks remain dominant.

Evaluation trend:

```text
Simulation Evaluation
        ↓
Realistic Real-to-Sim Evaluation
        ↓
Distributed Real-world Evaluation
```

### Section VIII. Recommendations for Practitioners

1. Prioritize diverse and high-quality datasets.
2. Prefer continuous actions using diffusion or flow matching.
3. Use gradient insulation during pre-training.
4. Begin with lightweight adaptation such as action-head fine-tuning or LoRA.
5. Use world models and latent actions to exploit human videos.
6. Use multi-task learning to improve action-relevant representations.

### Section IX. Future Research Directions

Key directions:

- multimodal sensing
- reasoning and memory
- continual learning
- reinforcement learning
- safety
- failure detection and recovery
- rigorous evaluation
- real-world applications

### Section X. Conclusion

Four major conclusions:

1. Large-scale data and pre-trained foundation models are essential.
2. Hierarchical policies are becoming increasingly important.
3. Modalities beyond vision and language are gaining importance.
4. Sim-to-real transfer and embodiment generalization remain major unsolved problems.

Future VLA systems are expected to increasingly combine:

```text
VLM
+ World Model
+ Affordance
+ Hierarchical Policy
+ Continuous Action Generation
+ Reinforcement Learning
```