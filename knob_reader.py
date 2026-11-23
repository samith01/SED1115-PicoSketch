"""
knob_reader.py - reads the two knobs and the pen button.
Owner: Klara Kerekes
"""
from jig_settings import *


def knob(adc):
    """
    Owner: Klara Kerekes
    Inputs:  adc (machine.ADC) - one knob.
    Outputs: float 0.0 to 1.0 - how far the knob is turned.
    Operation: scales adc.read_u16() from KNOB_MIN..KNOB_MAX to 0..1,
               clamped so it never goes below 0 or above 1.
    """
    pass

def set_pen(servos, angle): #will be called and ran in button_pressed bc to call the desired angle to be moved to 
        #have to translate the angle as an int into a value that the servo will accepts
    servos.duty_u16(translate(angle)) #translate formula
    
def button_pressed(button):
    """
    Owner: Klara Kerekes
    Inputs:  button (machine.Pin) - pen switch, pull-down.
    Outputs: bool - True while the switch is held down.
    Operation: button.value() == 1 (switch reads 1 when pressed).
    """
    global state
    while True:
        if sw3.value() and state == False : #Lowering Servo angle arm #empty means zerio, 0, which is true
            state = True
            
            set_pen(servos, pen_down) #calling function set_pen and running it according to how it's written in main.py
             
            time.sleep(0.5) # time before another button pressed will be registered. Anything before won't be considered
            while sw3.value(): # wait till we release the button, for which the value will be 0, False for that
                pass # button released  
        
       
        if sw3.value() and state == True : #Raising Servo angle arm
            state = False
            
            set_pen(servos, pen_down) #calling function set_pen to set the servo angle to != pen_down, but rather PEN_UP_ANGLE
                #calling function set_pen (from main) to set the servo angle to the degree associated w/PEN_UP_ANGLE (30 degrees)


            time.sleep(0.5) # time before another button press is registered and acted upon
            while sw3.value(): # when button value is 0 (false), when release doesn't do anything 
                pass
            # button released
             

button_pressed(sw3) #calling to run the function above when the condition is met
    #outside of function so that when sw3 is pressed it'll


    
    pass
