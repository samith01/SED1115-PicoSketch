""" Owner: Klara Kerekes
    knob_reader.py - reads the two knobs and the pen button.
"""

from machine import Pin, PWM, ADC
import time
from main import set_pen #the movement of the pen depending on what it already set to
#import jig_settings
from jig_settings import PEN_DOWN_ANGLE, PEN_UP_ANGLE, PEN_PIN, KNOB_MAX, KNOB_MIN
from main import set_pen #the movement of the pen depending on what it already set to
from servo_translator import translate #for translating the servo angle into PWM value servo will accepted


#Mapping degreee of rotation of knobs (GP 26 & 27) controlling movement in x & y directions,respectively, into range 
""" Owner: Klara Kerekes
    Inputs:  adc (machine.ADC) - one knob.
    Outputs: float 0.0 to 1.0 - how far the knob is turned.
    Operation: scales adc.read_u16() from KNOB_MIN..KNOB_MAX to 0..1,
               clamped so it never goes below 0 or above 1.
"""

#knob Pin's that corresponds to the control of movement in x & y direction for shoulder and elbow servos, respectively
x_knob = ADC(Pin(26)) 
y_knob = ADC(Pin(27)) 


#Maps the ADC values into the desired range of 0.0 to 1.0 (floats) and clamps & restricts anything outside of it
#works in tandom with knob() function
def map_adc_clamped(value, in_min, in_max, out_min, out_max):
    mapped = (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min #how the mapped values in range are determined
    low, high = min(out_min, out_max), max(out_min, out_max) #to determine if mapped values are outside of range
    return max(low, min(high, mapped)) #returns within the acceptable range

#have to do reading and mapping for each knob pin
def knob():
    #read ADC values directly from the knob Pin's
    x_raw_knob_value = x_knob.read_u16() 
    y_raw_knob_value = y_knob.read_u16()
    
    #maps and clamps those raw values into the range
    x_values_mapped = map_adc_clamped(x_raw_knob_value, 320, 65535, 0.0, 1.0)
    y_values_mapped = map_adc_clamped(y_raw_knob_value, 320, 65535, 0.0, 1.0)

    print(f"x knob values(GP26): {x_values_mapped}			|knob values (GP27): {y_values_mapped}") #prints out mapped values the range as they change


#Changing the wrist servo angle every time a button (GP12) is pressed to opposite of current position
""" Owner: Klara Kerekes
    Inputs:  button (machine.Pin) - pen switch, pull-down.
    Outputs: bool - True while the switch is held down.
    Operation: button.value() == 1 (switch reads 1 when pressed).
 """

pen_down = PEN_DOWN_ANGLE
pen_up = PEN_UP_ANGLE

state = False #state when program starts. Also, when button is not pressed

sw3 = Pin(12, Pin.IN, Pin.PULL_DOWN) #button that is to be prssed for the action of lighting up LED
      
servos = PWM(Pin(PEN_PIN)) #Pin in GP2 on accessory board. Already defined in jig_settings, so imported
servos.freq(50)


#translating from int desire angle degree to PWM so servo can move to position  
def set_pen(servo, angle): 
    servo.duty_u16(translate(angle)) #takes angle values translates to a duty_u16 value (servos understand) & send to it    

def button_pressed(button):
    global state
    if sw3.value() and state == False : #Lowering Servo angle arm #empty means zerio, 0, which is true
        state = True
        
        set_pen(servos, PEN_DOWN_ANGLE)  #calling function set_pen to set servo to angle down, 30 degress
         
        while sw3.value(): #blank brackets mean value of 0 (False), occurs when button is released
            pass # don't want anything else to happen so tell program to move on
            
    if sw3.value() and state == True : #when swtich value is 0 (false) and state value are True angle of Servo arm will raise
        state = False #opposite of pre
        
        set_pen(servos, PEN_UP_ANGLE) #calling function set_pen to set servo to angle up, 0 degress

        while sw3.value(): #value of 0 (False), occurs when button is released
            pass # nothing else required
            
    pass #allows tot exit from this section & move onto next part of code


# while True:
#     knob()
#     button_pressed(sw3) #calling to run the function above when the condition is met
#     time.sleep(0.5)
        
