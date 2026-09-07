# Representative Works

This document summarizes the representative datasets, benchmarks, and data engines introduced in the survey.

```text
Representative Works
├── VLA Datasets
│   ├── Real-World
│   └── Synthetic
│
├── VLA Benchmarks
│   ├── Table-top
│   └── Multi-scene
│
└── VLA Data Engines
    ├── Video-to-Data
    ├── Hardware-Assisted
    └── Generative
```

---

# 1. VLA Datasets

## 1.1 Real-World Datasets

### Open X-Embodiment (Padalkar et al., 2023)

- Aggregates data from diverse robot platforms and institutions
- Designed for cross-embodiment pretraining and large-scale transfer
- Provides broad robot and task diversity
- Main challenge:
  - heterogeneous action interfaces
  - different control frequencies
  - embodiment alignment

Use case:

```text
Cross-Embodiment Pretraining
→ Open X-Embodiment
```

---

### RT-1 (Brohan et al., 2022)

- Single-embodiment robot dataset
- Emphasizes data consistency and hygiene
- Uses a relatively fixed robot platform and action interface
- Suitable for training or fine-tuning when the deployment robot is similar to the training platform

---

### RT-2 (Brohan et al., 2023)

- Combines robot data with large-scale web knowledge
- Introduces broader semantic priors into robot learning
- Useful for transferring semantic knowledge from human-centric or web-scale data to robot control
- Main challenge:
  - grounding semantic knowledge into physically valid robot actions

---

### DROID (Khazatsky et al., 2024)

- Real-world dataset collected using Franka Panda
- Emphasizes in-the-wild data collection
- Increases variation in:
  - backgrounds
  - lighting
  - environments
- Designed to improve perceptual robustness under real-world conditions
- Useful when robustness to environmental variation is important

---

### BridgeData V2 (Walke et al., 2023)

- Collected using WidowX robots
- Uses a relatively standardized and low-cost collection setup
- Emphasizes consistency of action interfaces and data collection
- Suitable for single-platform learning and fine-tuning

---

### RH20T (Fang et al., 2023)

- Multimodal real-world robot dataset
- Includes:
  - vision
  - tactile / force
  - audio
  - robot state
- Particularly useful for contact-rich manipulation
- Addresses cases where vision alone is insufficient

---

### Ego4D (Grauman et al., 2022)

- Large-scale human egocentric interaction video corpus
- Captures human hand-object interactions
- Provides broad semantic and interaction priors
- Does not directly provide robot action labels
- Requires embodiment and action alignment before being used for robot learning

---

## 1.2 Synthetic Datasets

### SynGrasp-1B / GraspVLA (Deng et al., 2025)

- Large-scale synthetic robotic grasping dataset
- Uses extensive procedural and domain randomization
- Generates grasp poses and trajectories in simulation
- Designed for large-scale geometric pretraining
- Main advantage:
  - extremely scalable
  - no equivalent real-world collection cost
- Main limitation:
  - physical realism
  - sim-to-real gap

---

### RoboCasa (Nasiriany et al., 2024)

- Simulator-based household manipulation environment
- Provides:
  - diverse kitchen environments
  - large asset libraries
  - structured task suites
- Supports large-scale synthetic rollout and demonstration collection
- Useful for generalist household manipulation pretraining

---

### RoboGen (Wang et al., 2024c)

- Uses LLMs to propose new robot tasks
- Automatically generates simulation code
- Expands task diversity while reducing manual task authoring
- Can combine different solution strategies such as:
  - reinforcement learning
  - motion planning
  - trajectory optimization
- Main limitation:
  - generated tasks remain dependent on simulation and LLM quality

---

### MimicGen (Mandlekar et al., 2023)

- Scales a small number of human demonstrations through simulation
- Decomposes demonstrations into object-centric subtasks
- Perturbs:
  - object poses
  - initial conditions
- Reuses transformed trajectory segments in new configurations
- Generates 50k demonstrations from 200 human seed demonstrations
- Main strength:
  - demonstration efficiency
- Main limitation:
  - assumes reusable and structured subtasks

