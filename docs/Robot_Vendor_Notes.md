# Robot Vendor Notes

Technical notes from the robot vendor's installation and operation training for the `Physical-AI_2026` project.

This document summarizes robot operation, network configuration, safety settings, dual-arm control, and robotic hand integration.

The original training notes are retained separately for reference.

---

## 1. Hardware & Installation Status

### Robot System

- UFACTORY xArm7 × 2
- UFACTORY Gripper
- INSPIRE RH56E2 robotic hand

### Verified Status

- Both xArm7 robots are connected.
- Basic operation of both robots has been confirmed.
- The robotic hand is connected.
- Basic robotic hand operation has been confirmed.
- Ubuntu 22.04 and ROS2 Humble are installed.

Coordinated dual-arm control and VR-based real-robot teleoperation require further validation.

---

## 2. Robot Network

The vendor introduced network configuration using an ipTIME router and UFACTORY Studio.

### Network Configuration

- Confirm the IP address of each robot.
- Confirm that the workstation and robots are connected to the appropriate network.
- Verify communication before issuing robot commands.
- Record the network configuration for each robot separately.

The original vendor notes contain example IP addresses and communication ports.

These values must be confirmed against the current laboratory network before use.

### Robot Identification

| Device | IP Address | Connection Status |
|---|---|---|
| Left xArm7 | To be confirmed | Basic operation verified |
| Right xArm7 | To be confirmed | Basic operation verified |
| Robotic Hand | To be confirmed | Basic operation verified |

---

## 3. UFACTORY Studio

UFACTORY Studio is used for robot configuration and basic operation.

### Manual Mode

The vendor demonstrated manually changing the robot pose.

Before using manual operation:

- Confirm the robot's operating mode.
- Ensure that manual movement is permitted.
- Follow the vendor's instructions for manual guidance.
- Check the robot's surroundings before moving it.

Do not force the robot to move unless the appropriate manual guidance mode is enabled.

### Move J

Joint-space motion.

The robot moves toward the specified target joint configuration.

The end-effector does not necessarily follow a straight Cartesian path.

### Move L

Cartesian linear motion.

The robot attempts to move the end-effector along a straight-line path.

Joint motion and Cartesian motion may produce different trajectories.

Before execution:

- Confirm the target position.
- Check joint limits and workspace constraints.
- Check potential collisions.
- Test the intended motion in simulation.

### Recording

The vendor introduced robot motion recording functionality.

The recording procedure and exported data format require further confirmation.

---

## 4. Robot Initialization

Before starting an experiment:

1. Confirm the robot connection.
2. Check the current robot pose.
3. Verify the operating mode.
4. Check the configured TCP and payload.
5. Confirm speed and motion limits.
6. Ensure that the robot workspace is clear.
7. Verify emergency stop availability.

### Initial Position

Define and document a safe initial configuration for each robot.

Do not assume that the same initial position is safe for both arms.

---

## 5. TCP & Payload

### TCP

TCP (Tool Center Point) defines the reference point used for end-effector positioning and motion control.

When attaching a gripper, robotic hand, camera, or other equipment:

- Confirm the TCP position and orientation.
- Update the relevant tool configuration.
- Verify that the controller uses the intended reference frame.

### Payload

Additional equipment changes the mass and load distribution of the robot's end-effector.

The vendor emphasized configuring payload parameters to account for attached equipment.

Check:

- Tool mass
- Payload configuration
- Tool center of mass
- Robot load capacity

The xArm7 hardware specification lists a maximum payload of 3.5 kg.

The allowable operating load must account for the attached equipment and the applicable robot configuration.

Incorrect payload settings may affect motion behavior and collision detection.

---

## 6. Safety Configuration

### Collision Detection

Collision detection settings must be checked before real-robot experiments.

The vendor emphasized configuring the robot's safety parameters and considering the overlapping workspaces of the two arms.

### Motion Limits

Verify:

- Joint position limits
- Cartesian workspace limits
- Velocity limits
- Acceleration limits
- Payload limits
- Robot-to-robot collision risks

### Emergency Stop

Before implementing autonomous or VR-based robot control:

- Confirm the emergency stop procedure.
- Verify that the robot can be stopped safely.
- Establish a recovery procedure after a fault or emergency stop.

Safety functions must be validated on the actual hardware before real-robot teleoperation.

---

## 7. Dual-Arm Control

The laboratory has two xArm7 robotic arms.

Both arms have been connected, and basic operation has been verified.

### Communication

The vendor introduced controlling the two robots through their respective network connections.

Each robot must be identified independently.

### Development Checklist

- [ ] Confirm the network identity of each arm
- [ ] Verify independent robot communication
- [ ] Define each robot's base coordinate system
- [ ] Measure the relative position of the two robot bases
- [ ] Define safe operating regions
- [ ] Validate robot-to-robot collision avoidance
- [ ] Test coordinated motion in simulation
- [ ] Validate coordinated motion on real hardware

Basic operation of both robots does not imply that synchronized or coordinated dual-arm control has been completed.

---

## 8. Robotic Hand

The vendor introduced robotic hand communication and control.

### Current Status

- Hardware connected
- Basic operation verified

### Technical Topics

- Hand power and initialization
- Communication interface
- Position control
- Force feedback
- Register-based control
- Hand status monitoring

The original notes mention register operations and hand communication settings.

The exact register addresses, communication parameters, and control commands require confirmation from the corresponding hardware documentation.

### Integration Checklist

- [ ] Confirm the communication protocol
- [ ] Identify the verified control interface
- [ ] Confirm position feedback
- [ ] Confirm force feedback
- [ ] Define safe motion and force limits
- [ ] Test VR-to-Hand control mapping

---

## 9. ROS2 & Simulation

### ROS2

Installed environment:

- Ubuntu 22.04
- ROS2 Humble

The vendor discussed ROS2-based robot development and control.

Confirm the available ROS2 packages and robot interfaces before implementing ROS2-based control.

### Robot Models

The vendor also mentioned:

- URDF
- Isaac Sim

These tools may be considered for future simulation and robot model integration.

Their installation and integration status should be verified separately.

---

## 10. References

### UFACTORY

- [UFACTORY GitHub](https://github.com/xArm-Developer)
- [UFACTORY Documentation](https://docs.ufactory.cc/)

### Project Documentation

- [Setup Guide](SETUP.md)
- [Research Worklog](WORKLOG.md)
- [Project README](../README.md)

---

## 11. Items Requiring Confirmation

The following details were not fully established from the vendor training notes:

- Exact IP addresses and communication ports
- Verified UFACTORY Studio version
- Robot initialization and shutdown procedure
- Validated TCP and payload values
- Dual-arm synchronization method
- Robotic hand communication protocol
- Robotic hand register addresses
- ROS2 package versions and available robot interfaces

Update this document after confirming these details on the laboratory hardware.

---