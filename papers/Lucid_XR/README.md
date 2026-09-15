# Lucid-XR

## 0. Paper Information

- Title: Lucid-XR: An Extended-Reality Data Engine for Robotic Manipulation
- Authors: Yajvan Ravan, Adam Rashid, Alan Yu, Kai McClennen, Gio Huh, Kevin Yang, Zhutian Yang, Qinxi Yu, Xiaolong Wang, Phillip Isola, Ge Yang
- Year: 2026
- Venue: arXiv preprint
- Paper: https://arxiv.org/abs/2605.00244
- Code: Coming Soon
- Project: https://lucidxr.github.io/

---

## 1. One-line Summary

> Lucid-XR is an XR-based robotic data engine that collects human demonstrations through on-device physics simulation and transforms them into diverse, realistic synthetic data for training real-world robot manipulation policies.

---

## 2. Why this Paper?

### Problem

- Collecting large-scale real-world robot demonstrations is expensive and time-consuming.

- Digitally creating millions of realistic-looking virtual worlds at the scale required for robots to generalize to the real world is also prohibitively expensive.

- Virtual demonstrations collected in simple and sparsely populated 3D environments alone are insufficient for training real-world visual policies.

- Existing XR / teleoperation systems often rely on external computers or servers for:
  - physics simulation
  - kinematics computation
  - human-to-robot pose retargeting

- Network communication introduces latency and bandwidth bottlenecks.
  - This becomes particularly problematic for dynamic, deformable, and contact-rich manipulation.

- Retargeting human poses to robot embodiments with different kinematic structures often requires:
  - robot-specific custom code
  - a separate kinematics server
  - additional system configuration

- These requirements make internet-scale crowdsourcing of robot demonstrations difficult.

### Motivation

- Human demonstrations could be collected cheaply and safely inside XR simulation instead of requiring a physical robot for every demonstration.

- Running physics simulation directly on the XR device can:
  - remove network latency
  - eliminate the need for a separate simulation server
  - enable untethered interaction
  - make demonstration collection easier to scale through the internet

- The simulated environment itself does not need to be photorealistic if its physical trajectories can later be transformed into visually realistic data.

- Generative models can provide visual diversity while the physics simulator preserves:
  - geometry
  - contact
  - trajectory
  - robot behavior

- Lucid-XR therefore separates two problems:

```text
Behavior / Physics
        ↓
collect in simulation

Visual Appearance
        ↓
diversify with generative models
```

### Main Contribution

1. **On-Device Physics Simulation**
   - Move physics simulation directly onto XR devices.
   - Run MuJoCo through the web browser using WebAssembly.
   - Reduce latency and enable untethered multi-physics interaction.

2. **Human-to-Robot Pose Retargeting**
   - Retarget human motion to virtual robots without requiring a custom program and external kinematics server for every embodiment.
   - Use MoCap sites and inverse kinematics to define robot control through a schema-based interface.

3. **Synthetic Data Generation for Robot Learning**
   - Convert low-fidelity virtual demonstrations into diverse and realistic visual training data.
   - Combine generative imagery with camera and trajectory augmentation.
   - Demonstrate transfer of policies trained using synthetic data to realistic and real-world environments.

---

## 3. Key Concepts

### Lucid-XR

- Extended-Reality data engine for robotic manipulation.

- Main goal:
  - collect scalable human demonstrations in XR
  - preserve physically valid behavior
  - augment demonstrations into diverse visual training data
  - train robot manipulation policies
  - transfer the learned policies to real environments

---

### Vuer

- Core XR framework used by Lucid-XR.

- Simulator-agnostic XR framework running directly inside a web browser.

- Handles:
  - XR interaction
  - rendering
  - physics simulation
  - human input
  - robot pose retargeting

---

### On-Device Physics Simulation

- Physics simulation is executed directly on the XR headset instead of an external computer.

```text
Conventional XR

XR Device
    ↓ hand pose
Network
    ↓
External Physics Server
    ↓ updated scene
Network
    ↓
XR Device
```

```text
Lucid-XR

XR Device
 ├─ Vuer
 ├─ MuJoCo
 ├─ Physics
 └─ Rendering
```

- Advantages:
  - reduced network latency
  - no separate simulation server
  - lower communication bandwidth requirement
  - responsive interaction with dynamic and deformable objects
  - easier deployment to many XR users

---

### Multi-Physics Simulation

Lucid-XR demonstrates support for:

- rigid-body contact
- flexible / deformable materials
- granular particles
- fluid / wind forces
- non-convex collision
- self-contact
- articulated objects

---

### WebAssembly

- MuJoCo is compiled into WebAssembly.

- Purpose:
  - bypass the single-threaded browser V8 engine
  - achieve near-native simulation performance directly on XR hardware

---

### WebXR

- Browser standard for XR interaction.

- Enables support for:
  - hand tracking
  - motion controllers
  - different XR headsets

- Makes the system less dependent on a particular XR vendor.

---

### WebGL

- Used for real-time 3D rendering inside the browser.

- Lucid-XR builds its rendering and interaction front-end using `react-three/fiber`.

---

