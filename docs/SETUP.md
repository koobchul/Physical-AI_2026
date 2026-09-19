# Setup Guide

Environment setup guide for the `Physical-AI_2026` project.

This document describes the hardware, software, and development environment used for VR teleoperation, robot simulation, and real-world robot control.

For detailed robot operation and safety notes, see [Robot Vendor Notes](ROBOT_VENDOR_NOTES.md).

---

## 1. System Information

### Robot Lab Workstation

| Component | Configuration |
|---|---|
| OS | Ubuntu 22.04 |
| CPU | Intel Xeon Gold (32 cores / 64 threads) |
| GPU | NVIDIA RTX PRO 5000 Blackwell (48 GB) |
| RAM | 256 GB |
| Python | To be confirmed |
| CUDA | To be confirmed |
| Conda Environment | To be confirmed |
| ROS2 | Humble (installed) |

### Other Development Machines

Development is also conducted on separate computers at Optim. Lab and MLAlab.

Record the Python environment, installed packages, and machine-specific configurations when necessary.

---

## 2. Hardware

### Robots

- UFACTORY xArm7 × 2
- UFACTORY Gripper
- INSPIRE RH56E2 robotic hand

### VR

- Meta Quest 2

### Current Hardware Status

| Component | Status |
|---|---|
| xArm7 (Left) | Connected; basic operation verified |
| xArm7 (Right) | Connected; basic operation verified |
| Robotic Hand | Connected; basic operation verified |
| Dual-Arm Coordination | Further validation required |
| VR-to-Real-Robot Control | Further validation required |

Basic operation verification does not imply that coordinated dual-arm motion or VR-based real-robot control has been validated.

---

## 3. Software Stack

### VR & Simulation

- Python
- MuJoCo
- robosuite
- SteamVR
- ALVR
- OpenVR
- PyOpenGL
- GLFW

### Robot Control & Learning

- ROS2 Humble
- UFACTORY Studio
- UFACTORY xArm Python SDK
- PyTorch

Installed package versions and working configurations should be recorded for each development machine.

---

## 4. Repository Setup

Clone the repository:

```bash
git clone https://github.com/koobchul/Physical-AI_2026.git
```

Move into the repository:

```bash
cd Physical-AI_2026
```

Before starting work:

```bash
git status
git pull
```

---

## 5. Python Environment

Check the Python version:

```bash
python --version
```

Check the available Conda environments:

```bash
conda env list
```

Activate the existing project environment before running the application.

Record the verified environment name and dependency versions after confirming the working configuration.

---

## 6. VR Environment

### Connection Pipeline

```text
Meta Quest 2
     ↓
ALVR
     ↓
SteamVR
     ↓
OpenVR
     ↓
Python Application
     ↓
MuJoCo / robosuite
```

### Connection Checklist

- [ ] Quest 2 connected through ALVR
- [ ] SteamVR running
- [ ] HMD tracking confirmed
- [ ] Left controller detected
- [ ] Right controller detected
- [ ] Stereo rendering confirmed

### OpenVR Check

```bash
python -c "import openvr; print('OpenVR OK')"
```

For detailed installation instructions and troubleshooting, refer to the verified configuration of the robot lab workstation.

---

## 7. VR Teleoperation

### Main Implementation

```text
code/vr_teleop/main_vr_scene.py
```

The current implementation integrates:

- HMD tracking
- Stereo rendering
- Camera coordinate transformation
- VR controller input
- Robot control in simulation
- Gripper control in simulation

### Execution

From the repository root:

```bash
cd code/vr_teleop
```

Check the available command-line arguments:

```bash
python main_vr_scene.py --help
```

The final experimental configuration was reported as:

```bash
python main_vr_scene.py --fov-scale-x 0.5
```

**Version verification required:** The previously shared script defines `--fov-scale` rather than `--fov-scale-x`.

Confirm the exact script version and execution arguments used in the successful experiment before treating this command as the verified configuration.

See [VR Teleoperation README](../code/vr_teleop/README.md).

---

## 8. Simulation

### Framework

- MuJoCo
- robosuite

### Current Environment

The current VR implementation uses:

- Environment: `Lift`
- Robot: `XArm7`
- Controller: `BASIC`

### Validation Checklist

- [ ] Simulation launches successfully
- [ ] Robot model loads correctly
- [ ] HMD tracking updates the virtual camera
- [ ] VR controller input controls the simulated robot
- [ ] Simulated gripper control verified
- [ ] Robot workspace and control limits validated

---

## 9. Real Robot Setup

### xArm7

The laboratory has two xArm7 robotic arms.

Both robots have been connected, and basic operation has been verified.

Before developing the real-robot control pipeline:

- Confirm the network connection of each robot.
- Identify the correct robot before issuing commands.
- Verify the initial robot poses.
- Confirm payload and TCP settings.
- Configure speed, workspace, and collision limits.
- Verify emergency stop and recovery procedures.

### Robotic Hand

The robotic hand has been connected, and basic operation has been confirmed.

Before integrating it with the VR teleoperation pipeline:

- Verify its communication interface.
- Confirm the power and initialization procedure.
- Confirm the available control commands.
- Validate position and force feedback.
- Establish safe operating limits.

### Dual-Arm Control

Coordinated dual-arm operation requires additional validation.

- Confirm independent communication with both arms.
- Verify the coordinate system of each robot.
- Define safe operating regions.
- Check potential arm-to-arm collisions.
- Validate coordinated motion in simulation before real execution.

For additional information, see [Robot Vendor Notes](ROBOT_VENDOR_NOTES.md).

---

## 10. Known Working Configuration

Record the verified configuration after testing.

| Item | Configuration |
|---|---|
| Workstation OS | Ubuntu 22.04 |
| ROS2 | Humble |
| VR Headset | Meta Quest 2 |
| Robot | UFACTORY xArm7 × 2 |
| Robotic Hand | INSPIRE RH56E2 |
| Python | To be confirmed |
| MuJoCo | To be confirmed |
| robosuite | To be confirmed |
| SteamVR | To be confirmed |
| ALVR | To be confirmed |
| Final VR Command | Version verification required |

---

## 11. Safety & Security

Before real-robot experiments:

- Verify the emergency stop and robot recovery procedures.
- Confirm that the workspace is clear.
- Use conservative speed and acceleration limits.
- Validate the intended motion in simulation.
- Confirm payload, TCP, and collision settings.
- Keep personnel outside the robot operating area during automated motion.

Do not commit:

- Passwords or access tokens
- Private credentials
- Sensitive network information
- Machine-specific secrets

---