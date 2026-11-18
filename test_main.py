"""
test_main.py - unit tests for the servo functions in main.py
Owner: Samith Fernando
Run on a laptop with:  python test_main.py
"""
from main import move_arm, set_pen, park_arm
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


# move_arm sets both arm servos and leaves the pen alone
servos = make_servos()
move_arm(servos, 20, 30)
assert servos["shoulder"].duty == translate(20)
assert servos["elbow"].duty == translate(30)
assert servos["pen"].duty is None

# set_pen up and down
servos = make_servos()
set_pen(servos, True)
assert servos["pen"].duty == translate(PEN_DOWN_ANGLE)
set_pen(servos, False)
assert servos["pen"].duty == translate(PEN_UP_ANGLE)

# park_arm lifts pen, goes home and turns all servos off
servos = make_servos()
park_arm(servos)
assert servos["pen"].duty == translate(PEN_UP_ANGLE)
assert servos["shoulder"].duty == translate(HOME_POSE[0])
assert servos["elbow"].duty == translate(HOME_POSE[1])
assert servos["shoulder"].off and servos["elbow"].off and servos["pen"].off

print("all main tests passed")