### SE(3)

- Represents a rigid-body pose consisting of:

```text
SE(3)
 ├─ Translation
 │   └─ x, y, z
 │
 └─ Rotation
```

- Lucid-XR records robot actions and observations as SE(3) MoCap poses.

- This provides a task-space representation rather than a robot-specific joint-space representation.

---

### Pose Retargeting

- Converts human motion into robot-compatible motion.

```text
Human Hand Motion
        ↓
MoCap Sites
        ↓
Target SE(3) Pose
        ↓
Inverse Kinematics
        ↓
Robot Motion
```

- Helps make demonstrations less dependent on one particular robot embodiment.

---

### Hitchhiking Controller

- Inspired by *Hitchhiking Hands*.

- Problem:
  - directly controlling a distant robot gripper in XR amplifies hand-tracking errors.

- Solution:
  - select a distant MoCap site
  - attach local human hand movement to that target
  - manipulate it through natural gestures

- Allows more precise interaction with distant virtual robots.

---

### 6D Rotation Representation

- Rotations are represented using the continuous 6D representation.

- Useful for neural-network-based policy learning because it avoids problematic discontinuities found in some alternative rotation parameterizations.

---

### Generative Visual Augmentation

- Converts visually simple simulation observations into diverse and realistic-looking observations.

- Uses:
  - text prompts
  - semantic object masks
  - normalized depth
  - robot overlays

---

### Demonstration Augmentation

- Existing demonstrations can be modified after collection.

- Includes:
  - camera repositioning
  - object repositioning
  - robot repositioning
  - trajectory warping
  - visual appearance generation

- This allows one demonstration to produce many training examples.

---

## 4. Method / Overview

Lucid-XR can be summarized as the following pipeline:

```text
Scene / Assets
      ↓
Vuer + MuJoCo
      ↓
On-Device Physics Simulation
      ↓
XR Human Interaction
      ↓
Human-to-Robot Pose Retargeting
      ↓
Virtual Demonstration
      ↓
 ┌─────────────────────────────┐
 │ Demonstration Augmentation  │
 │                             │
 │ - Camera Repositioning      │
 │ - Object Repositioning      │
 │ - Robot Repositioning       │
 │ - Trajectory Warping        │
 └─────────────────────────────┘
      ↓
Generative Image Pipeline
      ↓
Diverse + Realistic Multi-view Data
      ↓
Robot Policy Learning
      ↓
ACT / Diffusion Policy
      ↓
Sim-to-Real Evaluation
```

The overall system can be understood as three stages.

### Stage 1. Collect Physical Behavior

- Human operators interact with virtual environments through XR.

- Physics runs directly on the XR device.

- Human motion is retargeted to the virtual robot.

- The output is physically grounded demonstration trajectories.

---

### Stage 2. Multiply the Demonstrations

- Existing trajectories can be modified without recollecting demonstrations.

- Lucid-XR changes:
  - camera viewpoints
  - object locations
  - robot locations
  - initial scene configurations

- A small number of demonstrations can therefore produce a much larger dataset.

---

### Stage 3. Increase Visual Diversity

- Low-fidelity simulated images are transformed using generative models.

- Physical trajectories remain grounded in simulation while visual appearance changes.

- The resulting dataset contains diverse:
  - backgrounds
  - lighting
  - textures
  - object appearances
  - camera viewpoints

---

## 5. Synthetic Data Generation / Demonstration Augmentation

### 5.1 Generating Realistic Images from Virtual Demonstrations

Lucid-XR follows the LucidSim-style image generation approach.

```text
Text Prompt
      +
Semantic Object Masks
      +
Normalized Depth
      +
Robot Overlay
      ↓
Generative Image Pipeline
      ↓
Realistic Synthetic Observation
```

- Diverse prompts are generated at scale using ChatGPT.

- Separate prompts can describe:
  - background
  - individual objects
  - negative conditions

- Semantic masks obtained from simulation constrain:
  - object identity
  - object location
  - scene composition

- Normalized depth provides geometric constraints.

- Robot overlays preserve the robot configuration.

- Main idea:

```text
Physics / Trajectory
        ↓
remain consistent

Appearance
        ↓
becomes diverse
```

---

### 5.2 Procedural Scene Generation

- Lucid-XR provides a Python interface for procedurally generating MuJoCo XML scenes.

- This makes it possible to systematically vary initial states.

- Users can control distributions over:
  - object positions
  - scene configurations
  - robot positions

- This is useful for controlling the training-data distribution rather than manually constructing every scene.

---

### 5.3 Repositioning Cameras Post-Demonstration

- Camera poses can be modified after the demonstration has already been collected.

```text
One Demonstration
      ↓
Replay Trajectory
      ↓
Camera 1
Camera 2
Camera 3
...
      ↓
Multiple Views
```

- No new human demonstration is required.

- Simulator information includes:
  - camera intrinsics
  - camera extrinsics
  - ground-truth depth

- These can be used to compute optical flow for nearby camera poses.

- Main goal:
  - reduce sensitivity to one particular camera configuration
  - increase multi-view training data
  - improve sim-to-real robustness

---