---

# 2. VLA Benchmarks

## 2.1 Table-top Benchmarks

### Meta-World (Yu et al., 2021)

- Contains 50 relatively simple manipulation tasks
- Uses a shared table-top setting
- Mainly focuses on:
  - atomic manipulation
  - short-horizon behavior
  - low-level control
- Often uses low-dimensional state observations
- Provides relatively limited long-horizon and visual reasoning difficulty

---

### LIBERO (Liu et al., 2023)

- Table-top benchmark for language-conditioned robot learning
- Most tasks correspond to relatively atomic skills
- Tasks can generally be completed within limited horizons
- Introduces variations in:
  - object types
  - spatial arrangements
- Used for both training and evaluation

Related benchmarks:

- LIBERO-plus (Fei et al., 2025)
  - robustness-oriented extension

- LIBERO-PRO (Zhou et al., 2025)
  - focuses on robust and fair evaluation beyond memorization

- LIBERO-X (Wang et al., 2026)
  - robustness-oriented VLA evaluation

---

### SimplerEnv (Li et al., 2024b)

- Evaluates short-horizon table-top manipulation policies in simulation
- Uses environments that are realistic enough to preserve sim-to-real policy ranking
- Prioritizes reliable policy evaluation over highly complex compositional reasoning
- Main focus:
  - execution reliability
  - sim-to-real evaluation consistency

---

### RoboChallenge (Yakefu et al., 2025)

- Real-world table-top robotic evaluation platform
- Allows online evaluation of embodied policies using physical robots
- Provides an alternative to simulation-only benchmark evaluation

---

### CALVIN (Mees et al., 2022)

- Long-horizon language-conditioned manipulation benchmark
- Requires agents to execute sequences of language instructions
- Includes multiple table-top environments
- Most challenging setting requires zero-shot generalization to an unseen environment
- Main challenges:
  - sustained grounding
  - temporal credit assignment
  - long-horizon execution
- Performance degrades significantly as instruction sequences become longer

---

### GemBench (Garcia et al., 2025)

- Evaluates hierarchical generalization
- Includes:
  - novel object placements
  - unseen object instances
  - compositional long-horizon tasks
- Built within the RLBench simulator
- Shows that strong short-horizon performance does not necessarily transfer to higher task complexity

---

### COLOSSEUM (Pumacay et al., 2024)

- Evaluates robustness under controlled table-top environments
- Introduces systematic visual and physical perturbations
- Uses multiple perturbation axes
- Performance degrades significantly when several perturbation factors are combined
- Shows that single-factor robustness does not necessarily transfer to compounded variability

---

## 2.2 Multi-scene Benchmarks

### BEHAVIOR-1K (Li et al., 2024a)

- Evaluates long-horizon everyday human activities
- Requires coordination of multiple manipulation skills
- Covers:
  - full-room environments
  - multi-room environments
- Supports interactions with:
  - rigid objects
  - deformable materials
  - fluids
- Designed for more realistic and semantically rich embodied tasks

---

### VLABench (Zhang et al., 2024b)

- Language-conditioned manipulation benchmark
- Focuses on:
  - composite tasks
  - multi-step reasoning
  - long-horizon execution
  - scene-semantic reasoning
- Includes diverse:
  - scene types
  - object categories
  - randomized configurations
- Increases both perceptual difficulty and reasoning complexity

---

### Open X-Embodiment (O'Neill et al., 2025)

- Aggregates heterogeneous real-world robot and environment data
- Emphasizes:
  - behavioral breadth
  - cross-embodiment transfer
  - large-scale diversity
- Unlike benchmarks explicitly designed around long-horizon reasoning, it emphasizes scale and embodiment diversity

---

# 3. VLA Data Engines

## 3.1 Video-to-Data Engines

Main idea:

```text
Human / Internet Video
        ↓
Pose or Scene Reconstruction
        ↓
Robot Retargeting
        ↓
Robot Training Data
```

Main challenge:

```text
Human Embodiment
        ↓
Visual Embodiment Gap
        ↓
Robot Embodiment
```

---

