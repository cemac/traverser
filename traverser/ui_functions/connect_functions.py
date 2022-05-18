# -*- coding: utf-8 -*-
"""
Connect / disconnect functions
"""

# Package imports:
from traverser.ui_functions.vixim_functions import await_run

def toggle_connect_buttons(ui):
    """
    Enable / disable buttons on connect / disconnect
    """
    # Define buttons to be enabled / disabled:
    connect_buttons = ['configure', 'start', 'prog_config',
                       'control_yplus', 'control_yminus', 'control_xplus',
                       'control_xminus', 'control_gh',
                       'motion_type',
                       'vel', 'accel', 'decel']
    # Loop through buttons:
    for connect_button in connect_buttons:
        this_button = ui.ui_buttons[connect_button]
        # If button is enabled:
        if this_button.isEnabled():
            # Un-check:
            this_button.setChecked(False)
            # Disable button:
            this_button.setDisabled(True)
        else:
            # Enable button:
            this_button.setEnabled(True)

def toggle_connect(ui):
    """
    Toggle connection to motor controller
    """
    # Get the connect button:
    button_connect = ui.ui_buttons['connect']
    # If connected:
    if ui.status['connected'] == 1:
        # Disable buttons which should be disabled on disconnect:
        toggle_connect_buttons(ui)
        # Try to stop:
        cmd_status, err_msg = await_run(ui, 'stop')
        ui.log_message(err_msg, cmd_status)
        # Give up  if that failed:
        if not cmd_status:
            button_connect.setChecked(True)
            toggle_connect_buttons(ui)
            return
        # Try to disconnect:
        cmd_status, err_msg = await_run(ui, 'disconnect')
        ui.log_message(err_msg, cmd_status)
        # Give up if that failed:
        if not cmd_status:
            button_connect.setChecked(True)
            toggle_connect_buttons(ui)
            return
        # Disable program run button:
        button_prog_run = ui.ui_buttons['prog_run']
        button_prog_run.setChecked(False)
        button_prog_run.setEnabled(False)
        # Update ui connected status:
        ui.status['connected'] = 0
        # Update button text and checked status:
        button_connect.setText('Connect')
        button_connect.setChecked(False)
    # Else, not connected, so connect:
    else:
        # Make sure config window is closed:
        ui.config_window.close()
        # Try to connect:
        cmd_status, err_msg = await_run(ui, 'connect')
        ui.log_message(err_msg, cmd_status)
        # Give up  if that failed:
        if not cmd_status:
            button_connect.setChecked(False)
            return
        # Update ui connected status:
        ui.status['connected'] = 1
        # Update drives statuses:
        cmd_status, err_msg = await_run(ui, 'update_drives_status')
        # Log message if error:
        if not cmd_status:
            ui.log_message(err_msg, cmd_status)
        # Update button text and checked status:
        button_connect.setText('Disconnect')
        button_connect.setChecked(True)
        # Enable buttons which should be enabled on connect:
        toggle_connect_buttons(ui)
        # Enable program run button. Possibly:
        if ui.program['x'] is not None and ui.program['y'] is not None:
            button_prog_run = ui.ui_buttons['prog_run']
            button_prog_run.setChecked(False)
            button_prog_run.setEnabled(True)
