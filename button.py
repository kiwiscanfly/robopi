from gpiozero import Button, RGBLED
from colorzero import Color
from signal import pause

# GPIO pin numbers for each colour channel
RED_PIN = 17
GREEN_PIN = 27
BLUE_PIN = 22

button = Button(2)
led = RGBLED(RED_PIN, GREEN_PIN, BLUE_PIN)

color_arr = [Color("red"), Color("green"), Color("blue"), Color("white")]
color_index = 0


def on_button_pressed():
    global color_index
    print("Button was pressed!")
    led.color = color_arr[color_index]
    color_index = (color_index + 1) % len(color_arr)


def on_button_released():
    print("Button was released!")
    led.off()


button.when_pressed = on_button_pressed
button.when_released = on_button_released

pause()
