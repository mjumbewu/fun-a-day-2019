"""
A "simple" (who am I kidding; I don't know how simple it might be) fading LED.
"""

from RPi import GPIO
import math
import time

# I'm working through this with a couple of different sources. The first is an
# article on how pulse width modulation works with LEDs[1]. It's neat that, by
# it's explanation, the dimming is basically atrick of the eye owing to the fact
# that we can only perceive change at a certain frequency. The second is the
# RPi.GPIO docs[2].
#
# [1] https://electronicshobbyists.com/raspberry-pi-pwm-tutorial-control-brightness-of-led-and-servo-motor/
# [2] https://sourceforge.net/p/raspberry-gpio-python/wiki/PWM/

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

if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)

    outpin = 33
    GPIO.setup(outpin, GPIO.OUT)
    pwm = GPIO.PWM(outpin, 100)

    pwm.start(0)
    fade(pwm, 0, 100, 1)
    fade(pwm, 100, 0, 2)
    fade(pwm, 0, 100, 1)
    fade(pwm, 100, 0, 2)
    pwm.stop()

    GPIO.cleanup()
