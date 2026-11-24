""" Owner: Klara Kerekes
    knob_reader.py - reads the two knobs and the pen button.
"""

from machine import PWM, Pin,  ADC
import time
from main import set_pen #the movement of the pen depending on what it already set to
#import jig_settings
from jig_settings import PEN_DOWN_ANGLE, PEN_UP_ANGLE, PEN_PIN, KNOB_MAX, KNOB_MIN
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