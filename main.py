"""
main.py - entry point. Runs on Pico start-up.
Reads knobs and switch, converts to angles, moves the arm, forever.
Owner: Samith Fernando
"""
import time
from jig_settings import *
from knob_reader import init_knobs, read_target_xy
from pen_button import init_button, debounce_press, toggle_pen
from arm_angles import xy_to_angles
from servo_driver import init_servos, move_arm, set_pen, park_arm


def setup():
    """
    Owner: Samith Fernando
    Inputs:  none (uses constants from jig_settings).
    Outputs: state (dict) - hardware objects, smoothing buffers,
             pen state and debounce state.
    Operation: calls init_knobs, init_button and init_servos, lifts the pen,
               and builds the state dictionary used by update().
    """
    x_adc, y_adc = init_knobs(X_POT_PIN, Y_POT_PIN)
    button = init_button(PEN_SWITCH_PIN)
    servos = init_servos({"shoulder": SHOULDER_PIN,
                          "elbow": ELBOW_PIN,
                          "pen": PEN_PIN}, SERVO_FREQ_HZ)

    # start with the pen up so nothing gets drawn by accident
    set_pen(servos, False)

    state = {
        "x_adc": x_adc,
        "y_adc": y_adc,
        "button": button,
        "servos": servos,
        "x_hist": [],          # recent X readings for smoothing
        "y_hist": [],          # recent Y readings for smoothing
        "pen_down": False,
        "last_button": False,  # last stable button state
        "last_press_ms": 0,    # time of last accepted button change
    }
    return state


def update(state):
    """
    Owner: Samith Fernando
    Inputs:  state (dict) from setup(), modified in place.
    Outputs: None.
    Operation: one loop pass -
               1. debounce_press -> toggle_pen -> set_pen on a new press
               2. read_target_xy -> xy_to_angles
               3. move_arm if the angles are safe, else skip this pass
    """
    # 1. pen button
    now = time.ticks_ms()
    new_press, state["last_button"], state["last_press_ms"] = debounce_press(
        state["button"], state["last_button"], state["last_press_ms"], now)
    if new_press:
        state["pen_down"] = toggle_pen(state["pen_down"])
        set_pen(state["servos"], state["pen_down"])

    # 2. knobs -> target position -> angles
    x, y = read_target_xy(state["x_adc"], state["y_adc"],
                          state["x_hist"], state["y_hist"])
    angles = xy_to_angles(x, y)

    # 3. only move if the angles are safe (xy_to_angles returns None if not)
    if angles is not None:
        move_arm(state["servos"], angles[0], angles[1])


def main():
    """
    Owner: Samith Fernando
    Inputs:  none.  Outputs: none.
    Operation: setup once, then call update() every LOOP_DELAY_MS until
               stopped; always parks the arm on exit (Ctrl-C or error).
    """
    state = setup()
    try:
        while True:
            update(state)
            time.sleep_ms(LOOP_DELAY_MS)
    finally:
        park_arm(state["servos"])


if __name__ == "__main__":
    main()
