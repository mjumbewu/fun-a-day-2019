"""
cycle through colors of an RGB LED. Use pulse width modulation to draw one
color all the way up or down at a time.
"""

import RPi.GPIO as GPIO
import collections as coll
import math
import time

ColorPins = coll.namedtuple('ColorPins', ['red', 'green', 'blue'])

def fade(pwm, start_dc, end_dc, duration, interval=0.05):
    """
    Parameters
    - start_dc: The starting duty cycle (0 - 100)
    - end_dc: The final duty cycle (0 - 100)
    - duration: How long the fade should take (seconds)
    - interval: How long between fade steps (seconds; default
                0.05, or 50 milliseconds -- 20 steps per second)
    """
    # How many dim steps. For example, if we want a duration of 5s with a step
    # interval of 1s, then we'll have 6 steps (including the start and end with
    # 5 1s pauses in between). If we want a duration of 2.5s with 1s steps then
    # we'lll have 3 steps (the start and end, with two 1s pauses and a 0.5s
    # pause). Round to leave room for floating point approximation
    num_steps = math.ceil(round(duration / interval, 4))

    # Calculate the size of each step. Note this only applies to the full-length
    # steps. In the cases above, if we fade from 0 to 100 duty cycle, in the 5s
    # case we would have a dc_step of 20, whereas in the 2.5s case we would have
    # a dc_step of 40, even though the last step would only be 20.
    dc_step = (end_dc - start_dc) * interval / duration

    for i in range(num_steps):
        dc = start_dc + i * dc_step
        pwm.ChangeDutyCycle(dc)
        elapsed = i * interval
        time.sleep(min(interval, duration - elapsed))
    pwm.ChangeDutyCycle(end_dc)

def fadeup(p):
    fade(p, 100, 0, 3, interval=0.1)

def fadedown(p):
    fade(p, 0, 100, 3, interval=0.1)

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

    try:
        fadeup(pwm.red)
        while True:
            fadeup(pwm.green)
            fadedown(pwm.red)
            fadeup(pwm.blue)
            fadedown(pwm.green)
            fadeup(pwm.red)
            fadedown(pwm.blue)
    except KeyboardInterrupt:
        for m in pwm:
            m.stop()
        GPIO.cleanup()
