# -*- coding: utf-8 -*-
"""
Instrument functions
"""

# Third party imports:
from PyQt5.QtCore import Qt

def toggle_inst_connect(ui):
    """
    Toggle connection to instrument
    """
    # Get the connect button:
    button_inst_connect = ui.ui_buttons['inst_connect']
    # If connected:
    if ui.instrument.connected is True:
        # Try to disconnect:
        cmd_status, err_msg = ui.instrument.disconnect()
        ui.log_message(err_msg, cmd_status)
        # Give up  if that failed:
        if not cmd_status:
            button_inst_connect.setChecked(True)
            return
        # Update ui connected status:
        ui.instrument.connected = False
        # Update button text and checked status:
        button_inst_connect.setText('Connect')
        button_inst_connect.setChecked(False)
    # Else, not connected, so connect:
    else:
        # Try to connect:
        cmd_status, err_msg = ui.instrument.connect()
        ui.log_message(err_msg, cmd_status)
        # Give up  if that failed:
        if not cmd_status:
            button_inst_connect.setChecked(False)
            return
        # Update ui connected status:
        ui.instrument.connected = True
        # Update button text and checked status:
        button_inst_connect.setText('Disconnect')
        button_inst_connect.setChecked(True)

def update_instrument(ui):
    """
    Update instrument information in the UI
    """
    # If an instrument is not selected, return:
    if ui.instrument is None:
        return
    # If not connected, return:
    if not ui.instrument.connected:
        return
    # Get the instrument area:
    inst_area = ui.ui_components['instrument_area']
    # Acquire a reading if program is not running:
    if ui.program['running'] is False:
        ui.instrument_values = ui.instrument.acquire()
    instrument_values = ui.instrument_values
    # Loop through instrument values:
    inst_area_values = inst_area.values['values']
    for i, i_id in enumerate(instrument_values['ids']):
        # Loop through instrument area values:
        for j, j_id in enumerate(inst_area.values['ids']):
            # If ids match:
            if i_id == j_id:
                # Update value:
                j_value = inst_area_values[j]
                if instrument_values['error'][i] is True:
                    i_text = 'Error'
                    i_style = 'color: #993333;'
                else:
                    i_value = instrument_values['values'][i]
                    i_units = instrument_values['units'][i]
                    i_text = '{0} {1}'.format(i_value, i_units)
                    i_style = 'color: #000000;'
                j_value.setStyleSheet(i_style)
                j_value.setFont(ui.fonts['standard'])
                j_value.setText(i_text)
