# VLA Models and Methods

This document summarizes the representative models, architectural families, action representations, datasets, and methods introduced in the survey.

---

## 1. Evolution of VLA Models

```text
CNN-based
│
└── CLIPort
      ↓
Transformer-based
│
├── Gato
└── VIMA
      ↓
Large-scale Real-world VLA
│
├── RT-1
├── RT-2
├── RT-X
└── OpenVLA
      ↓
Continuous Action
│
├── Octo
├── RDT-1B
└── π0
      ↓
Latent Action
│
└── LAPA
      ↓
Hierarchical VLA
│
├── RT-H
├── π0.5
└── GR00T N1
```

---

## 2. Anchor Models

### CLIPort

#### Main Idea

- One of the earliest end-to-end vision-language robotic manipulation models.
- Uses CLIP to extract visual and linguistic features.
- Combines them with the Transporter Network for manipulation.

#### Importance

> Demonstrated the feasibility of jointly learning vision, language, and robotic manipulation.

#### Limitation

- CNN and MLP-based architectures struggle to unify diverse modalities and scale effectively.

---

### Gato

#### Main Idea

- Generalist transformer agent.
- Uses a single transformer model for:
  - language
  - visual question answering
  - image captioning
  - games
  - robot control

#### Architecture

```text
Language → SentencePiece
Vision → ViT
        ↓
Decoder-only Transformer
        ↓
Autoregressive Action
```

#### Importance

> A precursor to the Robotics Transformer family.

---

### VIMA

#### Main Idea

- Encoder-decoder transformer for multimodal robot prompts.
- Conditions robot actions on combinations of:
  - text
  - goal images
  - object representations

#### Architecture

```text
Object Image → Mask R-CNN → ViT
Text → T5
Bounding Box → Tokens
        ↓
Transformer
        ↓
Discrete Action Tokens
```

#### Limitation

- Experiments were limited to simulation environments.

---

## 3. Robotics Transformer Family

### RT-1

#### Main Idea

- Large-scale real-world general-purpose robot policy.
- Trained on approximately:
  - 700 tasks
  - 130K episodes

#### Architecture

```text
Images
↓
EfficientNet

Language
↓
Universal Sentence Encoder

        ↓
FiLM Conditioning
        ↓
TokenLearner
        ↓
Decoder-only Transformer
        ↓
Discrete Action Tokens
```

#### Key Point

- Predicts action tokens non-autoregressively.

#### Importance

> One of the first scalable VLAs covering a broad range of real-world robotic tasks.

---

### RT-2

#### Main Idea

- Extends RT-1 by using large pre-trained Vision-Language Models as the backbone.

#### Backbone

- PaLM-E
- PaLI-X

#### Training

```text
Internet-scale Vision-Language Data
                +
             Robot Data
                ↓
         Joint Fine-tuning
                ↓
         Robot Actions
```

#### Importance

> Established the use of pre-trained VLM backbones as a standard design pattern for VLA.

---

### RT-X

#### Main Idea

- Trains policies using datasets collected from multiple robot embodiments.

#### Importance

> Demonstrated that multi-embodiment robot data can improve generalization compared with single-robot training.

---

### RT-H

#### Main Idea

Hierarchical policy:

```text
Observation + Instruction
        ↓
High-level Policy
        ↓
Language Motion
        ↓
Low-level Policy
        ↓
Robot Action
```

#### Importance

- Introduced an intermediate language-based action representation.
- Improved performance on long-horizon tasks.
- Representative early hierarchical VLA architecture.

---

## 4. Open-source VLA

### OpenVLA

#### Backbone

```text
Prismatic VLM
├── LLaMA 2 7B
├── DINOv2
└── SigLIP
```

#### Training

- Full fine-tuning on Open X-Embodiment.

#### Importance

> Representative mainstream open-source VLA based on a pre-trained VLM backbone.

---

## 5. Continuous Action Generation

### Octo

#### Main Idea

- Generalist open-source robot policy.
- First major VLA in the survey to use Diffusion Policy.

#### Architecture

```text
Language → T5
Goal Image → CNN
Observation → CNN
Proprioception → MLP
        ↓
Transformer
        ↓
Readout Token
        ↓
Diffusion Action Head
        ↓
Continuous Action
```

#### Importance

> Represents the transition from discrete action tokens toward smooth continuous action generation.

---

### RDT-1B

#### Main Idea

- Large-scale Diffusion Transformer for robotic control.
- Integrates the diffusion process directly into the transformer.

