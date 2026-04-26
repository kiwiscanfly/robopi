#!/usr/bin/env python3
# Test the RGB LEDs on the PiDog v2.
# Cycles through each built-in effect with a keypress between each one.
# Run on the Pi: python3 led_test.py

import time
from pidog import Pidog
from robot_hat.music import disable_speaker

HOLD_TIME = 3  # seconds to show each effect

EFFECTS = [
    ("breath", "white",  1,   1.0),
    ("breath", "pink",   1,   1.0),
    ("breath", "red",    1,   1.0),
    ("bark",   "red",    2,   1.0),
    ("boom",   "white",  1,   1.0),
    ("listen", "white",  1,   0.8),
]


def main():
    print("Initialising PiDog...")
    dog = Pidog()
    disable_speaker()
    time.sleep(0.5)

    print("RGB LED test — press Enter to advance through each effect.\n")

    for style, color, bps, brightness in EFFECTS:
        input(f"  Press Enter for: {style} / {color}...")
        dog.rgb_strip.set_mode(style=style, color=color, bps=bps, brightness=brightness)
        time.sleep(HOLD_TIME)

    print("\nTurning off LEDs.")
    dog.rgb_strip.close()
    print("Done.")


if __name__ == "__main__":
    main()
