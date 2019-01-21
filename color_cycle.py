"""
Cycle through colors of an RGB LED using pulse width modulation. Use a sin wave
function to determine the intesity of each color.
"""

import RPi.GPIO as GPIO
import collections as coll
import math
import time

ColorPins = coll.namedtuple('ColorPins', ['red', 'green', 'blue'])

def pinoff(pins):
    if isinstance(pins, int):
        pins = (pins,)
    for pin in pins:
        GPIO.output(pin, GPIO.LOW)

def pinon(pins):
    if isinstance(pins, int):
        pins = (pins,)
    for pin in pins:
        GPIO.output(pin, GPIO.HIGH)

def scaled_sin(xshift=0, yshift=1, period=(2*math.pi), amplitude=2):
    return lambda x: (math.sin((x - xshift) * 2 * math.pi / period) + (2 * yshift / amplitude)) * amplitude / 2

if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)

    pins = ColorPins(11, 7, 12)
    for p in pins:
        GPIO.setup(p, GPIO.OUT)

    pwm = ColorPins(
        GPIO.PWM(pins.red, 1000),
        GPIO.PWM(pins.green, 1000),
        GPIO.PWM(pins.blue, 1000),
    )

    for m in pwm:
        m.start(100)

    redf = scaled_sin(xshift=0, yshift=50, period=12, amplitude=100)
    greenf = scaled_sin(xshift=3, yshift=50, period=12, amplitude=100)
    bluef = scaled_sin(xshift=6, yshift=50, period=12, amplitude=100)

    try:
        i = 0
        while True:
            x = i / 10
            pwm.red.ChangeDutyCycle(redf(x))
            pwm.green.ChangeDutyCycle(greenf(x))
            pwm.blue.ChangeDutyCycle(bluef(x))
            time.sleep(0.2)
            i += 1
    except KeyboardInterrupt:
        GPIO.cleanup()
