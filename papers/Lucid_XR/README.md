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

> Lucid-XR is an XR-based robotic data engine that enables scalable collection of virtual human demonstrations through on-device physics simulation and converts them into diverse and realistic synthetic training data for robot manipulation.

---

## 2. Why this Paper?

### Problem

- Digitally creating millions of realistic-looking virtual worlds at the scale required for robots to generalize to the real world is infeasibly expensive.

- Virtual demonstrations collected in simple and sparsely populated 3D environments alone are insufficient for training real-world computer vision systems.

- Existing XR / teleoperation systems often rely on an external computer or server for physics simulation and kinematics computation.
  - Network communication introduces latency.
  - This becomes particularly problematic for dynamic, deformable, or contact-rich interactions.

- Retargeting human poses to robot form factors with different kinematic structures often requires:
  - robot-specific custom code
  - a separate kinematics server
  - additional system configuration

- These requirements make large-scale crowdsourcing of robot demonstrations difficult.

### Motivation

- Instead of collecting every demonstration using a physical robot, human demonstrations can be collected cheaply and safely inside an XR simulation.

- If physics simulation can run directly on an XR device:
  - network latency can be removed
  - a dedicated simulation server is no longer required
  - demonstration collection can potentially scale through the internet

- However, low-fidelity virtual demonstrations alone lack sufficient visual diversity for training real-world robot policies.

- Generative models can transform simple simulated observations into visually diverse and realistic data while preserving the underlying physical interaction.

- Combining:
  - scalable XR demonstration collection
  - on-device physics simulation
  - human-to-robot pose retargeting
  - generative visual augmentation

  could provide a scalable data engine for training real-world robot policies.

### Main Contribution

1. **On-device physics simulation**
   - Move physics simulation directly onto XR devices.
   - Enables latency-free, untethered multi-physics simulation through a web browser.

2. **Human-to-robot pose retargeting**
   - Retarget human motion to virtual robot embodiments without requiring custom robot-specific programs or an external kinematics server.

3. **Synthetic data generation for robot learning**
   - Convert simple virtual demonstrations into diverse and realistic visual training data using a generative pipeline.
   - Demonstrate deployment of policies trained using Lucid-XR synthetic data in realistic evaluation environments.

---

## 3. Key Concepts

### Lucid-XR

- An extended-reality data engine for robotic manipulation.

- Main goal:
  - collect scalable human demonstrations in XR
  - augment them into diverse and realistic robot training data
  - use the resulting data to train robot manipulation policies

### Vuer

- Core XR framework used by Lucid-XR.

- A simulator-agnostic XR framework that runs directly inside a web browser.

- Handles:
  - XR interaction
  - rendering
  - physics simulation
  - robot control / retargeting

### On-Device Physics Simulation

- Physics simulation is executed directly on the XR device instead of on an external simulation server.

- Advantages:
  - removes network latency
  - enables untethered XR interaction
  - reduces bandwidth requirements
  - enables more responsive interaction with deformable and dynamic objects

### Multi-Physics Simulation

Lucid-XR supports multiple types of physical interaction, including:

- rigid-body contact
- deformable / flexible materials
- particle-rich environments
- fluid / wind forces
- non-convex collision using SDF-based collision

### WebAssembly

- MuJoCo is compiled into WebAssembly.

- Purpose:
  - bypass the single-threaded V8 JavaScript engine
  - achieve near-native physics simulation speed directly on XR hardware

### WebXR

- Browser standard for XR device interaction.

- Enables interaction through:
  - hands
  - motion controllers
  - different XR devices

### WebGL

- Used for real-time 3D rendering directly inside the browser.

- Lucid-XR uses a react-three/fiber based front-end for rendering and interaction.

### Pose Retargeting

- Converts human hand / body motion into robot-compatible motion.

- Lucid-XR binds motion capture sites to robot landmarks and uses robot kinematics to track them.

### SE(3)

- Represents a rigid-body pose consisting of:
  - 3D translation
  - 3D rotation

- Lucid-XR uses SE(3) poses for controlling robot grippers and representing motion.

### Hitchhiking Controller

- Interaction method inspired by *Hitchhiking Hands*.

- Allows users to remotely select and manipulate distant robot grippers inside XR.

- Helps avoid large tracking errors that occur when directly mapping human hand motion to a distant virtual robot.

### Generative Visual Augmentation

- Converts low-fidelity simulation observations into diverse and realistic-looking images.

- Uses:
  - text prompts
  - semantic masks
  - depth information
  - robot overlays

### Demonstration Augmentation

- Existing demonstrations can be modified after collection.

- Includes:
  - camera repositioning
  - object repositioning
  - robot repositioning
  - trajectory warping

---

## 4. Method / Overview

Lucid-XR can be understood as the following data pipeline:

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
Virtual Demonstration Data
      ↓
Demonstration Augmentation
      ↓
Generative Image Pipeline
      ↓
Diverse + Realistic Multi-view Data
      ↓
Robot Policy Training
      ↓
Evaluation / Sim-to-Real