### 5.4 Trajectory Warping for Repositioning Objects and Robots

- Inspired by MimicGen.

- Keypoints are selected from existing demonstration trajectories.

- Keypoints are moved according to a predefined distribution.

- New trajectories are generated using:
  - linear interpolation for position
  - spherical interpolation for rotation

```text
Original Demonstration
        ↓
Select Keypoints
        ↓
Move Object / Robot / Target
        ↓
Transform Keypoints
        ↓
Interpolate
        ↓
New Demonstration
```

- Enables:
  - object repositioning
  - robot repositioning
  - changes in initial scene configuration

- Main goal:
  - generate more demonstrations from a small source dataset
  - improve robustness to object-position variation

---

## 6. Task / Environment Setup

### Manipulation Tasks

| Task | Description | Main Physics Challenge |
|---|---|---|
| Block Stacking | Create a three-block stack using a dexterous hand | Dexterous contact |
| Pour Liquid | Pick up a cup, hand it to another hand, and pour into a sink | Granular particle flow + bimanual interaction |
| Ball Sorting | Sort three colored balls using a toy sorter | Rigid-body + particle collision |
| Knot Tying | Tie a knot on a suspended rope using a two-finger gripper | Flexible material + self-contact |
| Kitchen-Sink | Stack a cup on a bowl and place both into a sink | Long-horizon manipulation + large scene + SDF collision |
| Mug Tree | Pick up a mug and hang it on a drying rack | Concave-shape contact + SDF collision |

---

### Demonstration Representation

- Observations and actions are recorded as:
  - SE(3) MoCap poses
  - 25 Hz

- Rotation:
  - continuous 6D representation

- Demonstrations are designed to be relatively embodiment-agnostic.

- The task-space representation allows behavior-cloned policies to transfer across compatible two-finger grippers more easily than robot-specific joint trajectories.

---

### Policy Observation

The policy receives:

```text
Robot Proprioception
        +
Visual Observation
```

Visual input is either:

```text
Wrist RGB
```

or:

```text
Three Fixed RGB Cameras
```

- Wrist camera:
  - useful for local manipulation and close-range contact

- Fixed multi-view cameras:
  - provide broader workspace information
  - reduce occlusion
  - provide global scene context

---

### Policy Action

- Output:
  - chunked absolute end-effector poses

```text
Observation
     ↓
Policy
     ↓
Future End-Effector Pose Chunk
     ↓
Robot Execution
```

---

### ACT

Lucid-XR uses standard Action Chunking Transformer (ACT).

Main-text configuration:

- 15k updates
- chunk size: 25
- learning rate: `1e-4`
- batch size: 64
- DETR-style VAE backbone
  - 4 encoders
  - 1 decoder
  - head dimension: 128
  - FFN dimension: 256
- image augmentation:
  - color jitter
- evaluation:
  - temporal aggregation

At 25 Hz, a chunk size of 25 corresponds to approximately one second of action predictions.

---

### Diffusion Policy

Lucid-XR also trains a score-based action denoiser.

Architecture:

```text
Image Observation
       ↓
Image Features
       ↓
FiLM Conditioning
       ↓
1D U-Net
       ↓
Action Denoising
       ↓
Action Chunk
```

- Optimizer:
  - AdamW

- Learning-rate schedule:
  - exponential schedule from `1e-3` to `1e-5`

- Inference:
  - 1000 denoising steps
  - actions executed in chunks

---

### Reproducibility Note

There is a discrepancy between the main-text ACT settings and the Appendix training table.

Main text:

| Hyperparameter | Value |
|---|---:|
| Learning Rate | 1e-4 |
| Batch Size | 64 |
| Encoder Layers | 4 |
| Decoder Layers | 1 |
| Head Dimension | 128 |
| FFN Dimension | 256 |
| Chunk Size | 25 |

Appendix Table 2:

| Hyperparameter | Value |
|---|---:|
| Learning Rate | 5e-5 |
| Batch Size | 32 |
| Encoder Layers | 4 |
| Decoder Layers | 7 |
| Feedforward Dimension | 3200 |
| Hidden Dimension | 512 |
| Number of Heads | 8 |
| Chunk Size | 10 |
| KL Weight | 10 |
| Dropout | 0.1 |

Therefore, exact reproduction would require checking the released implementation or clarification from the authors rather than relying on only one of these descriptions.

---

## 7. Important Models / Datasets / Methods

| Method / System | Role in Lucid-XR |
|---|---|
| Vuer | Browser-based XR framework and core interface |
| MuJoCo | Physics simulation and inverse kinematics |
| WebAssembly | Runs MuJoCo efficiently inside the browser |
| WebXR | XR device / hand / controller interaction |
| WebGL | Real-time browser rendering |
| react-three/fiber | 3D rendering and interaction front-end |
| LucidSim | Basis of the generative image augmentation pipeline |
| MimicGen | Inspiration for trajectory warping |
| ACT | Action-chunking imitation-learning policy |
| Diffusion Policy | Generative action-sequence policy |
| DETR-style VAE | Backbone used by ACT |
| 1D U-Net | Action denoising network |
| FiLM | Conditions the diffusion model on image features |
| Semantic Masking | Controls object identity and scene composition during image generation |
| Depth Conditioning | Provides scene-geometry constraints |
| SE(3) Retargeting | Maps human / MoCap motion to robot task-space motion |
| 6D Rotation Representation | Continuous representation for rotation learning |
| SDF Collision | Handles non-convex object collision without convex decomposition |

