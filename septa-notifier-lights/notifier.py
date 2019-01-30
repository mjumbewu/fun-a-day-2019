#!/usr/bin/env python3

import requests
import time


def load_route_config(route):
    return {
        'route': 45,
        'stop_coord': [-75.163861,39.926073],
        'direction': 'NorthBound',
        'thresholds': [
            0.012041569042285299,
            0.009924757175874788,
            0.008893667972218605,
            0.0076096783112062135,
            0.0063416787209699945,
            0.005056295580758721,
            0.0037998697346114914,
            0.0025383224775481017,
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
    try:
        response = requests.get('http://www3.septa.org/hackathon/TransitView/{route}'.format(route=route))
    except Exception as e:
        print(e)
        # If there's something wrong, just wait a bit and try again
        time.sleep(5)
        return

    data = response.json()
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


def transition_state(state, new_state):
    pass


def notification_loop(init_state, queue):
    state = init_state
    new_state = state
    while True:
        print('Current state is {state}\n'.format(state=state))
        while not queue.empty():
            new_state = queue.get()

        if new_state == 'exit':
            break

        if new_state != state:
            transition_state(state, new_state)
            state = new_state

        time.sleep(3)


if __name__ == '__main__':
    # Load the route config
    config = load_route_config(45)

    # Start a thread for the loop
    from queue import Queue
    from threading import Thread
    q = Queue()
    thread = Thread(target=notification_loop, args=(None, q))
    thread.start()

    # Enter the listening loop
    try:
        while True:
            new_state = check_for_updates(config)
            q.put(new_state)
            time.sleep(3)
    except KeyboardInterrupt:
        q.put('exit')
        thread.join()
        pass
