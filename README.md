# Physical-AI_2026

Physical AI / Robot Learning research project.

This repository contains implementations, experiments, and documentation for VR teleoperation, robotic manipulation, simulation, and robot learning.

---

## 1. Research Goal

The goal of this project is to develop robot learning systems that connect human demonstrations, robot simulation, and real-world robotic manipulation.

Our research focuses on:

- VR Teleoperation
- Robot Manipulation
- Demonstration Data Collection
- Imitation Learning
- Robot Policy Learning
- Vision-Language-Action (VLA)
- Sim-to-Real

The current objective is to develop a VR-based robot teleoperation system and extend it toward real-world demonstration collection and robot learning.

---

## 2. Current Research Progress

### VR Teleoperation

A VR teleoperation system has been implemented using Meta Quest 2, SteamVR, OpenVR, MuJoCo, and robosuite.

The current implementation supports:

- HMD position and rotation tracking
- VR controller tracking
- Stereo rendering and camera transformation
- VR-based robot control in simulation
- Simulated gripper control

The VR distortion experiments conducted on September 17–18 led to an updated rendering configuration.

The team has reported improvements in visual distortion and rendering performance.

**Current main implementation:**

`code/vr_teleop/main_vr_scene.py`

### Robot Hardware

Both xArm7 robotic arms and the robotic hand have been connected, and their basic operation has been verified.

**Current development priorities:**

1. Validate the final VR configuration.
2. Verify robot workspace and safety settings.
3. Establish VR-to-Real-Robot control.
4. Develop demonstration data collection.
5. Extend the system toward imitation learning and robot policy learning.

---

## 3. Research Pipeline

```text
Human / VR Input
        ↓
VR Tracking & Controller Input
        ↓
Coordinate Transformation
        ↓
Robot Control in Simulation
        ↓
Real Robot Teleoperation
        ↓
Demonstration Data Collection
        ↓
Imitation Learning / Robot Policy
        ↓
VLA & Sim-to-Real
```

The pipeline represents the overall research direction. Real-robot teleoperation and robot learning remain subsequent development stages.

---

## 4. Hardware & Software

### Hardware

| Category | Equipment |
|---|---|
| Robot Arms | UFACTORY xArm7 × 2 |
| Gripper | UFACTORY Gripper |
| Robotic Hand | INSPIRE RH56E2 |
| VR Headset | Meta Quest 2 |
| GPU | NVIDIA RTX PRO 5000 Blackwell 48 GB |

### Software

- Python / PyTorch
- MuJoCo / robosuite
- SteamVR / ALVR / OpenVR
- ROS2
- UFACTORY Studio

Detailed environment information is available in [SETUP.md](docs/SETUP.md).

---

## 5. Repository Structure

```text
Physical-AI_2026/
│
├── code/
│   └── vr_teleop/
│       ├── archive/
│       ├── cases/
│       ├── diagnostics/
│       ├── main_vr_scene.py
│       └── README.md
│
├── docs/
│   ├── worklog/
│   │   └── 2026-09/
│   ├── SETUP.md
│   ├── WORKLOG.md
│   └── ROBOT_VENDOR_NOTES.md
│
├── README_DH.md
├── README_HW.md
└── README.md
```

---

## 6. Documentation

| Document | Description |
|---|---|
| [VR Teleoperation](code/vr_teleop/README.md) | Implementation, execution, and diagnostic experiments |
| [Setup Guide](docs/SETUP.md) | Hardware and software environment setup |
| [Research Worklog](docs/WORKLOG.md) | Research progress, milestones, and daily records |
| [Robot Vendor Notes](docs/Robot_Vendor_Notes.md) | Robot operation, configuration, and safety notes |

Detailed experiment records are maintained in `docs/worklog/`.

Meeting notes and general research discussions are managed through the shared Daily Sheet.

---

## 7. Collaborators

| Name | Affiliation |
|---|---|
| 구병철 (Byoungchul Koo) | Optim. Lab |
| 정동현 (Donghyun Jeong) | MLAlab |
| 정현우 (Hyunwoo Jeong) | MLAlab |

Department of Statistical Data Science, University of Seoul

---

## 8. Collaboration Workflow

Before starting work:

```bash
git status
git pull
```

After completing work:

```bash
git status
git add <file-path>
git commit -m "Describe the update"
git push
```

Use separate branches and Pull Requests when multiple researchers modify the same component.

Do not commit sensitive configuration files or large experimental videos.

---

## 9. Status

**Work in Progress**

Current stage: VR Teleoperation → Real Robot Integration.

Future stages: Demonstration Collection → Robot Learning → VLA.

---