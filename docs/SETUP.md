# Setup Guide

Environment setup guide for the Physical-AI_2026 project.

This document records the configuration required to reproduce the VR teleoperation, simulation, and robot control environment.

---

## 1. System Information

Fill this section for each machine when necessary.

### Robot Lab Workstation

- OS:
- CPU:
- GPU:
- RAM:
- Python:
- CUDA:
- Conda Environment:

### Other Development Machines

- OS:
- Python:
- Conda Environment:

---

## 2. Hardware

### Robot

- UFACTORY xArm7
- UFACTORY Gripper
- INSPIRE RH56E2

### VR

- Meta Quest 2

---

## 3. Software Stack

Main software:

- Python
- PyTorch
- MuJoCo
- robosuite
- SteamVR
- ALVR
- OpenVR

---

## 4. Python Environment

Check Python:

~~~bash
python --version
~~~

Example Conda environment:

~~~bash
conda create -n physical_ai python=3.10
conda activate physical_ai
~~~

Check active environment:

~~~bash
conda env list
~~~

---

## 5. Repository Setup

Clone the repository:

~~~bash
git clone https://github.com/koobchul/Physical-AI_2026.git
~~~

Move into the repository:

~~~bash
cd Physical-AI_2026
~~~

Before starting work:

~~~bash
git pull
~~~

---

## 6. VR Environment

### Quest 2

Target connection flow:

~~~text
Meta Quest 2
     ↓
ALVR
     ↓
SteamVR
     ↓
OpenVR
     ↓
Python Application
~~~

---

## 7. SteamVR

### Installation

TODO

### Execution

TODO

### Important Notes

- Confirm that the headset is detected.
- Confirm that HMD pose updates correctly.
- Confirm that left and right controllers are detected.
- Confirm that SteamVR tracking is active.

---

## 8. ALVR

### Installation

TODO

### Connection

TODO

### Important Configuration

TODO

---

## 9. OpenVR

Check whether the Python OpenVR package is available:

~~~bash
python -c "import openvr; print('OpenVR OK')"
~~~

If necessary:

~~~bash
pip install openvr
~~~

---

## 10. Simulation

### MuJoCo

Installation:

~~~text
TODO
~~~

Test:

~~~text
TODO
~~~

### robosuite

Installation:

~~~text
TODO
~~~

Test:

~~~text
TODO
~~~

---

## 11. Robot Setup

### xArm7

Connection procedure:

~~~text
TODO
~~~

### Gripper

~~~text
TODO
~~~

### INSPIRE RH56E2

~~~text
TODO
~~~

Do not commit sensitive or machine-specific configuration such as:

- Passwords
- Tokens
- Private credentials
- Private network information

---

## 12. VR Teleoperation

Move to the implementation directory:

~~~bash
cd code/vr_teleop
~~~

Example execution:

~~~bash
python main_vr.py
~~~

Current pipeline:

~~~text
HMD / Controller
       ↓
OpenVR
       ↓
Pose Extraction
       ↓
Coordinate Transformation
       ↓
Robot / Simulation Command
~~~

---

## 13. Coordinate Systems

When debugging VR-to-Robot control, verify:

- VR world coordinate
- HMD coordinate
- Left-eye coordinate
- Right-eye coordinate
- Camera coordinate
- Robot base coordinate
- End-effector coordinate

Record any conversion matrices or axis conventions here.

### VR Coordinate Convention

~~~text
TODO
~~~

### Robot Coordinate Convention

~~~text
TODO
~~~

### VR → Robot Transformation

~~~text
TODO
~~~

---

## 14. Troubleshooting

### SteamVR does not detect the headset

#### Symptoms

-

#### Cause

-

#### Solution

-

---

### ALVR connection failure

#### Symptoms

-

#### Cause

-

#### Solution

-

---

### Controller not detected

#### Symptoms

-

#### Cause

-

#### Solution

-

---

### Incorrect stereo image

Check:

- Left / right eye order
- Projection matrix
- Eye transform
- IPD translation
- Frustum center
- Vertical / horizontal sign convention

---

### Incorrect HMD motion

Check:

- Position axis convention
- Rotation matrix convention
- Matrix multiplication order
- World-to-camera vs camera-to-world
- Relative vs absolute pose
- Prediction timing

---

### Incorrect robot motion

Check:

- VR-to-Robot axis mapping
- Position scaling
- Rotation scaling
- Reference pose
- Position deadzone
- Rotation deadzone
- Robot base coordinate

---

## 15. Machine-Specific Notes

### Robot Lab Workstation

~~~text
TODO
~~~

### Personal / Lab Mac

~~~text
TODO
~~~

### Donghyun Environment

~~~text
TODO
~~~

---

## 16. Known Working Configuration

Once the pipeline becomes stable, record the verified configuration here.

- OS:
- Python:
- SteamVR:
- ALVR:
- OpenVR:
- MuJoCo:
- robosuite:
- Robot:
- VR Headset:
- Verified Date:

---

## 17. Setup Checklist

- [ ] Repository cloned
- [ ] Python environment created
- [ ] Required packages installed
- [ ] Quest 2 connected
- [ ] ALVR connected
- [ ] SteamVR running
- [ ] HMD tracking confirmed
- [ ] Controller tracking confirmed
- [ ] Simulation running
- [ ] Robot connection confirmed
- [ ] VR-to-Robot transformation validated