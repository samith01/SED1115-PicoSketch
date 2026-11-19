"""
test_arm_angles.py - unit tests for pen_xy and servo_angles (issues #27, #28)
Run on a laptop with:  python test_arm_angles.py
"""
from math import sqrt
from arm_angles import pen_xy, servo_angles
from jig_settings import *


def close(a, b):
    """Angles are floats, so allow a bit of rounding error."""
    return abs(a - b) < 0.5


# pen_xy: the arm can never reach further than both arms added together
for pose in (HOME_POSE, X_MAX_POSE, Y_MAX_POSE):
    x, y = pen_xy(pose)
    assert sqrt(x * x + y * y) <= 2 * ARM_MM + 0.01

# and the three poses should not all land on the same point
assert pen_xy(HOME_POSE) != pen_xy(X_MAX_POSE)

# servo_angles: the corners the jig was calibrated at (issue #28)
s, e = servo_angles(0, 0)
assert close(s, 20) and close(e, 30)

s, e = servo_angles(1, 0)
assert close(s, 140) and close(e, 30)

s, e = servo_angles(0, 1)
assert close(s, 90) and close(e, 85)

# halfway along X should sit between home and the far end
s, e = servo_angles(0.5, 0)
assert 20 < s < 140

# middle of the paper should still be a usable servo angle
s, e = servo_angles(0.5, 0.5)
assert 0 <= s <= 180 and 0 <= e <= 180

print("all arm tests passed")
