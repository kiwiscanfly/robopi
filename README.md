# robopi

A hands-on learning journal for embedded Linux and robotics on a
Raspberry Pi 4, documented as working code and notes.

## the journey

Starting from bare metal — a fresh Raspberry Pi OS Lite install —
and building toward a working ROS 2 robotics platform.

| Stage | Topic | Status |
|-------|-------|--------|
| 01 | GPIO basics — LED control | 🔧 in progress |
| 02 | Sensors and input | ⏳ upcoming |
| 03 | ROS 2 installation | ⏳ upcoming |
| 04 | ROS 2 nodes and topics | ⏳ upcoming |
| 05 | Hardware integration with ROS | ⏳ upcoming |

## hardware

- Raspberry Pi 4 Model B, 32 GB SD card
- OS: Raspberry Pi OS Lite 64-bit (Debian Trixie)

## setup
```bash
ssh rebecca@robopi.local
```

## notes

- GPIO library: lgpio (RPi.GPIO is deprecated on Trixie)
- ROS 2 distribution target: Jazzy Jalisco via rospian apt repo