### H2R (Li et al., 2026)

- Detects 3D human hand poses from egocentric videos
- Retargets human motions to robot kinematics
- Replaces human hands with rendered robot arms using:
  - segmentation
  - inpainting
- Attempts to bridge the visual embodiment gap between humans and robots
- Preserves original scene context while robotizing human demonstrations

---

### RoboWheel (Zhang et al., 2025b)

- Extends human-to-robot retargeting with physics-aware optimization
- Uses:
  - SDF penalties
  - residual reinforcement learning
- Preserves:
  - contact timing
  - grasp semantics
- Supports cross-embodiment retargeting to:
  - 6/7-DoF robot arms
  - dexterous hands
  - humanoid robots

---

### Video2Policy (Ye et al., 2025)

- Reconstructs structured manipulation tasks from internet videos
- Extracts:
  - object meshes
  - 6D object poses
- Uses GPT-4o to generate executable task code
- Performs iterative refinement of generated tasks
- Supports:
  - automated language annotation
  - simulation task creation
  - sim-to-real transfer

---

### X-Humanoid (Yang et al., 2025)

- Targets whole-body humanoid learning
- Fine-tunes video diffusion models to "robotize" human bodies
- Converts human demonstrations into humanoid videos
- Preserves full-body dynamics
- Uses large-scale human video as a source for humanoid demonstrations

---

### GenMimic (Ni et al., 2025)

- Learns from outputs of video generation models
- Converts synthetic human motion into robot trajectories
- Uses:
  - weighted keypoint tracking
  - symmetry regularization
- Demonstrates zero-shot transfer to physical robots
- Suggests that future robot policies may learn from text-to-video generation without requiring real human demonstrations

---

### UniSim (Yang et al., 2024)

- Learns a conditional video diffusion world model
- Uses:
  - internet images / videos
  - robot data
- Autoregressively simulates long-horizon interactions
- Enables closed-loop VLA policy training
- Demonstrates zero-shot transfer to real robots
- Represents a more general interactive simulator approach

---

## 3.2 Hardware-Assisted Engines

Main idea:

```text
Human Operator
      ↓
Physical Interface / Sensor
      ↓
Action Capture
      ↓
Robot Demonstration
```

Main trade-off:

```text
Precision ↔ Scalability
```

---

### ALOHA (Zhao et al., 2023)

- Low-cost bimanual teleoperation system
- Designed for fine-grained bimanual manipulation
- Uses kinematic similarity between operator interfaces and robot arms
- Combined with ACT action chunking
- Achieves around 80–90% success on selected fine-grained manipulation tasks
- Main limitation:
  - physical teleoperation hardware is still required

---

### GELLO (Wu et al., 2024)

- Low-cost teleoperation framework
- Uses a 3D-printed exoskeleton
- Includes passive joint regularization
- Improves reliability compared with VR-based teleoperation
- Main advantage:
  - very low hardware cost
  - intuitive control
- Main limitation:
  - lab-based collection restricts scene diversity

---

### UMI (Chi et al., 2024)

- Universal Manipulation Interface
- Uses:
  - portable GoPro-equipped gripper
  - SLAM-based trajectory tracking
- Allows demonstration collection without deploying a real robot at every location
- Supports in-the-wild collection
- Demonstrations collected across 30 real-world locations in 12 person-hours
- Around 3× faster than standard teleoperation
- Achieves 71.7% zero-shot success
- Main strength:
  - portable and scalable real-world data collection

---

### DexCap (Wang et al., 2024a)

- Designed for dexterous multi-finger manipulation
- Uses:
  - EMF gloves
  - chest-mounted RGB-D cameras
- Applies:
  - inverse kinematics retargeting
  - point-cloud-based policies
- Enables in-the-wild dexterous demonstration collection
- Achieves around 72% success on multi-finger tasks

---

### Lucid-XR (Ravan et al., 2025)

- Combines XR-based interaction with simulation
- Runs physics simulation directly on VR headsets
- Operates at low latency
- Uses diffusion models to transform rendered observations into photorealistic images
- Produces around 5× effective data compared with real teleoperation
- Improves robustness to environment variation
- Represents a hybrid between hardware-assisted collection and synthetic generation

