import time
import subprocess

import RPi.GPIO as GPIO
from serial import Serial, SerialException


s = Serial(port='/dev/ttyGS0', timeout=1)

buf = []

pins = {
    'red': 27,
    'green': 22,
    'blue': 17,
}

shutdown_pin = 26

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

for p in pins.values():
   GPIO.setup(p, GPIO.OUT)

GPIO.setup(shutdown_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

active = False

while GPIO.input(shutdown_pin) == GPIO.HIGH:
    try:
        data = s.read().decode('ascii')
    except SerialException:
        data = None
        s = Serial(port='/dev/ttyGS0', timeout=1)

    if data:
        buf.append(data)

    if data == '\n':
        buf = ''.join(buf).strip()
        if buf == 'available':
            GPIO.output(pins['green'], GPIO.HIGH)
            GPIO.output(pins['red'], GPIO.LOW)
            print('available')
        elif buf == 'away':
            GPIO.output(pins['green'], GPIO.LOW)
            GPIO.output(pins['red'], GPIO.LOW)
            print('away')
        elif buf == 'busy':
            GPIO.output(pins['green'], GPIO.LOW)
            GPIO.output(pins['red'], GPIO.HIGH)
            print('busy')
        elif buf == 'busy_strobe':
            GPIO.output(pins['green'], GPIO.LOW)
            if time.monotonic() % 1 < 0.5:
                GPIO.output(pins['red'], GPIO.HIGH)
                print('strobe: lo')
            else:
                GPIO.output(pins['red'], GPIO.HIGH)
                print('strobe: hi')
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
subprocess.run(['/sbin/shutdown', '-h', 'now'])

