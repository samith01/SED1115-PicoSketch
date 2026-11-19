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
    shoulder = radians(pose[0])
    bend = radians(ELBOW_ZERO - pose[1])

    x = ARM_MM * cos(shoulder) + ARM_MM * cos(shoulder + bend)
    y = ARM_MM * sin(shoulder) + ARM_MM * sin(shoulder + bend)
    return x, y


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
    home_x, home_y = pen_xy(HOME_POSE)
    xmax_x, xmax_y = pen_xy(X_MAX_POSE)
    ymax_x, ymax_y = pen_xy(Y_MAX_POSE)

    # where we want the pen, straight from the two knob positions
    tx = home_x + fx * (xmax_x - home_x) + fy * (ymax_x - home_x)
    ty = home_y + fx * (xmax_y - home_y) + fy * (ymax_y - home_y)

    # law of cosines gives the bend between the two arms
    d = sqrt(tx * tx + ty * ty)
    cos_bend = (d * d - 2 * ARM_MM * ARM_MM) / (2 * ARM_MM * ARM_MM)
    # clamp it so a target just out of reach can't crash the loop
    cos_bend = max(-1.0, min(1.0, cos_bend))
    bend = degrees(acos(cos_bend))

    # the target sits halfway along the bend, so take half off the bearing
    shoulder = degrees(atan2(ty, tx)) - bend / 2
    if shoulder < 0:
        # atan2 goes -180..180, servo angles only go 0..180
        shoulder = shoulder + 360
    elbow = ELBOW_ZERO - bend
    return shoulder, elbow