#### Architecture

```text
Language → T5
Vision → SigLIP
        ↓
Multimodal Conditioning
        ↓
Diffusion Transformer
        ↓
Action Representation
        ↓
MLP
        ↓
Executable Robot Action
```

#### Key Method: Alternating Condition Injection

- Image and text conditions are injected alternately across transformer layers.
- Designed to improve multimodal conditioning and reduce overfitting.

#### Importance

> Unlike architectures with a separate diffusion action head, RDT-1B integrates diffusion directly into the transformer backbone.

---

### π0

#### Backbone

- PaliGemma

#### Main Idea

- Introduces an Action Expert using flow matching.
- Handles both discrete multimodal representations and continuous robot actions.

#### Architecture

```text
Vision + Language
      ↓
PaliGemma
      ↓
Readout Representation
      +
Proprioception
      ↓
Action Expert
      ↓
Flow Matching
      ↓
Action Chunk
```

#### Key Point

- Outputs entire action chunks in parallel.
- Achieves control rates up to approximately 50 Hz.

#### Importance

> Representative VLA showing the shift from diffusion toward flow matching for real-time continuous control.

---

## 6. Latent Action Learning

### LAPA

#### Main Idea

- Learns latent actions from unlabeled video data.

```text
Image_t
   +
Image_t+H
   ↓
Temporal Representation
   ↓
VQ-VAE
   ↓
Latent Action Token z_t
```

The latent action is used to reconstruct future observations:

```text
Image_t + Latent Action
        ↓
World Model
        ↓
Predict Image_t+H
```

#### Importance

- Enables VLA pre-training using human videos without explicit robot action labels.
- Helps bridge human-to-robot embodiment differences.

#### Used in

- GR00T N1
- DreamGen

---

## 7. Hierarchical VLA

### π0.5

#### Main Idea

Combines:

```text
High-level Discrete Action Generation
              +
Low-level Flow Matching Control
```

#### Structure

```text
Language / Observation
        ↓
Subtask / Symbolic Action
        ↓
FAST Action Tokens
        ↓
Flow Matching Controller
        ↓
Continuous Robot Action
```

#### Importance

> Unifies high-level reasoning and low-level continuous control within one framework.

---

### GR00T N1

#### Main Idea

Integrates several major VLA trends:

```text
LAPA
→ Latent Action Learning

RDT-1B
→ Diffusion Transformer

π0
→ Flow Matching

        ↓

Hierarchical Generalist VLA
```

#### Architecture

- VLM as high-level policy
- Diffusion Transformer as low-level policy
- Flow matching for continuous action generation

#### Importance

> Representative generalist VLA architecture for humanoid robots.

---

## 8. Sensorimotor Architecture Taxonomy

### 8.1 Transformer + Discrete Action Token

```text
Vision + Language
      ↓
Transformer
      ↓
Discrete Action Token
```

Representative models:

- Gato
- VIMA
- RT-1
- RoboCat
- RoboFlamingo

---

### 8.2 Transformer + Diffusion Action Head

```text
Vision + Language
      ↓
Transformer
      ↓
Diffusion Action Head
      ↓
Continuous Action
```

Representative models:

- Octo
- NoMAD
- TinyVLA
- RoboBERT
- VidBot

---

### 8.3 Diffusion Transformer

```text
Vision + Language
      ↓
Diffusion Transformer
      ↓
Continuous Action
```

Representative models:

- RDT-1B
- MDT
- DexGraspVLA
- FP3
- Dita

---

### 8.4 VLM + Discrete Action Token

```text
Vision + Language
      ↓
Pre-trained VLM
      ↓
Discrete Action Token
```

Representative models:

- RT-2
- OpenVLA
- RT-H
- ECoT
- 3D-VLA

---

### 8.5 VLM + Diffusion Action Head

```text
Vision + Language
      ↓
VLM
      ↓
Diffusion Action Head
      ↓
Continuous Action
```

Representative models:

- Diffusion-VLA
- DexVLA
- ChatVLA
- ObjectVLA
- GO-1
- PointVLA
- HybridVLA

---

### 8.6 VLM + Flow Matching Action Head

```text
Vision + Language
      ↓
VLM
      ↓
Flow Matching Action Head
      ↓
Continuous Action
```

Representative models:

- π0
- π0.5
- GraspVLA
- OneTwoVLA
- Hume
- SwitchVLA

---

### 8.7 VLM + Diffusion Transformer

