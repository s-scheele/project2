from gpiozero import LED, Button
from time import sleep


led_green = LED(21)
led_yellow = LED(16)
led_red = LED(1)

button_green = Button(20)
button_yellow = Button(12)
button_red = Button(7)

while True:
  button_green.when_pressed = led_green.toggle
  sleep(0.5)

  button_yellow.when_pressed = led_yellow.toggle
  sleep(0.5)

  button_red.when_pressed = led_red.toggle
  sleep(0.5)