---

## 8. Experiments

### 8.1 Experimental Goals

The experiments evaluate three main questions:

1. Can Lucid-XR support diverse contact-rich physics in XR?
2. Can virtual demonstration collection produce data more efficiently than real-world teleoperation?
3. Can policies trained using synthetic Lucid-XR data generalize to realistic and real-world environments?

---

### 8.2 Data Collection Efficiency

The authors collected 30 minutes of demonstrations for three tasks using:

- Lucid-XR
- real-world teleoperation

Real-world collection requires:

- manually resetting objects
- repositioning the robot
- safety checks

Lucid-XR allows the user to reset the complete environment immediately inside simulation.

### Result

- Lucid-XR produced roughly **2× more demonstrations** than real-world teleoperation during the same collection time.

- After applying the augmentation pipeline, the effective dataset size became approximately **5× the real-world baseline**.

```text
Real-World Teleoperation
        ↓
Manual Reset + Safety Checks
        ↓
Lower Throughput

Lucid-XR
        ↓
Instant Virtual Reset
        ↓
~2× Demonstrations
        ↓
Data Augmentation
        ↓
~5× Effective Dataset
```

---

### 8.3 Real-to-Sim Evaluation

- Real-world kitchens were scanned and converted into 3D Gaussian representations.

- These realistic scenes were aligned with the simulated environment.

- The goal was to evaluate whether a policy trained in simple virtual scenes could generalize to realistic clutter and appearance.

### Kitchen Clearing Results

| Policy | Base Environment | Low Clutter | High Clutter + Noise |
|---|---:|---:|---:|
| ACT | 100% | 0% | 0% |
| ACT + LucidSim | 100% | 90% | 25% |

### Interpretation

- Standard simulated-image training works well in the original environment but collapses when visual conditions change.

- Generative visual augmentation dramatically improves robustness to unseen clutter.

- This indicates that visual diversity is critical for transferring a manipulation policy beyond its original simulated appearance distribution.

---

### 8.4 Sim-to-Real Evaluation

The authors collected datasets for:

- 10 minutes
- 20 minutes
- 30 minutes

For each collection duration:

```text
Lucid-XR Demonstrations
        ↓
Generative Rendering
        ↓
Synthetic Training Dataset
```

and

```text
Real Robot Teleoperation
        ↓
Real Training Dataset
```

were compared.

Policies were then evaluated on a real robot.

### Base Environment

- Policies trained entirely using Lucid-XR synthetic data performed comparably to policies trained on real-world demonstrations.

---

### Visual Distribution Shift

Evaluation environments were modified by changing:

- lighting
- colors
- tabletop appearance
- textured tablecloth
- black tablecloth

### Result

- Policies trained only on real-world demonstrations failed to generalize well under these visual changes.

- Lucid-XR-trained policies maintained significantly stronger performance.

### Key Interpretation

```text
More "real" training data
does not automatically mean
better visual generalization.

Synthetic diversity
        ↓
can improve robustness
to unseen appearances.
```

---

## 9. Strengths / Pros

### 1. Scalable Data Collection Architecture

- Removes the requirement for every demonstration collector to have:
  - a robot
  - a workstation
  - a dedicated simulation server

- Physics runs directly on the XR device.

- This creates a potential path toward internet-scale demonstration collection.

---

### 2. Separates Physics from Appearance

One of the most important ideas of the paper is:

```text
Physics
↓
Simulator

Appearance
↓
Generative Model
```

- The simulator does not need to render perfectly realistic scenes.

- It mainly needs to produce physically meaningful interactions.

- Generative models can then create visual diversity.

---

### 3. Post-Hoc Data Augmentation

- Demonstrations do not need to be recollected whenever:
  - camera position changes
  - object position changes
  - robot position changes
  - visual appearance changes

- Existing trajectories can be reused.

---

### 4. Supports Complex Physics

- Demonstrates:
  - deformable objects
  - ropes
  - particles
  - fluid forces
  - rigid-body contact
  - concave collision
  - dexterous manipulation

- Goes beyond simple pick-and-place simulation.

---

### 5. Strong Sim-to-Real Motivation

- The system is explicitly designed around deployment beyond simulation.

- Evaluation includes:
  - clutter
  - lighting changes
  - texture changes
  - realistic environment scans
  - real robot evaluation

---

### 6. Policy-Agnostic Data Engine

- Lucid-XR is not tied to one policy architecture.

- The authors evaluate both:
  - ACT
  - diffusion-based policy

- This strengthens the argument that the main contribution is the data pipeline rather than a specific policy model.

---

### 7. Embodiment-Aware but Less Embodiment-Dependent Data

- Storing behavior using end-effector-level SE(3) trajectories reduces dependence on robot-specific joint configurations.

