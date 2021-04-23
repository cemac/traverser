# -*- coding: utf-8 -*-
"""
Motion settings functions
"""

# Package imports:
from traverser.ui_functions.dialogue_functions import get_double

def set_motion(ui, motion_type):
    """
    Set velocity / acceleration / deceleration value
    """
    # If not connected:
    if ui.status['connected'] != 1:
        # Give up / return:
        err_msg = 'Not connected'
        ui.log_message(err_msg, False)
        return
    # If velocity:
    if motion_type == 'vel':
        # Get a value using get_double dialogue:
        status, value = get_double(
            ui, 'Set value', 'Velocity', ui.vixim.vel, 0, 50, 2
        )
        # If a value has been obtained, update vixim setting:
        if status:
            ui.vixim.vel = value
    # If acceleration:
    if motion_type == 'accel':
        # Get a value using get_double dialogue:
        status, value = get_double(
            ui, 'Set value', 'Acceleration', ui.vixim.accel, 0, 100, 2
        )
        # If a value has been obtained, update vixim setting:
        if status:
            ui.vixim.accel = value
    # If deceleration:
    if motion_type == 'decel':
        # Get a value using get_double dialogue:
        status, value = get_double(
            ui, 'Set value', 'Deceleration', ui.vixim.decel, 0, 100, 2
        )
        # If a value has been obtained, update vixim setting:
        if status:
            ui.vixim.decel = value
