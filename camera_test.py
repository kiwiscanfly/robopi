#!/usr/bin/env python3
# Stream the PiDog camera over HTTP via vilib.
# Access the feed at http://robopi.local:9000 in your browser.
# Run on the Pi: python3 camera_test.py

from vilib import Vilib

def main():
    print("Starting camera...")
    Vilib.camera_start(vflip=False, hflip=False)
    Vilib.show_fps()

    print("Starting web stream at http://robopi.local:9000/mjpg")
    Vilib.display(local=False, web=True)

    input("Stream running — press Enter to stop.\n")

    Vilib.camera_close()
    print("Camera stopped.")


if __name__ == "__main__":
    main()