- This creates a possible path toward cross-embodiment data reuse.

---

## 10. Limitations / Cons

### Paper-Stated Limitation

- Multi-view image consistency relies heavily on using the same text prompt across generated views.

- Maintaining consistent generative appearance across multiple camera views remains challenging.

- Generated visual data naturally comes with paired text labels, but the current learning pipeline does not fully exploit this additional supervision.

---

### Current Scale vs. Long-Term Vision

- The paper proposes internet-scale crowdsourcing.

- However, the experiments in the paper use demonstrations collected by the authors rather than demonstrating actual internet-scale crowdsourced data collection.

- Therefore:

```text
Current Work
    ≠
Internet-Scale Demonstration Dataset

Current Work
    =
Proof of Concept for an architecture
that could scale toward that direction
```

---

### Hand-Crafted Simulation Scenes

- The current experiments still require basic hand-crafted 3D scenes.

- This means scene construction has not yet been fully automated.

---

### Generative Multi-View Consistency

- Independent image generation can introduce inconsistencies across:
  - camera views
  - frames
  - object textures
  - lighting

- This becomes increasingly important when policies use multiple synchronized camera observations.

---

### Synthetic 3D Asset Engineering

- Automatically generated 3D assets can contain:
  - excessive mesh complexity
  - incorrect physical scale

- The authors report post-processing assets using:
  - MeshLab simplification
  - centering
  - rescaling

- Therefore, fully automatic environment generation still requires engineering work.

---

### Cross-Embodiment Transfer Is Not Solved

- Task-space demonstrations reduce embodiment dependence.

- However, actual transfer remains constrained by:
  - inverse kinematics
  - robot mobility
  - reachable workspace
  - end-effector capabilities

- Cross-embodiment transfer is identified as future work.

---

### Hyperparameter Reproducibility

- Training details in the main text and Appendix are not fully consistent.

- Exact reproduction therefore depends on access to the released implementation.

---

## 11. Trade-offs

### On-Device Simulation vs. External Simulation Server

```text
On-Device
+ low latency
+ no network bottleneck
+ scalable deployment
- limited compute
- limited memory
```

```text
External Server
+ larger compute budget
+ more complex simulation possible
- network latency
- communication bottleneck
- harder to scale
```

---

### Low-Fidelity Simulation + GenAI vs. Photorealistic Simulation

```text
Photorealistic Simulation
+ direct visual realism
- expensive to build
- difficult to scale
```

```text
Lucid-XR
Low-Fidelity Physics
        +
Generative Appearance
        ↓
+ cheaper scene construction
+ large visual diversity
- generative consistency challenges
```

---

### SDF Collision vs. Convex Decomposition

SDF:

- easier modeling of non-convex geometry
- removes manual convex decomposition

but:

- requires higher runtime compute
- requires more memory

---

### Single-View vs. Multi-View Observation

Single / wrist camera:

- lower computational cost
- detailed local manipulation view

Multi-view:

- better global information
- less occlusion

but:

- higher compute
- larger dataset
- greater multi-view consistency requirements

---

### Demonstration Augmentation vs. Physical Validity

- Trajectory warping generates large amounts of data cheaply.

- However, increasingly aggressive transformations may produce trajectories that are less physically valid.

- The augmentation distribution therefore needs to remain compatible with task geometry and robot constraints.

---

### Visual Diversity vs. Visual Consistency

- Generative models provide large appearance diversity.

- More aggressive generation may also introduce:
  - temporal inconsistency
  - multi-view inconsistency
  - unrealistic object appearance

- There is a trade-off between:

```text
Diversity
   ↕
Consistency
```

---

## 12. Key Findings

1. **On-device XR physics simulation is feasible.**
   - MuJoCo can run interactively inside modern XR browsers through WebAssembly.

2. **Virtual demonstration collection can be more efficient than physical teleoperation.**
   - Lucid-XR collects roughly 2× more demonstrations within the same collection time.

3. **Post-hoc augmentation can significantly increase effective dataset size.**
   - Augmentation increases the effective dataset to approximately 5× the real-world baseline.

4. **Visual diversity is important for sim-to-real generalization.**
   - Policies trained only on visually simple simulation data fail under visual distribution shift.

5. **Synthetic training data can compete with real-world demonstration data.**
   - Policies trained entirely with Lucid-XR synthetic data perform comparably to real-data policies in the base environment.

6. **Synthetic diversity can outperform real-data training under visual changes.**
   - Lucid-XR policies remain robust when:
     - lighting changes
     - colors change
     - backgrounds change
     - tabletop textures change

7. **Robot-data scaling does not necessarily require photorealistic physics simulation.**
   - Physical correctness and visual realism can be addressed by separate components.

8. **Task-space demonstration representation provides a useful path toward embodiment-independent robot data.**

---

## 13. Future Work / Open Challenges

### Internet-Scale Demonstration Collection

- The architecture is designed for internet-scale deployment.

- A major next step is validating the system with:
  - large numbers of users
  - diverse devices
  - diverse robot embodiments
  - distributed demonstration collection

---

### Cross-Embodiment Transfer

