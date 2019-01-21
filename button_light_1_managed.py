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

if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)

    button_pin = 7
    light_pin = 11

    GPIO.setup(button_pin, GPIO.IN)
    GPIO.setup(light_pin, GPIO.OUT)

    try:
        # auto debounce
        GPIO.add_event_detect(button_pin, GPIO.FALLING, callback=lambda _: toggle_light(light_pin), bouncetime=500)
        while True:
            time.sleep(0.01)

    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()
