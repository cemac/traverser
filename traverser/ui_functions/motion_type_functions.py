# -*- coding: utf-8 -*-
"""
Motion type functions
"""

# Package imports:
from traverser.ui_functions.dialogue_functions import get_double

def toggle_motion_type(ui):
    """
    Toggle motion type
    """
    # Get motion type area:
    motion_type_area = ui.ui_components['motion_type']
    # Get the type button:
    button_motion_type = ui.ui_buttons['motion_type']
    # Get the distance value and button elements:
    dist_value = motion_type_area.properties['dist_value']
    button_dist = ui.ui_buttons['dist']
    # If currently set to constant:
    if ui.motion_type == 'constant':
        # Update button text and checked status:
        button_motion_type.setText('Distance')
        button_motion_type.setChecked(True)
        # Update ui motion type property:
        ui.motion_type = 'distance'
        # Set the distance value:
        dist_value.setText(
            '{0:.02f} ({1}/{2})'.format(
                ui.motion_dist, ui.config.values['x_units'],
                ui.config.values['y_units']
            )
        )
        # Enable distance button:
        button_dist.setEnabled(True)
    # Else, currently se to distance:
    else:
        # Update button text and checked status:
        button_motion_type.setText('Constant')
        button_motion_type.setChecked(False)
        # Update ui motion type property:
        ui.motion_type = 'constant'
        # Set the distance value:
        dist_value.setText('--')
        # Disable distance button:
        button_dist.setEnabled(False)

def set_distance(ui):
    """
    Set value for distance based movement
    """
    # Get value for distance:
    status, value = get_double(
        ui, 'Set value', 'Distance', ui.motion_dist, 0, 9999999, 2
    )
    # If that succeeded ... :
    if status == True:
        # Update distance value:
        ui.motion_dist = value
        # Get motion type area:
        motion_type_area = ui.ui_components['motion_type']
        # Get the distance value element:
        dist_value = motion_type_area.properties['dist_value']
        # Set the distance value:
        dist_value.setText(
            '{0:.02f} ({1}/{2})'.format(
                ui.motion_dist, ui.config.values['x_units'],
                ui.config.values['y_units']
            )
        )
