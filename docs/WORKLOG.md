# Research Worklog

Development and experiment log for the Physical-AI_2026 project.

This document records technical progress, experiments, failures, debugging results, and next steps.

For meeting notes, ideas, and general discussion, use the shared Daily Sheet.

---

# Worklog Template

Use the following structure for new entries.

## 2026-09-17



### Goal

-

### Done

-

### Experiment

#### Experiment Name

**Purpose**

-

**Setup**

-

**Test**

-

**Result**

-

### Issues

-

### Next

-

### Notes

-

---

# 2026-09-17

## Goal

- Organize GitHub collaboration environment
- Organize VR teleoperation code and documentation
- Prepare shared development workflow

## Done

- Added VR teleoperation diagnostic scripts
- Organized repository structure
- Removed unnecessary macOS `.DS_Store`
- Added shared documentation structure
- Prepared GitHub repository for collaboration

## Experiment

### VR Teleoperation Diagnostics

**Purpose**

Validate HMD tracking, stereo rendering, camera transformation, and VR coordinate behavior.

**Tested Components**

- HMD rotation
- HMD translation
- 6DoF pose
- Predicted HMD pose
- Stereo eye transformation
- Projection frustum
- Camera coordinate transformation
- Left / right eye behavior

**Diagnostic Scripts**

- `case_01_headpose_relative_rotation.py`
- `case_02_projection_frustum_aspect.py`
- `case_03_symmetric_frustum_center.py`
- `case_04_same_image_both_eyes.py`
- `case_05_fresh_hmd_pose.py`
- `case_06_frustum_width_from_render_aspect.py`
- `case_07_full_6dof_head_translation.py`
- `case_08_predicted_hmd_pose_30ms.py`
- `case_09_static_camera_no_vr_override.py`
- `case_10_eye_transform_translation_only.py`
- `case_11_swap_left_right_submit.py`
- `case_12_zero_ipd_eye_translation.py`
- `case_13_world_up_lock_no_roll.py`
- `case_14_flip_frustum_center_sign.py`
- `case_15_flip_vertical_frustum_sign.py`

## Result

- TODO

## Issues

- VR camera / HMD transformation requires further validation.
- Stereo rendering behavior requires further testing.
- VR coordinate system must be aligned with the robot coordinate system.

## Next

- Stabilize VR rendering
- Confirm HMD coordinate transformation
- Confirm VR controller tracking
- Validate VR-to-Robot coordinate mapping
- Connect VR control to simulation
- Prepare xArm7 teleoperation pipeline

## Notes

-

---

# 2026-09-18

## Goal

-

## Done

-

## Experiment

### Experiment Name

**Purpose**

-

**Setup**

-

**Test**

-

**Result**

-

## Issues

-

## Next

-

## Notes

-

---

# Important Milestones

## VR Tracking

- [ ] Stable HMD position tracking
- [ ] Stable HMD rotation tracking
- [ ] Stable controller tracking
- [ ] Correct stereo rendering
- [ ] Correct projection / frustum

## VR Teleoperation

- [ ] VR coordinate system validated
- [ ] Robot coordinate system validated
- [ ] VR → Robot transformation validated
- [ ] End-effector position control
- [ ] End-effector orientation control
- [ ] Gripper control

## Simulation

- [ ] Robot model loaded
- [ ] VR input connected to simulation
- [ ] Manipulation task tested
- [ ] Demonstration recording enabled

## Real Robot

- [ ] xArm7 communication verified
- [ ] Safety limits configured
- [ ] Basic Cartesian control tested
- [ ] VR teleoperation tested
- [ ] Demonstration data collection tested

## Robot Learning

- [ ] Demonstration format defined
- [ ] Dataset pipeline defined
- [ ] Imitation Learning baseline
- [ ] Policy evaluation
- [ ] Sim-to-Real evaluation
- [ ] VLA integration


- python case_32_both_eyes.py --fov-scale-x 0.5
- final case 
