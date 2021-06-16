# -*- coding: utf-8 -*-
"""
Program functions
"""

# Standard lib imports:
import datetime
import os
import time
# Package imports:
from traverser.functions import convert_numeric
from traverser.ui_functions.status_functions import (
    units_to_value, value_to_units
)
from traverser.ui_functions.vixim_functions import await_run

def load_program(ui, program_file):
    """
    Load program from file
    """
    # Red the program from file:
    try:
        with open(program_file, 'r') as prog_fh:
            prog_lines = prog_fh.readlines()
    except:
        err_msg = 'Failed to read program from file {0}'.format(program_file)
        return False, err_msg
    # Loop through lines reading values:
    x_vals = []
    y_vals = []
    for prog_line in prog_lines:
        line_vals = prog_line.split(',')
        # 2 values expected:
        if len(line_vals) != 2:
            continue
        # Get x and y values and convert to numeric:
        try:
            x_val = units_to_value(ui, convert_numeric(line_vals[0]), 'x')
            y_val = units_to_value(ui, convert_numeric(line_vals[1]), 'y')
        except:
            continue
        # If we get here, values should be valid:
        x_vals.append(x_val)
        y_vals.append(y_val)
    # Update the program:
    ui.program['x'] = x_vals
    ui.program['y'] = y_vals
    ui.program['updated'] = True
    # Return:
    return True, None

def set_program(ui, min_x, max_x, min_y, max_y, x_inc, y_inc,
                pre_delay=0.5, post_delay=0.5, order='xy'):
    """
    Create a default program
    """
    # Get max x and y values (in units):
    x_dist = max_x
    y_dist = max_y
    # Lists for storing x and y values in units:
    x_uvals = []
    y_uvals = []
    # Init x and y value at 0:
    x_uval = min_x
    y_uval = min_y
    # Loop over values in bounds:
    while x_uval <= x_dist:
        x_uvals.append(x_uval)
        x_uval += x_inc
    while y_uval <= y_dist:
        y_uvals.append(y_uval)
        y_uval += y_inc
    # Create x / y program coordinates:
    x_vals = []
    y_vals = []
    # If order is xy:
    if order == 'xy':
        # 0 is increasing x, 1 is decreasing x:
        x_order = 0
        for my_y_uval in y_uvals:
            if x_order == 0:
                my_x_uvals = x_uvals
            else:
                my_x_uvals = x_uvals[::-1]
            for my_x_uval in my_x_uvals:
                my_x = units_to_value(ui, my_x_uval, 'x')
                my_y = units_to_value(ui, my_y_uval, 'y')
                x_vals.append(my_x)
                y_vals.append(my_y)
            # Reverse order for next row:
            if x_order == 0:
                x_order = 1
            else:
                x_order = 0
    # Else order is yx:
    else:
        # 0 is increasing y, 1 is decreasing y:
        y_order = 0
        for my_x_uval in x_uvals:
            if y_order == 0:
                my_y_uvals = y_uvals
            else:
                my_y_uvals = y_uvals[::-1]
            for my_y_uval in my_y_uvals:
                my_x = units_to_value(ui, my_x_uval, 'x')
                my_y = units_to_value(ui, my_y_uval, 'y')
                x_vals.append(my_x)
                y_vals.append(my_y)
            # Reverse order for next row:
            if y_order == 0:
                y_order = 1
            else:
                y_order = 0
    # Update the program:
    ui.program['x'] = x_vals
    ui.program['y'] = y_vals
    ui.program['min_x'] = min_x
    ui.program['max_x'] = max_x
    ui.program['x_inc'] = x_inc
    ui.program['min_y'] = min_y
    ui.program['max_y'] = max_y
    ui.program['y_inc'] = y_inc
    ui.program['order'] = order
    ui.program['pre_delay'] = pre_delay
    ui.program['post_delay'] = post_delay
    ui.program['updated'] = True

def init_program(ui):
    """
    Create a default program
    """
    # Get max x and y values (in units):
    x_dist = ui.config.values['x_dist']
    y_dist = ui.config.values['y_dist']
    # Calculate some increments in units:
    x_inc = x_dist // 10
    y_inc = y_dist // 10
    # Set the program:
    set_program(ui, 0, x_dist, 0, y_dist, x_inc, y_inc)

