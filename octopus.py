from RPi import GPIO
import time
import fade_light as fl

def channel_on(pin, brightness):
    GPIO.output(pin, GPIO.LOW)

if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)

    red_pin = 7
    multi2_b_pin = 11
    multi2_g_pin = 13
    multi2_r_pin = 15
    green2_pin = 18
    green1_pin = 22
    multi1_b_pin = 29
    multi1_g_pin = 31
    multi1_r_pin = 33

    all_pins = [
        red_pin,
        multi2_b_pin,
        multi2_g_pin,
        multi2_r_pin,
        green2_pin,
        green1_pin,
        multi1_b_pin,
        multi1_g_pin,
        multi1_r_pin,
    ]

    for p in all_pins:
        GPIO.setup(p, GPIO.OUT)

    red_pwm = GPIO.PWM(red_pin, 100)
    multi2_b_pwm = GPIO.PWM(multi2_b_pin, 100)
    multi2_g_pwm = GPIO.PWM(multi2_g_pin, 100)
    multi2_r_pwm = GPIO.PWM(multi2_r_pin, 100)
    green2_pwm = GPIO.PWM(green2_pin, 100)
    green1_pwm = GPIO.PWM(green1_pin, 100)
    multi1_b_pwm = GPIO.PWM(multi1_b_pin, 100)
    multi1_g_pwm = GPIO.PWM(multi1_g_pin, 100)
    multi1_r_pwm = GPIO.PWM(multi1_r_pin, 100)

    all_pwms = [
        red_pwm,
        multi2_b_pwm,
        multi2_g_pwm,
        multi2_r_pwm,
        green2_pwm,
        green1_pwm,
        multi1_b_pwm,
        multi1_g_pwm,
        multi1_r_pwm,
    ]

    for p in all_pwms:
        p.start(100)

    prev_p = None
    for p in all_pwms:
        fl.fade(p, 100, 0, 1)
        if prev_p:
            fl.fade(prev_p, 0, 100, 1)
        prev_p = p
    fl.fade(prev_p, 0, 100, 1)

    GPIO.cleanup()
