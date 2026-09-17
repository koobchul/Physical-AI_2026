# Physical-AI_2026

Physical AI / Robot Learning research repository.

This repository contains research, experiments, implementations, and documentation for robotic manipulation, VR teleoperation, simulation, and Vision-Language-Action (VLA).

---

## Research Goal

The goal of this project is to study and develop robotic manipulation systems that connect:

- Human Interaction
- VR Teleoperation
- Robot Simulation
- Robot Learning
- Imitation Learning
- Vision-Language-Action (VLA)
- Sim-to-Real
- Real-World Robot Manipulation

The project currently focuses on building a stable VR-based robot control pipeline and gradually extending it toward data collection and robot learning.

---

## Current Research Flow

~~~text
Human / VR Input
        ↓
VR Tracking
        ↓
Coordinate Transformation
        ↓
Robot Control
        ↓
Simulation
        ↓
Data Collection
        ↓
Robot Learning / VLA
        ↓
Real Robot
~~~

---

## Hardware

### Robots

- UFACTORY xArm7
- UFACTORY Gripper
- INSPIRE RH56E2

### VR

- Meta Quest 2

### Computing

- GPU Workstation

---

## Software Stack

- Python
- PyTorch
- MuJoCo
- robosuite
- SteamVR
- ALVR
- OpenVR

---

## Repository Structure

~~~text
Physical-AI_2026/
│
├── code/
│   ├── vr_teleop/
│   └── README.md
│
├── docs/
│   ├── SETUP.md
│   └── WORKLOG.md
│
├── papers/
│   └── Paper Reviews
│
└── README.md
~~~

---

## Current Work

### VR Teleoperation

Current experiments focus on:

- HMD pose tracking
- VR controller tracking
- Stereo rendering
- Projection / Frustum
- Camera pose transformation
- 6DoF head motion
- VR-to-Robot coordinate transformation
- End-effector control
- Gripper control

### Robot Manipulation

Planned development:

~~~text
VR Controller
      ↓
Robot End-Effector Command
      ↓
Simulation Validation
      ↓
Demonstration Collection
      ↓
Imitation Learning / Robot Policy
      ↓
Real Robot Deployment
~~~

---

## Documentation

### `code/README.md`

Code structure, diagnostic scripts, and implementation notes.

### `docs/SETUP.md`

Hardware and software environment setup instructions.

### `docs/WORKLOG.md`

Development, experiment, issue, and result logs.

### `papers/`

Paper reviews and research notes.

---

## Collaboration Workflow

Before starting work:

~~~bash
git pull
~~~

After completing work:

~~~bash
git add .
git commit -m "Describe the update"
git push
~~~

When multiple people are working on the same component, use separate branches and Pull Requests when necessary.

---

## Collaborators

- Byoungchul Koo
- Donghyun

---

## Status

Work in Progress.