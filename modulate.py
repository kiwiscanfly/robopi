#!/usr/bin/env python3
"""RGB LED colour cycling using PWM on a common cathode RGB LED.

Wiring (common cathode):
  Longest pin (cathode) -> GND (pin 6)
  Red leg   -> 470Ω -> GPIO 17 (pin 11)
  Green leg -> 470Ω -> GPIO 27 (pin 13)
  Blue leg  -> 470Ω -> GPIO 22 (pin 15)
"""

import time
from gpiozero import PWMLED  # PWMLED allows values between 0.0 (off) and 1.0 (full brightness)

# GPIO pin numbers for each colour channel
RED_PIN = 17
GREEN_PIN = 27
BLUE_PIN = 22

# Controls the speed and smoothness of colour transitions
STEP_DELAY = 0.02  # seconds to wait between each step (lower = faster)
STEPS = 100        # number of steps per transition (higher = smoother)


def fade_colour(leds, from_colour, to_colour, steps=STEPS):
    """Gradually transition all three LED channels from one colour to another.

    Each channel is interpolated independently from its starting brightness
    to its target brightness over the given number of steps.
    """
    red, green, blue = leds
    for step in range(steps + 1):
        # progress goes from 0.0 (start) to 1.0 (end) across all steps
        progress = step / steps
        # Linear interpolation: start + (end - start) * progress
        red.value   = from_colour[0] + (to_colour[0] - from_colour[0]) * progress
        green.value = from_colour[1] + (to_colour[1] - from_colour[1]) * progress
        blue.value  = from_colour[2] + (to_colour[2] - from_colour[2]) * progress
        time.sleep(STEP_DELAY)


def main():
    # Initialise one PWMLED per colour channel
    red = PWMLED(RED_PIN)
    green = PWMLED(GREEN_PIN)
    blue = PWMLED(BLUE_PIN)

    print("Starting RGB colour cycle. Ctrl+C to stop.")

    # Each tuple is (red, green, blue) brightness 0.0 to 1.0
    colours = [
        (1.0, 0.0, 0.0),  # red
        (1.0, 0.5, 0.0),  # orange
        (1.0, 1.0, 0.0),  # yellow
        (0.0, 1.0, 0.0),  # green
        (0.0, 0.0, 1.0),  # blue
        (0.5, 0.0, 1.0),  # purple
        (1.0, 1.0, 1.0),  # white
        (0.0, 0.0, 0.0),  # off
    ]

    leds = (red, green, blue)
    try:
        while True:
            for i, colour in enumerate(colours):
                # Wrap around to the first colour after the last one
                next_colour = colours[(i + 1) % len(colours)]
                fade_colour(leds, colour, next_colour)
    except KeyboardInterrupt:
        print("Stopping.")
    finally:
        # Always turn all LEDs off on exit, even if an error occurs
        red.off()
        green.off()
        blue.off()


if __name__ == "__main__":
    main()
