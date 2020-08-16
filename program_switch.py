"""
Cycle through different programs.
"""

import itertools as itertools
import threading as threading
from RPi import GPIO
from non_block_sense_hat import NonBlockSenseHat
import time

def day_1(interrupt, pin=7):
    """
    Morse code
    """
    import morse_code_hello_world as mc

    GPIO.setup(pin, GPIO.OUT)

    while True:
        if interrupt.is_set():
            break
        mc.pulse_message(pin, 'hello, world!')


def day_3(interrupt, pin=7):
    """
    Fading light
    From fade_light.py at 5cb7a3d8aa55bf498fc3b57f6ae0229af8ab3f9a
    """
    pass


def day_7(interrupt, red_pin=11, green_pin=13, blue_pin=15):
    """
    Cycle through RGB LED colors with sin waves
    From color_cycle.py at 8f0630def9b7218cc61a6e8d7c469c6b7cf4ffe9
    """
    pass


def day_8(interrupt, red_pin=11, green_pin=13, blue_pin=15):
    """
    Cycle through RGB LED colors by drawing one up/down at a time
    From color_cycle2.py at 83a4b0e1bbe35c4293451a08a73d849aed9aacce
    """
    pass


def day_10(interrupt, light_pin=7, button_pin=12):
    """
    Press a button to turn on a light, method 1
    From buttonbutton_light_1_managed.py at 805b5321a25465012f4b585873f1c2dbc927b49b
    """
    pass


def day_11(interrupt, light_pin=7, button_pin=12):
    """
    Press a button to toggle a light, method 2
    From button_light_2_manual_debounce_late.py at 437ece2db4b2339210b1ebaa1023a20b91194609
    """
    pass


def day_12(interrupt, light_pin=7, button_pin=12):
    """
    Press a button toggle a light, method 3
    From button_light_3_manual_debounce_early.py at b4529e75ce9fe516b9eb09032c32558262474bd8
    """
    pass


def day_13(interrupt, light_pin=7, button_pin=12):
    """
    Press a button, toggle a light, method 4
    From button_light_4_abstract_debounce_early.py at c34e8c110bb3a507ea17310d79cca5dbf950fc10
    """
    pass


class ProgramSwitcher:
    def __init__(self, button_pin=37):
        GPIO.setmode(GPIO.BOARD)

        self.button_pin = button_pin
        self.hat = NonBlockSenseHat()
        self.program_iter = itertools.cycle([
            (day_1, [], {}),
            (day_3, [], {}),
            (day_7, [], {}),
            (day_8, [], {}),
            (day_10, [], {}),
            (day_11, [], {}),
            (day_12, [], {}),
            (day_13, [], {}),
        ])
        self.program_interrupt = None
        self.program_thread = None

    def wait_for_button(self):
        GPIO.setup(self.button_pin, GPIO.IN)
        while True:
            print('Waiting for button press...')
            GPIO.add_event_detect(self.button_pin, GPIO.RISING)
            while not GPIO.event_detected(self.button_pin):
                time.sleep(0.05)
            self.switch_program()
            time.sleep(0.3)

    def switch_program(self):
        print('Switching programs...')
        if self.program_interrupt:
            self.stop_program()

        program, args, kwargs = next(self.program_iter)
        self.play_program(program, args, kwargs)

    def play_program(self, program, args, kwargs):
        print('Playing program ' + str(program) + '...')
        self.program_interrupt = threading.Event()
        self.program_thread = threading.Thread(target=program, args=[self.program_interrupt] + args, kwargs=kwargs)
        self.program_thread.start()

        self.message_thread, self.message_interrupt = self.hat.repeat_message(program.__doc__)

    def stop_program(self):
        print('Stopping program...')

        # Send a kill event and then wait for the thread(s) to complete
        self.program_interrupt.set()
        self.program_thread.join()

        self.message_interrupt.set()
        self.message_thread.join()

        self.program_interrupt = None
        self.program_thread = None

        self.message_interrupt = None
        self.message_thread = None

        GPIO.cleanup()

if __name__ == '__main__':
    switcher = ProgramSwitcher()

    try:
        switcher.wait_for_button()
    except KeyboardInterrupt:
        pass
    except:
        raise
    finally:
        switcher.stop_program()