- Study whether the same demonstration dataset can be transferred across:
  - different robot arms
  - different grippers
  - dexterous hands
  - mobile manipulators
  - humanoids

- Current transfer remains limited by:
  - inverse kinematics
  - mobility
  - embodiment-specific capabilities

---

### Better Multi-View Generative Consistency

- Improve consistency of:
  - object identity
  - texture
  - lighting
  - geometry

across different cameras and frames.

---

### Language Supervision

- Generated data naturally includes paired language prompts.

- These labels could potentially be used as additional supervision.

```text
Synthetic Image
      +
Text Description
      +
Robot Action
```

- This creates a possible connection toward multimodal robot learning and VLA-style training.

---

### Automated Scene Generation

- Reduce dependence on manually constructed MuJoCo environments.

- Potential goal:

```text
Language / Image / Scan
        ↓
Automatic 3D Environment
        ↓
Physics Setup
        ↓
Robot Demonstration Collection
```

---

### More Complex Physics

- Future WebGPU support could enable:
  - hardware-accelerated compute shaders
  - larger particle simulations
  - more complex deformable objects
  - liquids
  - richer contact-rich environments

---

### Long-Horizon Manipulation

- Current tasks demonstrate several contact-rich interactions.

- Future systems could investigate:
  - longer sequences
  - multi-stage tasks
  - planning
  - recovery behavior
  - compositional manipulation

---

## 14. My Takeaway

- The most important idea of Lucid-XR is not simply using XR for robot teleoperation.

- The key idea is to **separate the collection of physically meaningful behavior from the creation of visually realistic observations**.

```text
Simple Simulation
      ↓
Collect Physically Valid Behavior
      ↓
Reuse / Warp Demonstrations
      ↓
Generate Visual Diversity
      ↓
Train Robust Policy
      ↓
Real Robot
```

- This changes the role of simulation.

- Instead of asking:

> "How can we construct a simulation that perfectly looks like the real world?"

Lucid-XR asks:

> "Can we cheaply collect correct behavior in simulation and create realism afterward?"

- This is particularly interesting because large-scale robot learning is fundamentally constrained by data collection cost.

- Lucid-XR treats this as a **robot data engine problem**, rather than only a policy-learning problem.

- Another important lesson is that **more real data does not automatically produce better generalization**.

- A deliberately diversified synthetic dataset can outperform narrowly distributed real-world data when the evaluation environment changes.

---

## 15. Connection to My Research

Lucid-XR is highly relevant to my current robot-learning research environment because the core components closely match the infrastructure available in Optim. Lab.

### Available Research Stack

```text
XR
└─ Meta Quest 2

Simulation
├─ MuJoCo
└─ robosuite

Robot
├─ UFACTORY xArm7
├─ UFACTORY Gripper
└─ INSPIRE RH56E2 Dexterous Hand

Learning
├─ PyTorch
├─ Imitation Learning
├─ Reinforcement Learning
└─ Robot Policy Learning
```

---

### Possible Lucid-XR-Inspired Research Pipeline

```text
Quest 2 Teleoperation
        ↓
Human Motion / Controller Pose
        ↓
SE(3) End-Effector Target
        ↓
Retargeting / IK
        ↓
MuJoCo xArm7
        ↓
Virtual Demonstration
        ↓
Data Augmentation
        ↓
 ┌──────────────────────┐
 │ Object Pose          │
 │ Camera Pose          │
 │ Initial State        │
 │ Visual Appearance    │
 └──────────────────────┘
        ↓
Policy Learning
        ↓
ACT / Diffusion Policy
        ↓
Real xArm7
        ↓
Sim-to-Real Evaluation
```

---

### Observation Design

A possible initial setup:

```text
Observation
├─ External RGB Camera
├─ Wrist RGB Camera
├─ End-Effector Pose
├─ Joint State
└─ Gripper State
```

This would allow experiments comparing:

```text
Wrist Only
vs.
External Camera
vs.
Multi-View
```

---

### Action Representation

A Lucid-XR-style task-space representation could be:

```text
Action
├─ x
├─ y
├─ z
├─ 6D Rotation
└─ Gripper Command
```

This is preferable to storing only xArm7 joint trajectories if future work aims to investigate:

- cross-embodiment learning
- different grippers
- dexterous hands
- dual-arm manipulation

---

### Evaluation Protocol

Rather than evaluating only on the original training scene, experiments should include distribution shifts.

```text
In-Distribution
        ↓
Object Position Shift
        ↓
Camera Shift
        ↓
Lighting Shift
        ↓
Background / Texture Shift
        ↓
Clutter Shift
        ↓
Novel Object Instance
        ↓
Sim-to-Real
```

Possible evaluation metrics:

- task success rate
- completion time
- number of retries
- trajectory error
- grasp success
- robustness under visual shift
- robustness under object-position shift

---

### Research Questions Inspired by Lucid-XR

1. How much real robot data can be replaced by XR-generated demonstrations?

2. How much does trajectory augmentation improve generalization?

3. Which augmentation is most important?
   - object pose
   - camera pose
   - visual appearance
   - trajectory warping

