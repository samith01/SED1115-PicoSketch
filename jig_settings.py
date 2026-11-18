"""
jig_settings.py - constants for the PicoSketch brachiograph.
Owner: Samith Fernando
No functions: pin numbers and values we measured on the jig.
"""

# Input pins (accessory board)
X_POT_PIN = 26          # ADC0, horizontal knob
Y_POT_PIN = 27          # ADC1, vertical knob
PEN_SWITCH_PIN = 12     # wired with pull-down (1 = pressed)

# Raw knob range measured on the accessory board
KNOB_MIN = 320
KNOB_MAX = 65535

# Servo PWM pins
SHOULDER_PIN = 0
ELBOW_PIN = 1
PEN_PIN = 2
SERVO_FREQ_HZ = 50

# Pen servo angles
PEN_UP_ANGLE = 0
PEN_DOWN_ANGLE = 30

# Arm length (both arms are the same), mm
ARM_MM = 155.0

# Servo angles (shoulder, elbow) measured with the pen at 3 corners of
# the drawing area. arm_angles.py works out the paper from these.
HOME_POSE = (20, 30)    # pen at (0, 0), also where the arm parks
X_MAX_POSE = (140, 30)  # pen at the far end of X
Y_MAX_POSE = (90, 85)   # pen at the far end of Y

# elbow servo angle -> bend between the arms: bend = ELBOW_ZERO - elbow
# worked out from the 3 poses above so the X and Y lines come out square
ELBOW_ZERO = 184

LOOP_DELAY_MS = 20
