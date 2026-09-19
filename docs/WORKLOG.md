# Research Worklog

Development and experiment log for the `Physical-AI_2026` project.

This document tracks overall research progress, technical issues, milestones, and daily experiment records.

Detailed experiment plans, checklists, observations, and results are maintained in date-specific worklogs.

For meeting notes and general discussions, use the shared Daily Sheet.

---

## 1. Current Research Status

### Current Focus

VR teleoperation and robot manipulation system development.

The September 17–18 diagnostic experiments investigated HMD tracking, stereo rendering, camera transformation, VR distortion, and projection geometry.

The current main implementation is:

`code/vr_teleop/main_vr_scene.py`

The current system integrates:

- Meta Quest 2, ALVR, SteamVR, and OpenVR
- HMD and VR controller tracking
- Stereo rendering and camera transformation
- MuJoCo / robosuite simulation
- VR-based robot and gripper control in simulation

The final experimental VR configuration has been selected.

The previous diagnostic baseline, `main_vr_scene_7.py`, is preserved for comparison.

### Open Issues

- Validate the stability and accuracy of the final VR configuration.
- Confirm VR-to-Robot coordinate transformation and control accuracy.
- Verify robot workspace and safety limits.
- Establish and validate the real-robot teleoperation pipeline.
- Prepare demonstration data collection.

### Next Priorities

1. Verify the final VR configuration.
2. Validate controller tracking and robot control in simulation.
3. Measure robot dimensions and workspace.
4. Configure real-robot communication and safety limits.
5. Prepare VR teleoperation experiments with xArm7.

For implementation details, see [VR Teleoperation](../code/vr_teleop/README.md).

---

## 2. Worklog Index

Detailed experiment records are organized by date.

| Date | Main Topic | Worklog |
|---|---|---|
| 2026-09-16 | Initial project setup and documentation | [2026-09-16](worklog/2026-09/2026-09-16.md) |
| 2026-09-17 | VR teleoperation diagnostics (Cases 01–16) | [2026-09-17](worklog/2026-09/2026-09-17.md) |
| 2026-09-18 | VR distortion experiments and final configuration investigation | [2026-09-18](worklog/2026-09/2026-09-18.md) |

Add new daily worklogs to this index as research progresses.

---

## 3. Important Milestones

Mark an item as completed only after the corresponding functionality has been implemented and validated.

### VR Tracking & Rendering

- [ ] Stable HMD position and rotation tracking
- [ ] Stable VR controller tracking
- [ ] Stereo rendering and projection validated
- [ ] Final VR configuration validated

### VR Teleoperation & Simulation

- [ ] VR-to-Robot coordinate transformation validated
- [ ] End-effector position and orientation control validated
- [ ] Gripper control validated
- [ ] Robot manipulation task tested
- [ ] Demonstration recording enabled

### Real Robot

- [ ] xArm7 communication verified
- [ ] Robot workspace and safety limits configured
- [ ] Basic Cartesian control tested
- [ ] VR teleoperation tested
- [ ] Demonstration data collection tested

### Robot Learning

- [ ] Demonstration format and dataset pipeline defined
- [ ] Imitation Learning baseline implemented
- [ ] Robot policy evaluated
- [ ] Sim-to-Real evaluation performed
- [ ] VLA integration tested

---

## 4. Documentation Guidelines

### Daily Worklog

Create a new Markdown file for each research day.

```text
docs/worklog/YYYY-MM/YYYY-MM-DD.md
```

Each daily worklog should contain:

- Goal
- Done
- Experiment (Purpose, Setup, Test, Result)
- Issues
- Next
- Notes

Record detailed Case checklists, observations, and results in the corresponding daily worklog.

### Experiment Code

Store diagnostic scripts in:

```text
code/vr_teleop/cases/YYYY-MM-DD/
```

Use the naming convention:

`case_XX_short_description.py`

Each experiment should identify its reference implementation and document the modified variables.

### Documentation Rules

| Document | Purpose |
|---|---|
| [README.md](../README.md) | Project overview and research direction |
| [VR Teleoperation README](../code/vr_teleop/README.md) | Code structure, execution, and experiment rules |
| [SETUP.md](SETUP.md) | Hardware and software environment setup |
| `docs/WORKLOG.md` | Overall research progress and milestones |
| `docs/worklog/YYYY-MM/YYYY-MM-DD.md` | Detailed daily experiment records |
| Shared Daily Sheet | Meeting notes, ideas, and general discussions |

---