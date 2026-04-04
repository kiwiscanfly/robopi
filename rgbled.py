from gpiozero import RGBLED
from colorzero import Color

# GPIO pin numbers for each colour channel
RED_PIN = 17
GREEN_PIN = 27
BLUE_PIN = 22

led = RGBLED(RED_PIN, GREEN_PIN, BLUE_PIN)


def main():
    print("Setting LED to red")
    led.color = Color("red")
    input("Press Enter to continue...")

    print("Setting LED to green")
    led.color = Color("green")
    input("Press Enter to continue...")

    print("Setting LED to blue")
    led.color = Color("blue")
    input("Press Enter to continue...")

    print("Setting LED to white")
    led.color = Color("white")
    input("Press Enter to continue...")

    print("Turning LED off")
    led.off()


if __name__ == "__main__":
    main()