```text
Vision + Language
      ↓
VLM
      ↓
Diffusion Transformer
      ↓
Continuous Action
```

Representative models:

- GR00T N1
- CogACT
- TrackVLA
- SmolVLA
- MinD

---

## 9. World Models

World models predict future observations or latent representations from current observations and instructions.

```text
Current Observation
        ↓
World Model
        ↓
Future Observation / Latent State
        ↓
Planning / Action Generation
```

Three main design patterns are introduced.

---

### 9.1 Action Generation using World Models

```text
Observation + Instruction
        ↓
World Model
        ↓
Future Image / Video
        ↓
Inverse Dynamics Model
        ↓
Robot Action
```

Representative models:

- UniPi
- DreamGen
- GeVRM
- HiP
- Dreamitate
- SuSIE
- LUMOS

Important intermediate representations:

- future video
- future image
- subgoal image
- optical flow
- feature-point trajectory
- object displacement

#### Embodiment-Agnostic Intermediate Representations

Many approaches use:

- optical flow
- feature-point trajectories

because they can represent motion without directly depending on a specific robot action space.

Representative models:

- AVDC
- ATM
- Track2Act
- LangToMo
- MinD
- PPI

---

### 9.2 Latent Action Generation via World Models

```text
Current Image + Future Image
        ↓
World Model
        ↓
Latent Action
        ↓
VLA Pre-training
```

Representative models:

- LAPA
- Moto
- UniVLA
- UniSkill

#### Main Benefit

> Enables learning from large-scale human videos without explicit robot action labels.

---

### 9.3 Sensorimotor Models with Implicit World Models

These models jointly predict:

```text
Robot Action
+
Future Observation
```

Representative models:

- GR-1
- GR-2
- GR-3
- GR-MG
- 3D-VLA
- FLARE
- WorldVLA
- ViSA-Flow

#### Main Idea

> Future observation prediction acts as an auxiliary task that improves action learning and planning.

---

## 10. Affordance-based Models

Affordance refers to:

> The actions that are possible given an object, scene, environment, and the robot's embodiment.

Three major approaches are introduced.

---

### 10.1 Affordance Prediction and Action Generation using VLMs

```text
Vision + Language
        ↓
VLM
        ↓
Affordance
        ↓
Action
```

Representative models:

- VoxPoser
- KAGI
- LERF-TOGO
- Splat-MOVER

Typical affordance representations:

- affordance maps
- constraint maps
- keypoints
- grasp regions
- 3D point clouds

---

### 10.2 Affordance Extraction from Human Data

Human videos are used to extract:

- hand trajectories
- contact points
- object interactions
- hand-object relationships

Representative models:

- VRB
- HRP
- VidBot

#### Main Benefit

> Human videos provide a scalable source of interaction knowledge without requiring direct robot demonstrations.

---

### 10.3 Affordance + Sensorimotor VLA

Representative models:

- CLIPort
- RoboPoint
- RoboGround
- RT-Affordance
- A0
- RoboBrain
- Chain-of-Affordance

Typical intermediate representations:

- keypoints
- masks
- contact points
- end-effector poses
- affordance regions
- placement locations

---

## 11. Data Modalities

### Vision

Common visual encoders:

- ResNet
- ViT
- EfficientNet
- CLIP
- SigLIP
- DINOv2

Recent trend:

> SigLIP and DINOv2 have become preferred visual feature extractors in many modern VLAs.

Image tokenization:

- VQ-VAE
- VQ-GAN

Token compression:

- Perceiver Resampler
- Q-Former
- QT-Former
- TokenLearner

Object-centric representations:

- bounding boxes
- segmentation masks
- cropped object embeddings
- tracked features

---

### Language

Common tokenizers:

- T5 tokenizer
- LLaMA tokenizer
- BPE
- SentencePiece

Common text encoders:

- Universal Sentence Encoder
- CLIP Text Encoder
- Sentence-BERT
- DistilBERT

Common LLM / VLM backbones:

- LLaMA
- Gemma
- Qwen
- Phi
- PaLM-E
- PaliGemma
- PrismaticVLM

---

### Additional Modalities

#### Audio

Representative methods:

- spectrogram / mel-spectrogram
- AST
- Whisper
- SpeechTokenizer

#### Tactile / Force

Representative sensors:

- DIGIT
- GelStereo
- 6-axis force-torque sensor

Useful for:

- contact-rich manipulation
- peg insertion
- fine-grained interaction

