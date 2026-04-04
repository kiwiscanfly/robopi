from gpiozero import PWMLED

RED_PIN = 17
GREEN_PIN = 27
BLUE_PIN = 22

red = PWMLED(RED_PIN)
green = PWMLED(GREEN_PIN)
blue = PWMLED(BLUE_PIN)

red.off()
green.off()
blue.off()
