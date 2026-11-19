"""
test_knob_reader.py - unit tests for knob and button_pressed (issues #25, #26)
Run on a laptop with:  python test_knob_reader.py
"""
from knob_reader import knob, button_pressed
from jig_settings import *


class FakeADC:
    """Stands in for machine.ADC so we can feed knob() a raw value."""
    def __init__(self, raw):
        self.raw = raw

    def read_u16(self):
        return self.raw


class FakePin:
    """Stands in for machine.Pin so we can pretend the switch is pressed."""
    def __init__(self, value):
        self.value_ = value

    def value(self):
        return self.value_


# knob: the two ends of the measured range, and the middle
assert knob(FakeADC(KNOB_MIN)) == 0.0
assert knob(FakeADC(KNOB_MAX)) == 1.0
assert abs(knob(FakeADC((KNOB_MIN + KNOB_MAX) // 2)) - 0.5) < 0.01

# knob: anything outside the measured range is clamped
assert knob(FakeADC(0)) == 0.0
assert knob(FakeADC(65535)) == 1.0

# button: the switch is wired with a pull down, so 1 means held down
assert button_pressed(FakePin(1)) is True
assert button_pressed(FakePin(0)) is False

print("all knob tests passed")
