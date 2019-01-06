"""
Single LED blinking "Hello, World!".
"""

from RPi import GPIO
import time

# I'm going to be using the Adafruit All About LEDs guide for this:
# https://learn.adafruit.com/all-about-leds

GPIO.setmode(GPIO.BOARD)

# Also, always handy is https://pinout.xyz/
outpin = 11
GPIO.setup(outpin, GPIO.OUT)

# I already know enough about Raspbery Pi GPIO programming to understand the
# mechanics behind blinking a light, so this is a little spin on "Hello, World".
# Here we define a mapping from letters/digits to morse code dots and dashes.
# The mapping is transcribed from https://en.wikipedia.org/wiki/Morse_code#/media/File:International_Morse_Code.svg.

code = {
    'A': '.-',
    'B': '-...',
    'C': '-.-.',
    'D': '-..',
    'E': '.',
    'F': '..-.',
    'G': '--.',
    'H': '....',
    'I': '..',
    'J': '.---',
    'K': '-.-',
    'L': '.-..',
    'M': '--',
    'N': '-.',
    'O': '---',
    'P': '.--.',
    'Q': '--.-',
    'R': '.-.',
    'S': '...',
    'T': '-',
    'U': '..-',
    'V': '...-',
    'W': '.--',
    'X': '-..-',
    'Y': '-.--',
    'Z': '--..',

    '1': '.----',
    '2': '..---',
    '3': '...--',
    '4': '....-',
    '5': '.....',
    '6': '-....',
    '7': '--...',
    '8': '---..',
    '9': '----.',
    '0': '-----',
}


# Pulsing
# -------

# To pulse a code, we need a few pieces of basic functionality:

def lighton():
    """ Turn a light on """
    print('\r.', end='')
    GPIO.output(outpin, GPIO.HIGH)

def lightoff():
    """ Turn a light off """
    print('\r ', end='')
    GPIO.output(outpin, GPIO.LOW)

def wait(d):
    """ Pause a certain amount of time """
    time.sleep(d)


# ------------------------------------------------------------------------------

# Using these basic functions, we build up more complex forms:

def pulse_pattern(pattern, unit=0.3):
    """ Given a specific pattern of dots and dashes, blink appropriately. """

    inpattern = False

    for s in pattern:

        # Before the first symbol, we are not between symbols, so we won't need
        # to pause. For subsequent symbols, pause one unit before blinking.
        if inpattern:
            wait(1 * unit)
        inpattern = True

        # Blinking is simple. For a dot, turn the light on for 1 unit of time.
        # For a dash, turn on for three units.
        lighton()
        if s == '.':
            wait(1 * unit)
        elif s == '-':
            wait(3 * unit)
        else:
            raise ValueError('Unrecognized symbol in {pattern!r}: {s!r}'.format(**locals()))
        lightoff()


def pulse_message(msg, unit=0.3):
    """ Given a message, blink appropriately. """

    inword = False

    for c in msg.upper():
        # There must always be a space between words. The space tells us that
        # we are starting a new word and should pause for 7 units of time.
        if c == ' ':
            inword = False
            wait(7 * unit)
            continue

        # Skip unrecognized characters.
        if c not in code:
            continue

        # If we've maded it to here, then we have a character to pulse. Before
        # the first character, we are not between characters, so we won't need
        # to pause. For subsequent characters, pause three units before blinking.
        if inword:
            wait(3 * unit)
        inword = True

        # Pulse out the pattern for the character.
        pattern = code[c]
        pulse_pattern(pattern, unit=unit)


if __name__ == '__main__':
    pulse_message('hello, world!')
    GPIO.cleanup()
