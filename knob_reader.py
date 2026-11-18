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


def button_pressed(button):
    """
    Owner: Klara Kerekes
    Inputs:  button (machine.Pin) - pen switch, pull-down.
    Outputs: bool - True while the switch is held down.
    Operation: button.value() == 1 (switch reads 1 when pressed).
    """
    pass