#### 3D Information

Four major forms:

```text
3D Information
├── Depth Images
├── Multi-view Images
├── Voxel Representations
└── Point Clouds
```

Representative encoders:

- Depth Anything
- ZoeDepth
- VGGT
- UVFormer
- PointNet
- PointNet++
- PointNext
- Uni3D ViT

---

## 12. Action Representation

### 12.1 Discrete Action Tokens

```text
Continuous Action Space
        ↓
Binning
        ↓
Discrete Tokens
```

Typical setup:

- each action dimension is discretized into approximately 256 bins

Representative models:

- RT-2
- OpenVLA

#### Advantages

- compatible with language-model next-token prediction
- simple cross-entropy training

#### Limitations

- increases token length
- can reduce control frequency
- less suitable for smooth real-time control

---

### 12.2 FAST Action Tokenization

FAST improves token efficiency using:

```text
Action Sequence
      ↓
Discrete Cosine Transform
      ↓
Quantization
      ↓
Byte-Pair Encoding
```

Used in:

- π0.5

#### Main Benefit

> Reduces action sequence length and enables faster inference than conventional binning.

---

### 12.3 Token-to-Continuous Action Decoding

```text
Transformer Token
      ↓
MLP / LSTM / GMM
      ↓
Continuous Robot Action
```

Loss functions:

- L1
- L2
- binary cross-entropy for binary gripper commands

---

### 12.4 Diffusion

Representative model:

- Octo

Advantages:

- smooth continuous actions
- multimodal action distributions
- non-autoregressive generation

---

### 12.5 Flow Matching

Representative model:

- π0

Advantages:

- smooth continuous actions
- fewer inference steps than conventional diffusion
- improved real-time responsiveness

---

### 12.6 Latent Action

Representative model:

- LAPA

Advantage:

> Enables action representation learning from videos without explicit robot action labels.

---

## 13. Cross-Embodiment Methods

### Open X-Embodiment

Standardizes multiple robot datasets into a shared format.

Core insight:

> Training on diverse robot embodiments improves VLA generalization.

---

### CrossFormer

```text
Heterogeneous Robot Modalities
        ↓
Modality-specific Tokenizers
        ↓
Unified Token Sequence
        ↓
Shared Transformer
        ↓
Embodiment-specific Action Heads
```

Examples of embodiment-specific heads:

- single-arm
- bimanual
- navigation
- quadruped

---

### UniAct

Introduces a Universal Action Space.

```text
Shared Discrete Action Codebook
        ↓
Embodiment-specific Decoder
        ↓
Robot Action
```

#### Main Idea

> Represent heterogeneous robot actions through a shared atomic action space.

---

### Embodiment-Agnostic Intermediate Representations

Instead of aligning different robot action spaces directly, some approaches use:

- optical flow
- feature-point trajectories

Representative models:

- LangToMo
- ATM

---

## 14. Emerging Reasoning Methods

### Hierarchical Policy

```text
Complex Instruction
        ↓
High-level Policy
        ↓
Subtasks / Intermediate Representation
        ↓
Low-level Policy
        ↓
Robot Actions
```

Representative models:

- RT-H
- π0.5
- GR00T N1
- LoHoVLA
- Hi Robot
- NaVILA

#### Main Benefit

> Separates semantic reasoning from fine-grained motor execution.

---

### Chain-of-Thought for VLA

Representative models:

- ECoT
- CoT-VLA
- ECoT-Lite
- Fast ECoT

Intermediate reasoning may include:

- task descriptions
- subtasks
- object positions
- subgoal images

#### Main Goal

> Introduce explicit intermediate reasoning between perception, instruction, and action generation.

---

## 15. Training

### Supervised / Imitation Learning

Most common VLA training paradigm.

```text
Image + Language + Action
        ↓
Supervised Learning
        ↓
VLA Policy
```

Typical pipeline:

```text
Pre-trained VLM
      ↓
Large-scale Pre-training
      ↓
High-quality Post-training
      ↓
Robot Policy
```

---

### Self-Supervised Learning

Three major purposes:

1. Modality alignment
2. Visual representation learning
3. Latent action representation learning

Representative techniques:

- contrastive learning
- masked autoencoding
- self-distillation
- future observation reconstruction

---

### Reinforcement Learning

Two major strategies:

#### 1. RL Fine-tunes the VLA

```text
VLA
 ↓
Environment
 ↑
Reward
```

Representative models:

