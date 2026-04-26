#!/usr/bin/env python3
"""Hello world example for robopi."""

import gpiozero
import time


def main():
    """Main function."""
    print("Hello world!")
    led = gpiozero.LED(17)
    for _ in range(5):
        led.on()
        time.sleep(0.5)
        led.off()
        time.sleep(0.5)
    print("Done")


if __name__ == "__main__":
    main()
