"""
servo_driver.py - converts angles to 50 Hz PWM duty cycles and drives
the shoulder, elbow and pen servos (through the safe arm-control
function provided by the instructor).
Owner: Samith Fernando
"""
import time
from jig_settings import *

# translate() is the safe servo function given to us by the instructor
# (servo_translator.py, SED1115 lab files). It turns an angle into a
# duty_u16 value and clamps it to 0..180 so the servo can't be damaged.
from servo_translator import translate


def init_servos(pins, freq):
    """
    Owner: Samith Fernando
    Inputs:  pins (dict) - {"shoulder": int, "elbow": int, "pen": int};
             freq (int) - PWM frequency, 50 Hz.
    Outputs: dict of machine.PWM objects with the same keys.
    Operation: creates a PWM object per servo pin and sets its frequency.
    """
    from machine import PWM, Pin

    servos = {}
    for name in pins:
        pwm = PWM(Pin(pins[name]))
        pwm.freq(freq)
        servos[name] = pwm
    return servos


def angle_to_duty(angle, cal):
    """
    Owner: Samith Fernando
    Inputs:  angle (float) - degrees 0 to 180; cal (dict) - {"duty_0", "duty_180"}.
    Outputs: int - duty_u16 value for that angle.
    Operation: clamps angle to 0..180 and interpolates linearly between
               the calibrated duty values.
    """
    if angle < 0:
        angle = 0
    if angle > 180:
        angle = 180
    duty = cal["duty_0"] + (cal["duty_180"] - cal["duty_0"]) * angle / 180
    return int(duty)


def set_servo_angle(pwm, angle, cal):
    """
    Owner: Samith Fernando
    Inputs:  pwm (machine.PWM); angle (float); cal (dict).
    Outputs: None.
    Operation: pwm.duty_u16(angle_to_duty(angle, cal)).
    """
    pwm.duty_u16(angle_to_duty(angle, cal))


def move_arm(servos, shoulder, elbow):
    """
    Owner: Samith Fernando
    Inputs:  servos (dict of PWM); shoulder, elbow (float) - degrees.
    Outputs: None.
    Operation: passes the two angles to the instructor-provided safe
               arm-control function (credited in a comment), which moves
               the shoulder and elbow servos without damaging the arm.
    """
    servos["shoulder"].duty_u16(translate(shoulder))
    servos["elbow"].duty_u16(translate(elbow))


def set_pen(servos, pen_down):
    """
    Owner: Samith Fernando
    Inputs:  servos (dict of PWM); pen_down (bool).
    Outputs: None.
    Operation: sets the pen servo to PEN_DOWN_ANGLE or PEN_UP_ANGLE.
    """
    if pen_down:
        set_servo_angle(servos["pen"], PEN_DOWN_ANGLE, SERVO_CAL["pen"])
    else:
        set_servo_angle(servos["pen"], PEN_UP_ANGLE, SERVO_CAL["pen"])


def park_arm(servos):
    """
    Owner: Samith Fernando
    Inputs:  servos (dict of PWM).
    Outputs: None.
    Operation: lifts the pen, moves the arm to HOME_SHOULDER / HOME_ELBOW
               and turns PWM off. Called when the program stops.
    """
    set_pen(servos, False)
    move_arm(servos, HOME_SHOULDER, HOME_ELBOW)
    time.sleep(0.5)  # give the servos time to get there before turning off
    for name in servos:
        servos[name].deinit()
