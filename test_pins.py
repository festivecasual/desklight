import time

import RPi.GPIO as GPIO


pins = {
    'green': 25,
    'red': 23,
}

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

for p in pins.values():
   GPIO.setup(p, GPIO.OUT)

GPIO.output(pins['red'], GPIO.HIGH)
GPIO.output(pins['green'], GPIO.LOW)
time.sleep(5)

GPIO.output(pins['green'], GPIO.HIGH)
GPIO.output(pins['red'], GPIO.LOW)
time.sleep(5)

GPIO.cleanup()