- iRe-VLA
- ConRFT
- VLA-RL
- RLDG
- DSRL

#### 2. VLA as High-level Policy + RL as Low-level Controller

```text
VLA
 ↓
High-level Command
 ↓
RL Controller
 ↓
Robot
```

Representative models:

- Humanoid-VLA
- NaVILA
- SLIM

#### Limitation

- sample inefficiency
- unsafe exploration
- high computational cost
- most evaluations remain in simulation or simplified setups

---

## 16. Training Stages and Adaptation

### Pre-training

Goals:

- general capabilities
- semantic grounding
- cross-task generalization
- cross-embodiment transfer

Important data sources:

- heterogeneous robot demonstrations
- human videos
- web-scale vision-language data
- synthetic trajectories
- simulation data

---

### Gradient Insulation

#### Main Idea

Prevent gradients from the randomly initialized action head from damaging the pre-trained VLM backbone.

```text
Pre-trained VLM
      X
Action-head Gradient
```

Benefits:

- training stability
- knowledge preservation
- training efficiency

---

### Post-training

Uses:

- task-specific data
- robot-specific data
- high-quality demonstrations

Common strategies:

- full fine-tuning
- action-head-only fine-tuning
- LoRA

---

### Frozen Backbone vs. Full Fine-tuning

```text
Frozen Backbone
+ cheaper
+ faster
+ preserves general knowledge
- weaker robot-domain adaptation

Full Fine-tuning
+ stronger specialization
+ potentially higher performance
- expensive
- risk of catastrophic forgetting
```

---

## 17. Data Collection

### Teleoperation

Representative systems:

- ALOHA
- Mobile ALOHA
- ALOHA 2
- Bi-ACT
- GELLO
- Apple Vision Pro-based teleoperation

#### ALOHA

Leader-follower teleoperation:

```text
Human
 ↓
Leader Robot
 ↓
Follower Robot
 ↓
Demonstration Trajectory
```

---

### Proxy Devices

Representative systems:

- UMI
- DexUMI
- Dobb-E
- DexCap
- DexWild

#### UMI

```text
Human Demonstration
      ↓
UMI + GoPro
      ↓
Visual SLAM
      ↓
6-DoF Trajectory
      ↓
Robot Policy Training
```

#### Main Benefit

> Human demonstration data can be collected without physically moving the target robot during collection.

---

### Human Data Collection

Representative datasets:

- Ego4D
- EPIC-KITCHENS
- Ego-Exo4D
- HOT3D
- HD-EPIC

#### Main Benefit

> Human behavior is much easier to collect at scale than robot interaction data.

---

## 18. Important Robot Datasets

| Dataset | Main Characteristic |
|---|---|
| QT-Opt | 580K grasp attempts |
| RT-1 | 130K trajectories, 700+ tasks |
| OXE | 1.4M episodes across 22 robot embodiments |
| DROID | 76K trajectories using a standardized Franka platform |
| RoboMIND | 107K trajectories with diverse embodiments |
| AgiBot World | Approximately 1M real-world trajectories |
| RH20T | RGB-D + force + audio multimodal data |
| BridgeData V2 | Large WidowX manipulation dataset |
| FuSe | Vision + tactile + audio multimodal robot dataset |

---

## 19. Data Augmentation

### Vision Augmentation

Representative methods:

- CACTI
- GenAug
- ROSIE
- DreamGen
- BYOVLA

Common techniques:

- object texture modification
- distractor insertion
- background modification
- generative image editing
- synthetic video generation

---

### Language Augmentation

Representative method:

- DIAL

Typical strategy:

```text
Seed Instructions
      ↓
LLM Paraphrasing
      ↓
Large Instruction Pool
      ↓
VLM Matching
      ↓
Trajectory Annotation
```

---

### Action Augmentation

Representative methods:

- DAgger
- CCIL

Main idea:

> Collect or synthesize corrective actions for states that the learned policy visits but expert demonstrations do not cover.

---

## 20. Important Evaluation Benchmarks

### MuJoCo-based

- robosuite
- robomimic
- RoboCasa
- LIBERO
- Meta-World

### PhysX / Isaac / SAPIEN

- IsaacLab
- ManiSkill
- ManiSkill 2
- ManiSkill 3
- ManiSkill-HAB
- RoboTwin

### Bullet-based

- Ravens
- VIMA-BENCH
- CALVIN
- Habitat
- Habitat 2.0
- Habitat 3.0

### RLBench Family

- RLBench
- THE COLOSSEUM

