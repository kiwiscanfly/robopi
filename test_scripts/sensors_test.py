#!/usr/bin/env python3
# Test the dual touch and ultrasonic modules on the PiDog v2.
# Touch the head sensors and wave your hand in front of the ultrasonic
# to confirm wiring is correct.
# Run on the Pi: python3 sensors_test.py

import time
from pidog import Pidog
from robot_hat.music import disable_speaker

LOOP_DELAY = 0.1  # seconds between readings


def main():
    print("Initialising PiDog...")
    dog = Pidog()
    disable_speaker()
    time.sleep(0.5)
    print("PiDog initialised.")
    print("\nReading sensors — Ctrl+C to stop.\n")
    print(f"{'Touch L':<12}{'Touch R':<12}{'Distance (cm)':<16}")
    print("-" * 40)

    while True:
        touch = dog.dual_touch.read()
        distance = dog.ultrasonic.read()

        touched_l = "TOUCHED" if touch in ("L", "LS", "RS") else "---"
        touched_r = "TOUCHED" if touch in ("R", "LS", "RS") else "---"
        dist_str = f"{distance:.1f}" if distance is not None else "---"

        print(f"{touched_l:<12}{touched_r:<12}{dist_str:<16}  (touch={touch!r})", end="\r")
        time.sleep(LOOP_DELAY)


if __name__ == "__main__":
    main()