---

## 3.3 Generative Data Engines

```text
Generative Data Engine
│
├── Trajectory Reuse
├── LLM-driven Generation
├── Visual Augmentation
└── Predictive World Models
```

---

## 3.3.1 Trajectory Reuse

### MimicGen (Mandlekar et al., 2023)

- Segments demonstrations into object-centric subtasks
- Spatially transforms subtrajectories to new object configurations
- Generates 50k demonstrations from 200 human seeds
- Main strength:
  - high demonstration efficiency
- Main limitation:
  - requires known or reusable subtask structure

---

### DynaMimicGen (Pomponi et al., 2025)

- Extends MimicGen to dynamic environments
- Uses Dynamic Movement Primitives
- Adapts trajectories in real time to moving objects
- Addresses the static-object assumption of conventional trajectory reuse

---

### DemoGen (Xue et al., 2025)

- Uses fully synthetic 3D point-cloud editing
- Segments, transforms, and composites object point clouds
- Generates both:
  - observations
  - robot actions
- Does not require repeated real-robot data collection
- Demonstrates real-world transfer from synthetic demonstrations

---

## 3.3.2 LLM-driven Generation

### GenSim (Wang et al., 2024b)

- Uses LLMs to generate robot simulation tasks
- Automatically generates:
  - task code
  - scene configurations
- Reduces manual task design
- Expands the number and diversity of available simulation tasks

---

### RoboGen (Wang et al., 2024c)

- Uses LLMs for automatic task and environment generation
- Generates:
  - task definitions
  - simulation code
  - reward functions
- Uses multiple learning / planning strategies depending on the subtask
- Main strength:
  - automated expansion of task diversity
- Main limitation:
  - physical validity depends on simulation and LLM capability

---

### RoboTwin 2.0 (Chen et al., 2025)

- Extends automated simulation generation with multimodal feedback
- Uses a VLM observer to:
  - monitor simulation execution
  - detect failures
  - provide corrections
- Iteratively refines generated task code
- Uses extensive domain randomization
- Generates 100k+ expert trajectories across five robot platforms
- Main idea:
  - generation + automated visual validation loop

---

## 3.3.3 Visual Augmentation

### ROSIE (Yu et al., 2023)

- Applies text-to-image diffusion to robot demonstrations
- Uses semantic inpainting
- Replaces:
  - objects
  - backgrounds
- Generates visually novel task variations from existing demonstrations
- Main limitation:
  - changes appearance but does not create fundamentally new physical interactions

---

### RoboEngine (Yuan et al., 2025)

- Plug-and-play robot data augmentation toolkit
- Uses Robo-SAM for robot-specific segmentation
- Includes physics-aware background generation
- Reduces dependence on:
  - green screens
  - camera calibration
- Designed to make visual augmentation easier to apply to existing robot datasets

---

### EMMA (Dong et al., 2025)

- Focuses on multi-view consistency
- Uses DreamTransfer
- Generates geometrically coherent observations across multiple camera views
- Supports text-controlled editing of:
  - foregrounds
  - backgrounds
  - lighting
- Addresses inconsistency that can occur when independently augmenting multiple camera views

---

## 3.3.4 Predictive World Models

Main idea:

```text
Current State + Action
          ↓
      World Model
          ↓
Predicted Future State
          ↓
Planning / Training / Evaluation
```

---

### PointWorld (Huang et al., 2026)

- Represents states and actions using 3D point flows
- Focuses on geometric precision
- Supports zero-shot model predictive control
- Main strength:
  - geometric planning
- Main limitation:
  - lacks rich visual textures required by some vision-based policies

---

### IRASim (Zhu et al., 2025)

- Uses trajectory-to-video diffusion
- Conditions predictions on robot actions at the frame level
- Can be used as a learned environment model for evaluation and planning
- Achieves 0.99 correlation with ground-truth simulation
- Improves Push-T performance from 0.637 to 0.961 IoU
- Suggests that learned visual dynamics can reduce expensive real-robot evaluation

