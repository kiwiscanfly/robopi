#!/usr/bin/env python3
"""Servo motor demo using hardware PWM via pigpio to eliminate jitter.

Wiring:
  Red wire   -> 5V (pin 2)
  Brown wire -> GND (pin 6)
  Orange wire (signal) -> GPIO 18 (pin 12)

Requires the pigpio daemon to be running on the Pi:
  sudo pigpiod
"""

from gpiozero import AngularServo
from gpiozero.pins.lgpio import LGPIOFactory
from time import sleep

# lgpio pin factory — more precise than the default software PWM
factory = LGPIOFactory()

# Pulse widths tuned for a typical SG90 servo — adjust if your servo behaves oddly
servo = AngularServo(
    18,
    min_pulse_width=0.0006,
    max_pulse_width=0.0023,
    pin_factory=factory,
)

PAUSE = 1.0  # seconds to hold each position


def main():
    print("Servo demo — sweeping through positions. Ctrl+C to stop.")

    positions = [
        (0,   "centre"),
        (90,  "full right"),
        (0,   "centre"),
        (-90, "full left"),
    ]

    try:
        while True:
            for angle, label in positions:
                print(f"Moving to {label} ({angle}°)")
                servo.angle = angle
                sleep(PAUSE)
    except KeyboardInterrupt:
        print("Stopping.")
    finally:
        servo.detach()  # stops sending PWM signal so servo doesn't strain holding position


if __name__ == "__main__":
    main()
