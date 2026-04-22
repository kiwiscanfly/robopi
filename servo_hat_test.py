#!/usr/bin/env python3
# Test 4 servos connected to P0-P3 on the SunFounder Robot HAT+ 5.
# Sweeps each servo one at a time so you can identify which is on which channel.
# Run on the Pi: python3 servo_hat_test.py

import time
from robot_hat import Servo

SERVO_CHANNELS = ["P0", "P1", "P2", "P3", "P7", "P8", "P9", "P10", "P11"]
HAT_I2C_ADDRESS = 0x15  # confirmed via i2cdetect — default is 0x14
STEP_DELAY = 0.01  # seconds between degree steps
SETTLE_DELAY = 0.5  # seconds to hold at end positions


def sweep(servo, start_angle, end_angle):
    step = 1 if end_angle > start_angle else -1
    for angle in range(start_angle, end_angle + step, step):
        servo.angle(angle)
        time.sleep(STEP_DELAY)


def test_channel(channel):
    print(f"\nChannel {channel}")
    input("  Press Enter to sweep this servo...")
    servo = Servo(channel, address=HAT_I2C_ADDRESS)

    servo.angle(0)
    time.sleep(SETTLE_DELAY)

    print("  → +90")
    sweep(servo, 0, 90)
    time.sleep(SETTLE_DELAY)

    print("  → -90")
    sweep(servo, 90, -90)
    time.sleep(SETTLE_DELAY)

    print("  → centre")
    sweep(servo, -90, 0)
    time.sleep(SETTLE_DELAY)


def main():
    print("Servo channel identification test")
    print("Each servo will sweep when you press Enter.")

    for channel in SERVO_CHANNELS:
        test_channel(channel)

    print("\nAll channels tested.")


if __name__ == "__main__":
    main()
