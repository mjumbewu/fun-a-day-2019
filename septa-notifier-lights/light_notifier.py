#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
import notifier


pwms = []
pins = [
    29, 31, 33,  # rgb (little)
    22,  # green (little)
    18,  # green (big)
    11, 13, 15,  # rgb (big)
    7,  # red
]

def transition_state(state, new_state):
    # Turn off old state
    if state != new_state:
        pwms[0].ChangeDutyCycle(100)
        pwms[1].ChangeDutyCycle(100)
        pwms[2].ChangeDutyCycle(100)

        pwms[3].ChangeDutyCycle(100)

        pwms[4].ChangeDutyCycle(100)

        pwms[5].ChangeDutyCycle(100)
        pwms[6].ChangeDutyCycle(100)
        pwms[7].ChangeDutyCycle(100)

        pwms[8].ChangeDutyCycle(100)

    # Turn on the new state
    if new_state == None:
        pwms[2].ChangeDutyCycle(0)
        pwms[0].ChangeDutyCycle(0)
        time.sleep(0.5)
        pwms[2].ChangeDutyCycle(100)
        time.sleep(0.5)
        pwms[1].ChangeDutyCycle(0)
        time.sleep(0.5)
        pwms[0].ChangeDutyCycle(100)
        time.sleep(0.5)
        pwms[2].ChangeDutyCycle(0)
        time.sleep(0.5)
        pwms[1].ChangeDutyCycle(100)
        time.sleep(0.5)

    elif new_state == 4:
        pwms[0].ChangeDutyCycle(100)
        pwms[1].ChangeDutyCycle(0)
        pwms[2].ChangeDutyCycle(100)

        pwms[3].ChangeDutyCycle(0)

        pwms[4].ChangeDutyCycle(0)
        time.sleep(3)

    elif new_state == 3:
        pwms[3].ChangeDutyCycle(0)

        pwms[4].ChangeDutyCycle(0)
        time.sleep(3)

    elif new_state == 2:
        pwms[4].ChangeDutyCycle(0)
        time.sleep(3)

    elif new_state == 1:
        pwms[5].ChangeDutyCycle(100)
        pwms[6].ChangeDutyCycle(0)
        pwms[7].ChangeDutyCycle(0)
        time.sleep(3)

    elif new_state == 0:
        pwms[8].ChangeDutyCycle(0)
        time.sleep(3)


def light_notification_loop(init_state, queue):
    state = init_state
    new_state = state
    while True:
        print('Current state is {state}\n'.format(state=state))
        while not queue.empty():
            new_state = queue.get()

        if new_state == 'exit':
            break

        transition_state(state, new_state)
        state = new_state


if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)

    for pin in pins:
        GPIO.setup(pin, GPIO.OUT, initial=GPIO.HIGH)
        pwm = GPIO.PWM(pin, 100)
        pwm.start(100)
        pwms.append(pwm)

    # Load the route config
    config = notifier.load_route_config(45)

    # Start a thread for the loop
    from queue import Queue
    from threading import Thread
    q = Queue()
    thread = Thread(target=light_notification_loop, args=(None, q))
    thread.start()

    # Enter the listening loop
    try:
        while True:
            new_state = notifier.check_for_updates(config)
            q.put(new_state)
            time.sleep(3)
    except KeyboardInterrupt:
        print('Ending...')
        q.put('exit')
        thread.join()
        GPIO.cleanup()
        pass
