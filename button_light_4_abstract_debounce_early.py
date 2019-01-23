"""
LED that gets toggled when a button is pressed.
"""

from RPi import GPIO
import time

def turn_on_light(light_pin):
    print('Turning light on')
    GPIO.output(light_pin, GPIO.HIGH)

def turn_off_light(light_pin):
    print('Turning light off')
    GPIO.output(light_pin, GPIO.LOW)

def toggle_light(light_pin):
    if GPIO.input(light_pin) == GPIO.HIGH:
        turn_off_light(light_pin)
    else:
        turn_on_light(light_pin)

class debounce:
    called_time = None

    def __init__(self, func, delay):
        self.func = func
        self.delay = delay

    def __call__(self, *args, **kwargs):
        if self.called_time is None or time.time() - self.called_time > self.delay:
            self.func(*args, **kwargs)
            self.called_time = time.time()

if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)

    button_pin = 7
    light_pin = 11

    GPIO.setup(button_pin, GPIO.IN)
    GPIO.setup(light_pin, GPIO.OUT)

    try:
        # abstracted front-end debounce
        GPIO.add_event_detect(button_pin, GPIO.FALLING)
        debounced_toggle_light = debounce(lambda _: toggle_light(light_pin), delay=0.5)
        while True:
            if GPIO.event_detected(button_pin):
                debounced_toggle_light()

            time.sleep(0.01)

    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()
