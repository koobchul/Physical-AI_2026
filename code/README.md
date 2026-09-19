# VR Teleoperation

VR teleoperation implementation and diagnostic experiments for the `Physical-AI_2026` project.

## 1. Current Implementation

The current main implementation is `main_vr_scene.py`.

The system integrates:
- Meta Quest 2, ALVR, SteamVR, and OpenVR
- HMD and controller tracking
- Stereo rendering and camera transformation
- MuJoCo / robosuite simulation
- VR-based robot and gripper control

The current implementation uses the robosuite `Lift` environment with the `XArm7` robot configuration.

### Execution

```bash
cd code/vr_teleop
python main_vr_scene.py --fov-scale-x 0.5
```

**Note:** The previously shared version of `main_vr_scene.py` defines `--fov-scale` instead of `--fov-scale-x`. Confirm the supported argument with `python main_vr_scene.py --help` before running.

## 2. Directory Structure

```text
vr_teleop/
├── archive/             # Previous implementations
├── cases/               # Date-specific experiments
│   ├── 2026-09-17/
│   └── 2026-09-18/
├── diagnostics/         # Diagnostic scripts
├── main_vr_scene_7.py   # Previous diagnostic baseline
├── main_vr_scene.py     # Current main implementation
└── README.md
```

## 3. Experiment Rules

The previous diagnostic baseline was `main_vr_scene_7.py`.

For new experiments:
1. Identify the reference implementation.
2. Change one variable whenever possible.
3. Compare the result with the reference implementation.
4. Record observations and conclusions in the daily worklog.

## 4. Experiment Records

| Date | Topic | Worklog |
|---|---|---|
| 2026-09-17 | HMD tracking, stereo rendering, camera transformation | [09-17](../../docs/worklog/2026-09/2026-09-17.md) |
| 2026-09-18 | VR distortion, coordinate transformation, FOV | [09-18](../../docs/worklog/2026-09/2026-09-18.md) |

Detailed experiment checklists and results are maintained in `docs/worklog/`.

## 5. Related Documentation

- [Project Overview](../../README.md)
- [Research Worklog](../../docs/WORKLOG.md)
- [Setup Guide](../../docs/SETUP.md)