def run_it(program_thread, ui):
    """
    Run the program
    """
    # Close program config window:
    ui.program_window.close()
    # Get the run button:
    button_prog_run = ui.ui_buttons['prog_run']
    button_prog_run.setChecked(True)
    button_prog_run.setEnabled(False)
    # Init o.k. to run flag as True:
    ready_status = True
    # Get the output file:
    ui._set_log_file.emit()
    log_file = None
    while log_file is None:
        log_file = ui.program['log_file']
        time.sleep(0.1)
    # Try open log file for writing:
    try:
        log_fh = open(log_file, 'w')
        log_fh.close()
    except:
        log_file = False
        err_msg = 'Failed to open output file for writing'
        ui.log_message(err_msg, False)
    # Reset log file:
    ui.program['log_file'] = None
    # If no log file, give up:
    if log_file is False:
        ui._display_alert.emit('No log file set')
        ui.program['log_file'] = None
        ready_status = False
    # Check an instrument is connected:
    if ui.instrument is None:
        ui._display_alert.emit('No instrument connected')
        ready_status = False
    elif ui.instrument.connected is False:
        ui._display_alert.emit('Instrument not connected')
        ready_status = False
    # If not ready to run, give up:
    if ready_status is False:
        button_prog_run.setEnabled(True)
        button_prog_run.setChecked(False)
        return
    # Log starting message:
    ui.log_message('Program started', True)
    # Get other buttons which can't be active at the same time:
    button_control_yminus = ui.ui_buttons['control_yminus']
    button_control_yplus = ui.ui_buttons['control_yplus']
    button_control_xminus = ui.ui_buttons['control_xminus']
    button_control_xplus = ui.ui_buttons['control_xplus']
    button_control_gh = ui.ui_buttons['control_gh']
    button_vel = ui.ui_buttons['vel']
    button_accel = ui.ui_buttons['accel']
    button_decel = ui.ui_buttons['decel']
    button_prog_config = ui.ui_buttons['prog_config']
    button_start = ui.ui_buttons['start']
    motion_buttons = [button_control_yminus, button_control_yplus,
                      button_control_xminus, button_control_xplus,
                      button_control_gh, button_vel, button_accel,
                      button_decel, button_prog_config, button_start]
    # Make sure no other motion buttons are enabled:
    for motion_button in motion_buttons:
        motion_button.setChecked(False)
        motion_button.setEnabled(False)
    # Send the stop message:
    program_thread.has_lock = True
    cmd_status, err_msg = await_run(ui, 'stop')
    program_thread.has_lock = False
    # Set program running status:
    ui.program['running'] = True
    # Loop through program coordinates:
    x_motor = ui.config.values['x_motor']
    y_motor = ui.config.values['y_motor']
    x_vals = ui.program['x']
    y_vals = ui.program['y']
    pre_delay = ui.program['pre_delay']
    post_delay = ui.program['post_delay']
    for index, x_val in enumerate(x_vals):
        y_val = y_vals[index]
        # If not connected:
        if ui.status['connected'] != 1:
            # Give up / return:
            err_msg = 'Not connected'
            ui.log_message(err_msg, False)
            # Make sure no other motion buttons are enabled:
            for motion_button in motion_buttons:
                motion_button.setChecked(False)
                motion_button.setEnabled(False)
            return
        # Send motors to this location ... x first:
        program_thread.has_lock = True
        cmd_status, err_msg = await_run(ui, 'drive_goto',
            [x_motor, x_val, ui.vixim.vel, ui.vixim.accel, ui.vixim.decel]
        )
        program_thread.has_lock = False
        # Check for errors:
        if not cmd_status:
            ui.log_message(err_msg, cmd_status)
            break
        # Move y:
        program_thread.has_lock = True
        cmd_status, err_msg = await_run(ui, 'drive_goto',
            [y_motor, y_val, ui.vixim.vel, ui.vixim.accel, ui.vixim.decel]
        )
        program_thread.has_lock = False
        # Check for errors:
        if not cmd_status:
            ui.log_message(err_msg, cmd_status)
            break
        # Pre delay:
        time.sleep(pre_delay)
        # Obtain values from instrument:
        ui.instrument_values = ui.instrument.acquire()
        instrument_values = ui.instrument_values
        # Open the log file for appending:
        log_fh = open(log_file, 'a')
        # Log values ... if the log file is empty:
        if os.path.getsize(log_file) == 0:
            # Add header:
            hdr_line = 'date'
            # X and Y:
            if ui.config.values['x_units'] == '':
                hdr_line += ',x'
            else:
                hdr_line += ',x ({0})'.format(ui.config.values['x_units'])
            if ui.config.values['y_units'] == '':
                hdr_line += ',y'
            else:
                hdr_line += ',y ({0})'.format(ui.config.values['y_units'])
            # Add instrument ids:
            # Add instrument ids:
            for ix, inst_id in enumerate(instrument_values['ids']):
                inst_units = instrument_values['units'][ix]
                if inst_units:
                    inst_id = '{0} ({1})'.format(inst_id, inst_units)
                else:
                    inst_id = '{0}'.format(inst_id)
                hdr_line += ',{0}'.format(inst_id)
            # Write the header:
            log_fh.write('{0}\n'.format(hdr_line))
        # Get date, x and y:
        log_dt = datetime.datetime.now()
        log_date = log_dt.strftime('%Y-%m-%d %H:%M:%S')
        log_x = value_to_units(ui, x_val, 'x')[0]
        log_y = value_to_units(ui, y_val, 'y')[0]
        # Create the line for the log:
        log_line = '{0},{1},{2}'.format(log_date, log_x, log_y)
        # Add values from instrument:
        for inst_val in instrument_values['values']:
            log_line += ',{0}'.format(inst_val)
        # Write the line:
        log_fh.write('{0}\n'.format(log_line))
        # Close the log file:
        log_fh.close()
        # Post delay:
        time.sleep(post_delay)
    # Set program running status:
    ui.program['running'] = False
    # Re-enable motion buttons:
    for motion_button in motion_buttons:
        motion_button.setEnabled(True)
    # Re-enable run button:
    button_prog_run.setEnabled(True)
    button_prog_run.setChecked(False)
    # Log completion message:
    ui.log_message('Program completed', True)
