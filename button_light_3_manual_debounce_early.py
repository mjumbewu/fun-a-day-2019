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
        # front-end debounce
        GPIO.add_event_detect(button_pin, GPIO.FALLING)
        detected_time = time.time()
        while True:
            if GPIO.event_detected(button_pin):
                if detected_time is None:
                    print('detected_time is none')
                    toggle_light(light_pin)
                    detected_time = time.time()

            if detected_time and time.time() - detected_time > 0.5:
                detected_time = None

            time.sleep(0.01)

    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()
