#!/usr/bin/env python3

import RPi.GPIO as GPIO
import requests
import math
import time


pwms = []
pins = [
    29, 31, 33,  # rgb (little)
    22,  # green (little)
    18,  # green (big)
    11, 13, 15,  # rgb (big)
    7,  # red
]


def load_route_config(route):
    return {
        'route': 45,
        'stop_coord': [-75.163861,39.926073],
        'direction': 'NorthBound',
        'thresholds': [
            0.012041569042285299,  # State 4
            0.009924757175874788,  # State 3
            # 0.008893667972218605,
            0.0076096783112062135,  # State 2
            # 0.0063416787209699945,
            0.005056295580758721,  # State 1
            # 0.0037998697346114914,
            0.0025383224775481017,  # State 0
        ]
    }

# [
#     [31307,'Broad St & Oregon Av - 2',(39.916565,-75.17125)],
#     [30858,'11th St & Oregon Av - FS',(39.916376,-75.165975)],
#     [21783,'11th St & Shunk St',(39.917384,-75.165758)],
#     [21784,'11th St & Porter St ',(39.918633,-75.165459)],
#     [21785,'11th St & Ritner St ',(39.919873,-75.165194)],
#     [21786,'11th St & Wolf St ',(39.921131,-75.16493)],
#     [21788,'11th St & Jackson St ',(39.922362,-75.164678)],
#     [16594,'11th St & Snyder Av',(39.923593,-75.164402)],
# ]


def euclid(X, Y):
    return sum((x - y) ** 2 for x, y in zip(X, Y)) ** 0.5


def check_for_updates(config):
    route = config['route']
    direction = config['direction']
    stop_coord = config['stop_coord']
    thresholds = config['thresholds']

    # Check for updates
    while True:
        try:
            response = requests.get('http://www3.septa.org/hackathon/TransitView/{route}'.format(route=route))
            data = response.json()
        except Exception as e:
            print(e)
            # If there's something wrong, just wait a bit and try again
            time.sleep(5)
        else:
            break

    next_state = None

    print('There are {cnt} buses on the line.'.format(cnt=len(data['bus'])))
    for idx, bus in enumerate(data['bus']):
        if bus['Direction'] != direction:
            print('{idx}. Wrong direction: {direction}'.format(idx=idx, direction=direction))
            continue

        if float(bus['lat']) > stop_coord[1]:
            print('{idx}. Too far north: {lat}'.format(idx=idx, lat=bus['lat']))
            continue

        dist = euclid(stop_coord, (float(bus['lng']), float(bus['lat'])))
        for state, threshold in enumerate(sorted(thresholds)):
            if dist < threshold:
                print('{idx}. At state {state}'.format(idx=idx, state=state))
                next_state = min(next_state or 99, state)
                break
    return next_state


def fadestepper(pwm, start_dc, end_dc, duration, interval=0.05):
    """
    Parameters
    - start_dc: The starting duty cycle (0 - 100)
    - end_dc: The final duty cycle (0 - 100)
    - duration: How long the fade should take (seconds)
    - interval: How long between fade steps (seconds; default
                0.05, or 50 milliseconds -- 20 steps per second)
    """
    try:
        iter(pwm)
    except TypeError:
        pwms = [pwm]
    else:
        pwms = pwm

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
        for pwm in pwms:
            pwm.ChangeDutyCycle(dc)
        yield

    for pwn in pwms:
        pwm.ChangeDutyCycle(end_dc)


def fade(pwms, start_dc, end_dc, duration, interval=0.05):
    for i, _ in enumerate(fadestepper(pwms, start_dc, end_dc, duration, interval)):
        elapsed = i * interval
        time.sleep(min(interval, duration - elapsed))


def fadeMulti(pwms, start_dcs, end_dcs, duration, interval=0.05):
    fadesteppers = \
        [fadestepper(pwm, start_dc, end_dc, 0.5) for pwm, start_dc, end_dc in zip(pwms, start_dcs, end_dcs)]

    while True:
        complete_fades = 0
        for fs in fadesteppers:
            try:
                next(fs)
            except StopIteration:
                complete_fades += 1
                if complete_fades == len(fadesteppers):
                    break

        # If we did not break out of the inner for loop go around and repeat
        # the loop again.
        else:
            continue

        # If we did break the inner for loop then we are done looping. Go ahead
        # and break out of the while loop.
        break



