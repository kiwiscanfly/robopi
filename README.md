# robopi

A hands-on learning journal for embedded Linux and robotics on a
Raspberry Pi 4, documented as working code and notes.

## hardware

- Raspberry Pi 4 Model B, 32 GB SD card
- OS: Raspberry Pi OS Lite 64-bit (Debian Trixie)

## setup

```bash
ssh rebecca@robopi.local
```

## session notes

| Date | Topics |
| ---- | ------ |
| [4 April 2026](notes/26-04-04.md) | GitHub setup, Pi boot troubleshooting, WiFi/NetworkManager, SSH, resistors, RGB LED, PWM, GPIO cleanup, locale fix |
| [5 April 2026](notes/26-04-05.md) | Servo motor, jitter fix with LGPIOFactory, Adafruit 16-channel servo HAT |

## notes

- GPIO library: lgpio (RPi.GPIO is deprecated on Trixie)
- ROS 2 distribution target: Jazzy Jalisco via [rospian](https://github.com/rospian/rospian-repo) apt repo
