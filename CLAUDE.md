# robopi — learning journal

This repo documents Rebecca's hands-on journey learning embedded Linux,
GPIO programming, and robotics on a Raspberry Pi 4 Model B running
Raspberry Pi OS Lite 64-bit (Debian Trixie).

## project arc

The learning path moves through these stages in order:

1. GPIO basics — controlling hardware with Python and lgpio
2. Sensors and input — reading data from the physical world
3. ROS 2 (Jazzy) — installing and learning the Robot Operating System
4. ROS 2 nodes and topics — writing publishers and subscribers
5. Hardware integration — connecting sensors and actuators to ROS

## current focus

Stage 1: GPIO basics. The immediate goal is a working LED blink circuit
on GPIO 17, then building toward more complex GPIO control before
introducing ROS 2.

## hardware

- Raspberry Pi 4 Model B
- Hostname: robopi (ssh rebecca@robopi.local)
- OS: Raspberry Pi OS Lite 64-bit (Debian Trixie)
- GPIO library: lgpio (not RPi.GPIO — that is deprecated on Trixie)

## conventions

- Python for all GPIO and ROS node code
- Each stage lives in its own directory: `01-gpio/`, `02-sensors/`, `03-ros2/` etc.
- Each stage has its own `README.md` documenting what was learned and how to run it
- Code should be written to run on the Pi itself, not a dev machine
- Keep things simple — this is a learning journal, not a production codebase

## notes for Claude Code

- The target platform is ARM64 Linux, not macOS or x86
- Use lgpio for all GPIO access, never RPi.GPIO
- ROS 2 is not yet installed — do not assume it is available until stage 3
- When writing GPIO code, assume the circuit described in the stage README
- Prefer clear, well-commented code over clever code — this is for learning