---

### 3D-VLA (Zhen et al., 2024)

- Combines 3D multimodal reasoning with generative world modeling
- Generates future goal states in:
  - RGB
  - depth
  - point clouds
- Uses diffusion models aligned with a 3D language model
- Main idea:
  - imagining future 3D states can improve VLA action planning

---

### Genie (Bruce et al., 2024)

- Learns from 200k hours of internet videos
- Discovers latent actions without robot action labels
- Uses unsupervised latent action discovery
- Suggests that large-scale web video can bootstrap interactive world models
- Main limitations:
  - around 1 fps generation
  - 16-frame temporal memory
  - limited real-time applicability

---

# 4. Comparison Summary

## Datasets

| Work | Category | Core Idea | Main Limitation |
|---|---|---|---|
| Open X-Embodiment | Real-World | Cross-embodiment aggregation | Action / embodiment alignment |
| DROID | Real-World | In-the-wild diversity | Real-world collection cost |
| RH20T | Real-World | Multimodal contact data | Limited scale |
| SynGrasp-1B | Synthetic | Billion-scale grasp data | Sim-to-real gap |
| RoboCasa | Synthetic | Household simulation | Simulation fidelity |
| MimicGen | Synthetic | Demonstration augmentation | Structured subtask assumption |

---

## Benchmarks

| Work | Environment | Main Focus |
|---|---|---|
| Meta-World | Table-top | Atomic manipulation |
| LIBERO | Table-top | Short-horizon language-conditioned tasks |
| CALVIN | Table-top | Long-horizon sequential instructions |
| GemBench | Table-top | Hierarchical generalization |
| COLOSSEUM | Table-top | Robustness to perturbations |
| BEHAVIOR-1K | Multi-scene | Everyday long-horizon activities |
| VLABench | Multi-scene | Compositional reasoning |

---

## Data Engines

| Approach | Representative Works | Strength | Limitation |
|---|---|---|---|
| Video-to-Data | H2R, RoboWheel, Video2Policy | Leverages web-scale human video | Reconstruction / embodiment gap |
| Hardware-Assisted | ALOHA, GELLO, UMI, DexCap | Physically grounded demonstrations | Hardware / human collection cost |
| Trajectory Reuse | MimicGen, DynaMimicGen, DemoGen | Data-efficient scaling | Structured task assumptions |
| LLM-driven | GenSim, RoboGen, RoboTwin 2.0 | Automatic task generation | Simulation / LLM dependent |
| Visual Augmentation | ROSIE, RoboEngine, EMMA | Visual diversity | Cannot create new physics |
| World Models | PointWorld, IRASim, 3D-VLA, Genie | Prediction and planning | Dynamics / grounding alignment |

---

# 5. Key Relationships

## Real-World vs Synthetic Data

```text
Real-World Data
├── High Physical Fidelity
└── High Collection Cost

Synthetic Data
├── High Scalability
└── Sim-to-Real / Physical Realism Gap
```

Practical direction:

```text
Synthetic Pretraining
        ↓
Real-world Calibration
        ↓
Deployment
```

---

## Benchmark Difficulty

```text
Task Complexity
Simple → Long-horizon / Compositional

Environment Structure
Table-top → Multi-scene
```

Increasing both dimensions improves realism but makes failure attribution harder.

---

## Data Engine Scaling

```text
Generation Capacity
       ↑↑↑

Physical Grounding
Verification
Embodiment Alignment
       ↑
```

The main challenge is not only generating more data, but ensuring that generated data remains physically valid and transferable.

---

# 6. Takeaway

The representative works in this survey follow one common direction:

```text
More Data
   ↓
More Diversity
   ↓
More Generalization
```

but increasing scale introduces new problems:

```text
Embodiment Alignment
Physical Grounding
Sim-to-Real
Reasoning Evaluation
Verification
```

Therefore, the important question is not simply:

> How can we generate more robot data?

but:

> How can we generate diverse and scalable robot data while preserving physical validity, embodiment alignment, and real-world transferability?