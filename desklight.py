import time
import subprocess

import RPi.GPIO as GPIO
from serial import Serial, SerialException


s = Serial(port='/dev/ttyGS0', timeout=1)

buf = []

pins = {
    'red': 23,
    'green': 25,
}

shutdown_pin = 26

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

for p in pins.values():
   GPIO.setup(p, GPIO.OUT)

GPIO.setup(shutdown_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while GPIO.input(shutdown_pin) == GPIO.HIGH:
    try:
        data = s.read().decode('ascii')
    except SerialException:
        data = None
        s = Serial(port='/dev/ttyGS0', timeout=1)

    if data:
        buf.append(data)
    else:
        for p in pins.values():
            GPIO.output(p, GPIO.LOW)

    if data == '\n':
        buf = ''.join(buf).strip()
        if buf == 'available':
            GPIO.output(pins['green'], GPIO.HIGH)
            GPIO.output(pins['red'], GPIO.LOW)
        elif buf == 'away':
            GPIO.output(pins['red'], GPIO.LOW)
            if time.monotonic() % 1 < 0.8:
                GPIO.output(pins['green'], GPIO.LOW)
            else:
                GPIO.output(pins['green'], GPIO.HIGH)
        elif buf == 'busy':
            GPIO.output(pins['green'], GPIO.LOW)
            GPIO.output(pins['red'], GPIO.HIGH)
        elif buf == 'busy_strobe':
            GPIO.output(pins['green'], GPIO.LOW)
            if time.monotonic() % 1 < 0.5:
                GPIO.output(pins['red'], GPIO.LOW)
            else:
                GPIO.output(pins['red'], GPIO.HIGH)
        buf = []

GPIO.cleanup()
subprocess.run(['/sbin/shutdown', '-h', 'now'])