4. How much does multi-view vision improve manipulation robustness?

5. Can task-space demonstrations collected for xArm7 transfer to another embodiment?

6. Can demonstrations collected using a two-finger gripper be reused for a dexterous hand?

7. Does generative visual augmentation outperform conventional domain randomization?

8. How does synthetic-to-real performance scale with the number of source demonstrations?

9. Can tactile information from a dexterous hand be combined with Lucid-XR-style visual demonstration data?

10. Can dual-arm demonstration data be collected efficiently in XR and transferred to real dual-arm manipulation?

---

## 16. Section Notes

<details>
<summary>Section-by-Section Reading Notes</summary>

### Section 1. Introduction

- Lucid-XR:
  - extended-reality data engine for robot manipulation

- Core idea:
  - collect human demonstrations in low-fidelity virtual environments
  - transform them into diverse and realistic visual robot training data

- Long-term vision:
  - internet-scale deployment of real-time physics simulation
  - crowdsourcing of human demonstrations through XR devices

- Key problems:
  - real robot data collection is expensive
  - photorealistic virtual environment construction is expensive
  - simple virtual environments lack sufficient visual diversity
  - human-to-robot pose retargeting often requires custom systems

- Lucid-XR combines:
  - XR demonstration collection
  - on-device physics
  - pose retargeting
  - generative visual augmentation

---

### Section 2. A Touch of Physics in Extended Reality (XR)

#### Three Web Standards

1. **WebAssembly**
   - compile MuJoCo into WebAssembly
   - bypass the single-threaded V8 engine
   - achieve near-native simulation speed

2. **WebXR**
   - common interface across XR devices
   - supports:
     - hand tracking
     - motion controllers
     - multiple XR devices

3. **WebGL**
   - real-time browser rendering
   - implemented using react-three/fiber

---

#### 2.1 Multi-Physics Simulation in Vuer

- Core framework:
  - `vuer`

- Simulator-agnostic XR framework running inside the browser.

- MuJoCo compiled to WebAssembly.

- Reported performance:
  - 90 fps rendering on Apple Vision Pro
  - demonstrations recorded at 25 fps
  - simulation step under 12 ms

- Main advantages:
  - no external simulation server
  - lower latency
  - reduced bandwidth bottleneck
  - support for dynamic and deformable interactions

---

#### Flexible Materials

- External physics servers require large mesh updates to be transferred through WiFi.

- This becomes a bottleneck for:
  - deformable objects
  - particle-rich scenes

- On-device physics removes this communication bottleneck.

---

#### Fluid Forces

- MuJoCo integrated fluid model.

- Supports:
  - wind
  - air resistance
  - rigid objects
  - deformable objects

---

#### Collision without Convex Decomposition

- Uses MuJoCo SDF collision solver.

- Advantage:
  - no manual convex decomposition required

- Trade-off:
  - more runtime computation
  - greater memory usage

---

#### 2.2 Precise Interactions at a Distance: Hitchhiking Controllers

- Problem:
  - directly controlling distant robot grippers amplifies hand-tracking error.

- Solution:
  - apply SE(3) transformation to target gripper in local MoCap frame.

- Inspired by:
  - *Hitchhiking Hands*
  - SIGGRAPH Asia 2023 Emerging Technologies

- Interaction:
  - gaze at target
  - activate MoCap site
  - control through natural grasp gesture

---

#### 2.3 On-Device Retargeting for Dexterous Hand Control

- Human and robot hands have different kinematics.

- Previous systems often require external kinematics servers.

- Lucid-XR performs retargeting directly on-device.

- MoCap sites are associated with:
  - fingertips
  - wrist

- Relative fingertip poses with respect to the wrist are used for control.

- Schema-based interface allows users to specify custom bindings between:
  - MoCap sites
  - robot bodies
  - landmarks
  - gestures

---

#### 2.4 Porting Existing Environments

Existing MuJoCo environments can be moved into Vuer.

Examples:

- RoboHive
- RoboCasa
- RoboSuite
- MuJoCo Menagerie

- XML and assets can be extracted from the original environments and loaded into Vuer.

---

### Section 3. Synthesizing Diverse Manipulation Data from Virtual Demonstrations

- Third major component:
  - generative synthetic data engine

- Purpose:
  - convert virtual demonstrations into realistic-looking multi-view image datasets

---

#### 3.1 Generating Realistic Images from Virtual Demonstrations

- Based on LucidSim.

- Inputs:
  - diverse text prompts
  - semantic masks
  - normalized depth
  - robot overlay

- Text prompts generated at scale using ChatGPT.

- Semantic masks constrain:
  - object identity
  - object location

- Depth constrains:
  - scene geometry

- Main idea:

```text
Preserve Physics
+
Change Appearance
```

---

#### 3.2 Demonstration Augmentation

##### Procedural Scene Generation

- Generate MuJoCo XML scenes using Python.

- Allows control over initial scene distributions.

---

##### Repositioning Cameras Post-Demonstration

- Change camera pose after demonstration collection.

- Replay the same trajectory from different viewpoints.

