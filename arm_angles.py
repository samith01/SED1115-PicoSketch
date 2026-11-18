"""
arm_angles.py - turns a knob position into shoulder and elbow servo
angles so the pen moves in straight X and Y lines.
No hardware code, so it can be tested on a laptop.
Owner: Ryan Hannum Horne
"""
from math import atan2, acos, cos, sin, sqrt, radians, degrees
from jig_settings import *


def pen_xy(pose):
    """
    Owner: Ryan Hannum Horne
    Inputs:  pose (tuple) - (shoulder, elbow) servo angles in degrees.
    Outputs: (x, y) tuple - pen position in mm, measured from the shoulder.
    Operation: forward kinematics. bend = ELBOW_ZERO - elbow, then
               x = ARM_MM*cos(s) + ARM_MM*cos(s + bend), same with sin for y.
    """
    pass


def servo_angles(fx, fy):
    """
    Owner: Ryan Hannum Horne
    Inputs:  fx, fy (float 0.0 to 1.0) - how far along X and Y the pen
             should be (straight from knob()).
    Outputs: (shoulder, elbow) tuple - servo angles in degrees.
    Operation: 1. pen_xy() on HOME_POSE, X_MAX_POSE, Y_MAX_POSE gives the
                  3 corners of the drawing area.
               2. target = home + fx*(xmax - home) + fy*(ymax - home)
               3. law of cosines on the distance d to the target gives
                  the bend, atan2 gives the shoulder.
               4. elbow = ELBOW_ZERO - bend. Check: (0,0) -> (20,30),
                  (1,0) -> (140,30), (0,1) -> (90,85).
    """
    pass
