# robopi — learning journal

This repo documents Rebecca's hands-on journey learning embedded Linux,
GPIO programming, and robotics on a Raspberry Pi 4 Model B running
Raspberry Pi OS Lite 64-bit (Debian Bookworm).

## project arc

The learning path moves through these stages in order:

1. GPIO basics — controlling hardware with Python and lgpio
2. Sensors and input — reading data from the physical world
3. ROS 2 (Jazzy) — installing and learning the Robot Operating System
4. ROS 2 nodes and topics — writing publishers and subscribers
5. Hardware integration — connecting sensors and actuators to ROS

## current focus

Stage 3: ROS 2 integration. The PiDog v2 build is complete and all hardware
is verified (servos calibrated, touch/ultrasonic/IMU sensors working, LEDs
and camera functional). The goal is to wrap the PiDog in ROS 2 nodes as a
foundation for ML experimentation.

## hardware

- Raspberry Pi 4 Model B
- Hostname: robopi (`ssh rebecca@robopi.local`)
- OS: Raspberry Pi OS Lite 64-bit (Debian Bookworm) — Bookworm is required for
  PiDog v2 compatibility; Trixie (Python 3.13) breaks mediapipe and tflite-runtime
  which have a hard ceiling of Python 3.12
- Hardware: SunFounder PiDog v2 with Robot HAT+ 5 (I2C address 0x15)
- GPIO library: lgpio (not RPi.GPIO — that is deprecated on Bookworm)

## conventions

- Python for all GPIO and ROS node code
- Each stage lives in its own directory: `01-gpio/`, `02-sensors/`, `03-ros2/` etc.
- Each stage has its own `README.md` documenting what was learned and how to run it
- Code should be written to run on the Pi itself, not a dev machine
- Keep things simple — this is a learning journal, not a production codebase

## Pi directory layout

```text
~/miniforge3/        Miniforge conda installation
~/miniforge3/envs/ros_env/   conda env — all Python packages including ROS 2, pidog, robot_hat
~/pidog_ros2/        ROS 2 package source (synced from pidog_ros2/ in this repo)
~/ros2_ws/           colcon workspace (built on Pi, not in repo)
~/pidog/             SunFounder pidog library source
~/robot-hat/         SunFounder robot-hat library source (branch 2.5.x)
~/vilib/             SunFounder vilib library source
```

Ad-hoc scripts (led_test.py, sensors_test.py etc.) deploy to `~/` via `deploy-run.sh`.

## notes for Claude Code

- The target platform is ARM64 Linux, not macOS or x86
- Use lgpio for all GPIO access, never RPi.GPIO
- ROS 2 Jazzy is being installed as part of Stage 3 — do not assume it is available until confirmed
- ROS 2 nodes live in `pidog_ros2/` (this repo) and are synced to `~/pidog_ros2/` on the Pi
- The colcon workspace is at `~/ros2_ws/` on the Pi — built there, not checked in
- pidog, robot_hat, vilib and all Python dependencies run in `~/miniforge3/envs/ros_env`
- Prefer clear, well-commented code over clever code — this is for learning