- Uses:
  - camera intrinsics
  - camera extrinsics
  - depth
  - optical flow

- Goal:
  - reduce camera-pose sensitivity
  - improve sim-to-real robustness

---

##### Trajectory Warping

- Similar to MimicGen.

- Select trajectory keypoints.

- Transform keypoints based on new:
  - object locations
  - robot locations
  - initial states

- Generate new trajectory using:
  - linear position interpolation
  - spherical rotation interpolation

- Goal:
  - multiply demonstration data
  - improve robustness to object-position variation

---

### Section 4. Results

#### Manipulation Environments

- Block Stacking
- Pour Liquid
- Ball Sorting
- Knot Tying
- Kitchen-Sink
- Mug Tree

- Tasks are deliberately selected to evaluate different physical interactions.

---

#### 4.1 Data Collection and Learning Setup

- observations and actions:
  - SE(3) MoCap poses
  - 25 Hz

- rotation:
  - 6D representation

- observations:
  - proprioception
  - wrist RGB or three fixed RGB cameras

- action:
  - chunked absolute end-effector poses

- policies:
  - ACT
  - diffusion-based action denoiser

---

#### 4.2 Comparing Data Collection Speed

- 30 minutes of demonstrations collected for each setting.

- Real world:
  - manual reset
  - robot repositioning
  - safety checks

- Lucid-XR:
  - environment reset using a button

- Result:
  - roughly 2× more demonstrations with Lucid-XR
  - roughly 5× effective dataset size after augmentation

---

#### 4.3 Real-to-Sim Evaluation

- Real kitchens scanned using 3D Gaussian representations.

- Used as realistic evaluation environments.

- ACT:

```text
Base            100%
Low Clutter       0%
High Clutter      0%
```

- ACT + LucidSim:

```text
Base            100%
Low Clutter      90%
High Clutter
+ Noise          25%
```

- Visual augmentation greatly improves robustness to realistic clutter.

---

#### 4.4 Sim-to-Real Evaluation

- Compare:
  - Lucid-XR synthetic-data policies
  - real-teleoperation-data policies

- Data amounts:
  - 10 min
  - 20 min
  - 30 min

- In the original environment:
  - synthetic-data policies perform comparably to real-data policies.

- Under changed visual conditions:
  - real-data policy generalization drops
  - Lucid-XR policy remains robust

- Modified conditions include:
  - lighting
  - color
  - tabletop appearance
  - textured tablecloth
  - black tablecloth

---

### Section 5. Related Works

#### Extended Reality for Robot Teleoperation and Data Collection

Related systems include:

- Hitchhiking Hands
- ARCap
- ARMADA
- ARCADE
- AR2-D2
- EVE
- Open Teach
- IRIS
- DexHub / DART

Main distinction of Lucid-XR:

- physics simulation runs directly on the XR device
- reduces cloud / network latency
- targets scalable virtual demonstration collection

---

#### Generative AI for Synthetic Data Augmentation

Related works include:

- LucidSim
- Gen2Sim
- RoboGen
- DrEureka
- URDFormer
- CACTI
- DreamGen
- GenAug

Lucid-XR extends this direction toward manipulation by combining:

```text
Physics Simulation
+
Human Demonstrations
+
Generative Visual Augmentation
```

---

#### Large-Scale Imitation Learning and Data Aggregation

Examples:

- Open X-Embodiment
- RH20T
- DROID

These datasets provide large numbers of demonstrations, but diversity across:

- robots
- environments
- tasks

remains a major challenge.

Lucid-XR approaches this problem from a different direction:

```text
Physical Data Aggregation
vs.
Scalable Virtual Demonstration Generation
```

---

### Section 6. Conclusion

- Lucid-XR provides a generative-AI-powered data pipeline for robot manipulation.

- Virtual demonstrations can produce policies that generalize across:
  - object instances
  - appearance
  - lighting

- XR controllers and hand gestures provide scalable human interaction with simulated robots.

- The authors argue that virtual demonstration data could help close the robot-data gap required for general robot foundation models.

---

#### Deploying Across Embodiments

- Full-embodiment demonstrations can be used directly.

- In many cases, embodiment-free floating-gripper demonstrations can also transfer.

- Cross-embodiment transfer is mainly constrained by:
  - inverse kinematics
  - mobility

- This remains an important future research direction.

---

## Final Perspective

Lucid-XR can be summarized with one core principle:

```text
Do not spend all resources
making the simulator visually perfect.

Make the interaction physically meaningful,
collect behavior cheaply,
and create visual diversity afterward.
```

For robot learning, this suggests a scalable alternative to the traditional pipeline:

```text
More Real Robots
      ↓
More Human Teleoperation
      ↓
More Real Data
```

Lucid-XR instead proposes:

```text
Cheap XR Demonstrations
        ↓
Physics-Grounded Simulation
        ↓
Trajectory Augmentation
        ↓
Generative Visual Diversity
        ↓
Large Synthetic Dataset
        ↓
Real-World Robot Policy
```

The central research question is therefore no longer only:

> How can we train a better robot policy?

but also:

> How can we build a scalable data engine that continuously produces useful robot experience?