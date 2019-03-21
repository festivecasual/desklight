import time

import RPi.GPIO as GPIO
from serial import Serial


s = Serial(port='/dev/ttyGS0', timeout=1)
buf = []

pins = {
    'red': 27,
    'green': 22,
    'blue': 17,
}

GPIO.setmode(GPIO.BCM)

for p in pins.values():
   GPIO.setup(p, GPIO.OUT)

active = False

while True:
    data = s.read().decode('ascii')

    buf.append(data)
    if data == '\n':
        buf = ''.join(buf).strip()
        if buf.startswith('Free'):
            GPIO.output(pins['green'], GPIO.HIGH)
            GPIO.output(pins['red'], GPIO.LOW)
        elif buf.startswith('Away'):
            GPIO.output(pins['green'], GPIO.LOW)
            GPIO.output(pins['red'], GPIO.LOW)
        elif buf.startswith('Busy'):
            GPIO.output(pins['green'], GPIO.LOW)
            GPIO.output(pins['red'], GPIO.HIGH)
        buf = []

    if data == u'':
        active = False
    else:
        active = True

    if active:
        GPIO.output(pins['blue'], GPIO.HIGH)
    else:
        for p in pins.values():
            GPIO.output(p, GPIO.LOW)

GPIO.cleanup()