def freqsForNone():
    return [50, 100, 100, 100, 100, 100, 100, 100, 100]

def fadeToNone(fromfreqs):
    fadeMulti(pwms, fromfreqs, freqsForNone(), 1)

def patternNone():
    pwms[0].ChangeDutyCycle(50)
    fade(pwms[1], 100, 50, 1.5)
    fade(pwms[0], 50, 100, 1.5)
    fade(pwms[2], 100, 50, 1.5)
    fade(pwms[1], 50, 100, 1.5)
    fade(pwms[0], 100, 50, 1.5)
    fade(pwms[2], 50, 100, 1.5)



def freqsFor4():
    return [100, 0, 100, 0, 0, 100, 100, 100, 100]

def fadeTo4(fromfreqs):
    fadeMulti(pwms, fromfreqs, freqsFor4(), 1)

def pattern4():
    time.sleep(3)



def freqsFor3():
    return [100, 100, 100, 0, 0, 100, 100, 100, 100]

def fadeTo3(fromfreqs):
    fadeMulti(pwms, fromfreqs, freqsFor3(), 1)

def pattern3():
    pwms[3].ChangeDutyCycle(0)
    pwms[4].ChangeDutyCycle(0)
    time.sleep(3)



def freqsFor2():
    return [100, 100, 100, 100, 0, 100, 100, 100, 100]

def fadeTo2(fromfreqs):
    fadeMulti(pwms, fromfreqs, freqsFor2(), 1)

def pattern2():
    pwms[4].ChangeDutyCycle(0)
    time.sleep(3)



def freqsFor1():
    return [100, 100, 100, 100, 100, 0, 100, 100, 100]

def fadeTo1(fromfreqs):
    fadeMulti(pwms, fromfreqs, freqsFor1(), 1)

def pattern1():
    pwms[5].ChangeDutyCycle(0)
    fade(pwms[6], 100, 0, 0.5)
    fade(pwms[5], 0, 100, 0.5)
    fade(pwms[7], 100, 0, 0.5)
    fade(pwms[6], 0, 100, 0.5)
    fade(pwms[5], 100, 0, 0.5)
    fade(pwms[7], 0, 100, 0.5)



def freqsFor0():
    return freqsForNone()

def fadeTo0(fromfreqs):
    # Fade to the red light momentarily and slowly fade out. Then fade to the
    # None state.
    fadeMulti(pwms, fromfreqs, [100, 100, 100, 100, 100, 100, 100, 100, 0], 2)
    time.sleep(3)
    fade(pwms[8], 0, 100, 5)
    fadeToNone([100, 100, 100, 100, 100, 100, 100, 100, 100])

def pattern0():
    patternNone()



fadefunc = {
    None: fadeToNone,
    4: fadeTo4,
    3: fadeTo3,
    2: fadeTo2,
    1: fadeTo1,
    0: fadeTo0,
}

patternfunc = {
    None: patternNone,
    4: pattern4,
    3: pattern3,
    2: pattern2,
    1: pattern1,
    0: pattern0,
}

finalfreqs = {
    None: freqsForNone,
    4: freqsFor4,
    3: freqsFor3,
    2: freqsFor2,
    1: freqsFor1,
    0: freqsFor0,
    ...: freqsFor0,
}


def transition_state(state, new_state):
    # Choose the appropriate state's end frequencies and fade to the new state.
    if state != new_state:
        print('Fading from {state} to {new_state}'.format(state=state, new_state=new_state))
        fromfreqs = finalfreqs[state]()  # <- end frequencies of current state
        fadefunc[new_state](fromfreqs)  # <- function to fade to new state

    # Run the pattern for the new state
    patternfunc[new_state]()


def light_notification_loop(init_state, queue):
    # Set the initial state
    state = ...
    new_state = init_state

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
    config = load_route_config(45)

    # Start a thread for the loop
    from queue import Queue
    from threading import Thread
    q = Queue()
    thread = Thread(target=light_notification_loop, args=(None, q))
    thread.start()

    # Enter the listening loop
    try:
        while True:
            new_state = check_for_updates(config)
            q.put(new_state)
            time.sleep(3)
    except KeyboardInterrupt:
        print('Ending...')
        q.put('exit')
        thread.join()
        GPIO.cleanup()
        pass
