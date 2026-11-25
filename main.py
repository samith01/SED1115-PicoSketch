"""
main.py - runs on Pico start-up. Reads the knobs and button, moves the
arm and pen, forever.
Owner: Samith Fernando
"""
from machine import Pin, PWM, ADC
import time
from jig_settings import *
from knob_reader import knob
from arm_angles import servo_angles

# translate() is the safe servo function given to us by the instructor
# (servo_translator.py, SED1115 lab files). Angle -> duty_u16, clamped 0..180.
from servo_translator import translate


wristPostionButton = Pin(12, Pin.IN, Pin.PULL_DOWN) #button that is to be prssed for the action of lighting up LED

homePostionButton = Pin(22, Pin.IN, Pin.PULL_DOWN) #button that is to be prssed for the action of lighting up LED

penIsDown = False #state when program starts. Also, when button is not pressed


def button_pressed(button):
    global penIsDown
    if wristPostionButton.value() and penIsDown == False : #Lowering Servo angle arm #empty means zerio, 0, which is true
        penIsDown = True
                 
        while wristPostionButton.value(): #blank brackets mean value of 0 (False), occurs when button is released
            pass # don't want anything else to happen so tell program to move on
            
    if wristPostionButton.value() and penIsDown == True : #when swtich value is 0 (false) and state value are True angle of Servo arm will raise
        penIsDown = False #opposite of pre
        
        while wristPostionButton.value(): #value of 0 (False), occurs when button is released
            pass # nothing else required
    
    pass #allows to exit from this section & move onto next part of code



def move_arm(servos, shoulder, elbow):
    """
    Owner: Samith Fernando
    Inputs:  servos (dict of PWM); shoulder, elbow (float) - degrees.
    Outputs: None.
    Operation: sends both angles through translate() to the arm servos.
    """
    servos["shoulder"].duty_u16(translate(shoulder))
    servos["elbow"].duty_u16(translate(elbow))


def set_pen(servos, pen_down):
    """
    Owner: Samith Fernando
    Inputs:  servos (dict of PWM); pen_down (bool).
    Outputs: None.
    Operation: moves the pen servo to PEN_DOWN_ANGLE or PEN_UP_ANGLE.
    """
    if pen_down:
        servos["pen"].duty_u16(translate(PEN_DOWN_ANGLE))
    else:
        servos["pen"].duty_u16(translate(PEN_UP_ANGLE))


def park_arm(servos):
    """
    Owner: Samith Fernando
    Inputs:  servos (dict of PWM).
    Outputs: None.
    Operation: lifts the pen, moves the arm to HOME_POSE and turns PWM off.
    """
    set_pen(servos, False)
    move_arm(servos, HOME_POSE[0], HOME_POSE[1])
    time.sleep(0.5)  # give the servos time to get there before turning off
    for name in servos:
        servos[name].deinit()


def main():
    """
    Owner: Samith Fernando
    Inputs:  none.  Outputs: none.
    Operation: sets up the pins, then loops: knobs -> servo_angles ->
               move_arm, and toggles the pen on each button press.
               Always parks the arm when the program stops.
    """

    x_pot = ADC(X_POT_PIN)
    y_pot = ADC(Y_POT_PIN)
    button = Pin(PEN_SWITCH_PIN, Pin.IN, Pin.PULL_DOWN)

    servos = {}
    servos["shoulder"] = PWM(Pin(SHOULDER_PIN))
    servos["elbow"] = PWM(Pin(ELBOW_PIN))
    servos["pen"] = PWM(Pin(PEN_PIN))

    for name in servos:
        servos[name].freq(SERVO_FREQ_HZ)

    try:
        while True:
            s, e = servo_angles(knob(x_pot,"x"), knob(y_pot,"y"))
            move_arm(servos, s, e)

            # toggle the pen only when the button goes from up to down
            button_pressed(button)
            set_pen(servos, penIsDown)

            time.sleep_ms(LOOP_DELAY_MS)

    finally:
        park_arm(servos)


if __name__ == "__main__":
    main()
