"""
A "simple" (who am I kidding; I don't know how simple it might be) fading LED.
"""

from RPi import GPIO
import time

GPIO.setmode(GPIO.BOARD)

outpin = 33
GPIO.setup(outpin, GPIO.OUT)


def about_equal(x, y, threshold=0.001):
    return (y - threshold) >= x >= (y + threshold)


def fade(pwm, start_dc, end_dc, duration, interval=0.05):
    """
    Parameters
    - start_dc: The starting duty cycle (0 - 100)
    - end_dc: The final duty cycle (0 - 100)
    - duration: How long the fade should take (seconds)
    - interval: How long between fade steps (seconds;
                default 0.05, or 20 steps per second)
    """
    dc_step = (end_dc - start_dc) * interval / duration
    i = 0
    while True:
        dc = start_dc + i * dc_step
        pwm.ChangeDutyCycle(min(100, max(0, dc)))
        t = i * interval
        if t > duration or about_equal(t, duration): break
        i += 1
        time.sleep(interval)


if __name__ == '__main__':
    pwm = GPIO.PWM(outpin, 100)
    pwm.start(0)
    fade(pwm, 0, 100, 1)
    fade(pwm, 100, 0, 2)
    fade(pwm, 0, 100, 1)
    fade(pwm, 100, 0, 2)
    pwm.stop()
