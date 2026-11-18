"""
test_servo_driver.py - unit tests for servo_driver.py
Owner: Samith Fernando
Run on a laptop with:  python test_servo_driver.py
init_servos needs the real Pico (machine module) so it is tested on the jig.
"""
from servo_driver import angle_to_duty, set_servo_angle, move_arm, set_pen, park_arm
from servo_translator import translate
from jig_settings import *


class FakePWM:
    """Stands in for machine.PWM so we can check what duty was set."""
    def __init__(self):
        self.duty = None
        self.off = False

    def duty_u16(self, value):
        self.duty = value

    def deinit(self):
        self.off = True


def make_servos():
    return {"shoulder": FakePWM(), "elbow": FakePWM(), "pen": FakePWM()}


cal = SERVO_CAL["shoulder"]

# angle_to_duty: ends and middle
assert angle_to_duty(0, cal) == 1638
assert angle_to_duty(180, cal) == 8192
assert angle_to_duty(90, cal) == 4915

# angle_to_duty: out of range angles get clamped
assert angle_to_duty(-20, cal) == 1638
assert angle_to_duty(200, cal) == 8192

# angle_to_duty should agree with the instructor's translate()
for a in [0, 20, 45, 90, 135, 180]:
    assert angle_to_duty(a, cal) == translate(a)

# set_servo_angle
pwm = FakePWM()
set_servo_angle(pwm, 90, cal)
assert pwm.duty == 4915

# move_arm sets both arm servos and leaves the pen alone
servos = make_servos()
move_arm(servos, 20, 30)
assert servos["shoulder"].duty == translate(20)
assert servos["elbow"].duty == translate(30)
assert servos["pen"].duty is None

# set_pen up and down
servos = make_servos()
set_pen(servos, True)
assert servos["pen"].duty == angle_to_duty(PEN_DOWN_ANGLE, SERVO_CAL["pen"])
set_pen(servos, False)
assert servos["pen"].duty == angle_to_duty(PEN_UP_ANGLE, SERVO_CAL["pen"])

# park_arm lifts pen, goes home and turns all servos off
servos = make_servos()
park_arm(servos)
assert servos["pen"].duty == angle_to_duty(PEN_UP_ANGLE, SERVO_CAL["pen"])
assert servos["shoulder"].duty == translate(HOME_SHOULDER)
assert servos["elbow"].duty == translate(HOME_ELBOW)
assert servos["shoulder"].off and servos["elbow"].off and servos["pen"].off

print("all servo_driver tests passed")