### Realistic / Real-world Evaluation

- SIMPLER
- RoboArena

#### Evaluation Trend

```text
Simulation Benchmark
        ↓
Realistic Real-to-Sim Evaluation
        ↓
Distributed Real-world Evaluation
```

---

## 21. Robot Platforms

```text
Robot Platforms
├── Manipulator
├── Hand / Gripper
├── Mobile Robot
├── Quadruped Robot
└── Humanoid Robot
```

### Manipulator

Most commonly used platform in VLA research.

Typical tasks:

- grasping
- pick-and-place
- assembly
- deformable object manipulation
- peg insertion

### Hand / Gripper

Used for:

- grasping
- tool use
- dexterous manipulation
- in-hand manipulation

### Mobile Robot

Used for:

- navigation
- mobile manipulation
- autonomous driving
- aerial robotics

### Quadruped Robot

Used for:

- rough-terrain locomotion
- outdoor navigation
- mobile manipulation

### Humanoid Robot

Advantages:

- human-like morphology
- compatibility with human environments
- potentially easier transfer from human demonstrations

---

## 22. Practitioner Recommendations

The survey recommends:

```text
1. Diverse + High-quality Data

2. Continuous Action Generation
   → Diffusion
   → Flow Matching

3. Gradient Insulation

4. Lightweight Adaptation
   → Action-head Fine-tuning
   → LoRA

5. World Models + Latent Actions

6. Multi-task Learning
   → Affordance
   → Keypoint
   → Future Prediction
   → Segmentation
```

---

## 23. Future Directions

### Multimodal Data

Need more scalable datasets containing:

- tactile
- force
- audio
- depth
- 3D information

### Reasoning and Memory

Need:

- long-horizon reasoning
- temporal memory
- information retrieval
- task decomposition

### Continual Learning

Need:

- online adaptation
- lifelong learning
- catastrophic forgetting prevention
- safe policy updates

### Reinforcement Learning

Promising directions:

- RL inside world models
- real-to-sim RL
- digital twins
- safer and more sample-efficient exploration

### Safety

Potential direction:

```text
VLA Generalization
        +
Model-based Control
        ↓
Safer Real-world Robot
```

### Failure Detection and Recovery

Need:

- failure detection
- action regeneration
- subtask regeneration
- re-planning
- predictive recovery

Representative models:

- SAFE
- Agentic Robot
- LoHoVLA
- FOREWARN

### Evaluation

Need statistically rigorous evaluation using:

- sufficient trials
- controlled conditions
- confidence intervals
- reproducible protocols

---

## 24. Final VLA Landscape

```text
                         VLA
                          │
        ┌─────────────────┼──────────────────┐
        │                 │                  │
   Architecture          Data             Learning
        │                 │                  │
 Sensorimotor        Robot Demo              IL
 World Model         Human Video             SSL
 Affordance          Simulation              RL
        │
        ↓
 Action Representation
        │
 ┌──────┼───────────────┐
Discrete   Diffusion   Flow Matching
        │
        ↓
 Latent Action / World Model
        │
        ↓
 Hierarchical Reasoning
        │
        ↓
 Real Robot Control
        │
 ┌──────┼───────────┬──────────────┐
Safety  Evaluation  Recovery  Continual Learning
```

---

## 25. Core Models to Remember

If only a small number of models are retained from this survey:

| Model | Why It Matters |
|---|---|
| CLIPort | Early vision-language manipulation |
| Gato | Generalist transformer precursor |
| RT-1 | Scalable real-world robot transformer |
| RT-2 | VLM backbone becomes central to VLA |
| RT-X | Cross-embodiment learning |
| OpenVLA | Representative open-source VLA |
| Octo | Diffusion-based continuous action |
| RDT-1B | Diffusion Transformer |
| π0 | Flow matching |
| LAPA | Latent actions from human video |
| π0.5 | Hierarchical discrete + continuous control |
| GR00T N1 | Generalist humanoid hierarchical VLA |

---

## 26. Models Worth Reading Next

### Core VLA Papers

1. RT-1
2. RT-2
3. Open X-Embodiment / RT-X
4. OpenVLA
5. Diffusion Policy
6. Octo
7. π0
8. LAPA
9. π0.5
10. GR00T N1

### Simulation / Synthetic Data / World Model Direction

11. GraspVLA
12. RDT-1B
13. DreamGen
14. 3D-VLA
15. ManiSkill / Isaac-based robot learning works