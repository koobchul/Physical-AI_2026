# Code

Implementation and experimental code for the Physical-AI_2026 project.

The current codebase primarily focuses on VR teleoperation, HMD tracking, stereo rendering, coordinate transformation, and robot control experiments.

---

## Directory Structure

~~~text
code/
│
├── vr_teleop/
│   ├── diagnostics/
│   ├── main_vr.py
│   ├── main_wlx.py
│   └── ...
│
├── case_01_headpose_relative_rotation.py
├── case_02_projection_frustum_aspect.py
├── case_03_symmetric_frustum_center.py
├── case_04_same_image_both_eyes.py
├── case_05_fresh_hmd_pose.py
├── case_06_frustum_width_from_render_aspect.py
├── case_07_full_6dof_head_translation.py
├── case_08_predicted_hmd_pose_30ms.py
├── case_09_static_camera_no_vr_override.py
├── case_10_eye_transform_translation_only.py
├── case_11_swap_left_right_submit.py
├── case_12_zero_ipd_eye_translation.py
├── case_13_world_up_lock_no_roll.py
├── case_14_flip_frustum_center_sign.py
├── case_15_flip_vertical_frustum_sign.py
└── README.md
~~~

---

## Main Components

### VR Tracking

Current tracking components include:

- HMD position
- HMD rotation
- VR controller position
- VR controller rotation
- 6DoF motion
- Predicted HMD pose

---

## Camera / Projection

Current experiments include:

- View matrix
- Projection matrix
- Stereo rendering
- Frustum configuration
- Aspect ratio
- Eye transformation
- Interpupillary distance
- Camera coordinate transformation

---

## Robot Control

The target control pipeline is:

~~~text
VR Controller Pose
        ↓
Coordinate Conversion
        ↓
Reference Pose
        ↓
Robot End-Effector Command
        ↓
Gripper Command
~~~

Current control components include:

- Position control
- Orientation control
- Relative motion
- Deadzone handling
- Gripper input
- VR-to-Robot coordinate transformation

---

## Diagnostic Cases

### Case 01 — Head Pose Relative Rotation

Tests relative HMD rotation behavior.

### Case 02 — Projection Frustum Aspect

Validates projection matrix and frustum aspect ratio.

### Case 03 — Symmetric Frustum Center

Tests symmetric stereo frustum configuration.

### Case 04 — Same Image Both Eyes

Renders identical images to both eyes for stereo debugging.

### Case 05 — Fresh HMD Pose

Tests real-time HMD pose updates.

### Case 06 — Frustum Width from Render Aspect

Validates frustum width using the render aspect ratio.

### Case 07 — Full 6DoF Head Translation

Tests full HMD translation and rotation.

### Case 08 — Predicted HMD Pose

Tests predicted HMD pose for rendering latency compensation.

### Case 09 — Static Camera / No VR Override

Uses a fixed virtual camera to isolate VR camera transformation issues.

### Case 10 — Eye Transform Translation Only

Applies only translation from the VR eye transform.

### Case 11 — Swap Left / Right Eye

Tests stereo rendering by swapping the submitted eye images.

### Case 12 — Zero IPD Eye Translation

Removes IPD-based eye translation for debugging.

### Case 13 — World Up Lock / No Roll

Suppresses HMD roll and locks the camera to the world-up direction.

### Case 14 — Flip Frustum Center Sign

Tests the horizontal frustum sign convention.

### Case 15 — Flip Vertical Frustum Sign

Tests the vertical frustum sign convention.

---

## Development Flow

~~~text
VR Tracking
    ↓
Stereo / Camera Validation
    ↓
Coordinate Transformation
    ↓
Robot Command Generation
    ↓
Simulation Validation
    ↓
Real Robot Integration
~~~

---

## Running the Code

Example:

~~~bash
cd code/vr_teleop
python main_vr.py
~~~

Actual commands may differ depending on the current experimental configuration.

---

## Development Guidelines

Before modifying code:

~~~bash
git pull
~~~

After modifications:

~~~bash
git status
git add .
git commit -m "Describe the code update"
git push
~~~

Avoid committing:

- Temporary files
- Large videos
- `.DS_Store`
- Credentials
- Passwords
- Private IP configuration
- Machine-specific secrets

---

## Notes

The `case_XX` scripts are diagnostic experiments.

They may be removed, reorganized, or merged after the VR rendering and teleoperation pipeline becomes stable.