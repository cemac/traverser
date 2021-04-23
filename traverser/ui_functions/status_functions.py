# -*- coding: utf-8 -*-
"""
Traverser status functions
"""

# Third party imports:
from PyQt5.Qt import QColor
from PyQt5.QtChart import QScatterSeries
# Package imports:
from traverser.ui_functions.vixim_functions import await_run

def motion_stopped(ui):
    """
    Motion appears to have stopped, so make sure motion buttons are not
    checked
    """
    # Get the motion buttons:
    button_control_yplus = ui.ui_buttons['control_yplus']
    button_control_yminus = ui.ui_buttons['control_yminus']
    button_control_xplus = ui.ui_buttons['control_xplus']
    button_control_xminus = ui.ui_buttons['control_xminus']
    button_control_gh = ui.ui_buttons['control_gh']
    motion_buttons = [button_control_yplus, button_control_yminus,
                      button_control_xplus, button_control_xminus,
                      button_control_gh]
    # Make sure no motion buttons are active:
    for motion_button in motion_buttons:
        motion_button.setChecked(False)

def update_status(ui):
    """
    Update status information and elements
    """
    # If not connected, give up:
    if ui.status['connected'] == 0:
        return None, None, False
    # Update x and y position information:
    x_motor = ui.config.values['x_motor']
    y_motor = ui.config.values['y_motor']
    x_pos = ui.vixim.status[x_motor]['pos']
    y_pos = ui.vixim.status[y_motor]['pos']
    # If x and y positions have not changed, try to update status of drives:
    if x_pos == ui.status['x'] and y_pos == ui.status['y']:
        # Update drives statuses:
        cmd_status, err_msg = await_run(ui, 'update_drives_status')
        # Log message if error:
        if not cmd_status:
            ui.log_message(err_msg, cmd_status)
        # Re-check positions:
        x_pos = ui.vixim.status[x_motor]['pos']
        y_pos = ui.vixim.status[y_motor]['pos']
        # If still the same, presume motors have stopped so un-check motion
        # buttons:
        if x_pos == ui.status['x'] and y_pos == ui.status['y']:
            motion_stopped(ui)
    # Update ui status:
    ui.status['x'] = x_pos
    ui.status['y'] = y_pos
    # Update status labels if we have a position:
    if x_pos is not None and y_pos is not None:
        update_status_labels(ui, x_pos, y_pos)
    # Update motion settings:
    update_motion_labels(ui)
    # Return position and status:
    return x_pos, y_pos, True

def plot_program(ui):
    """
    Plot programmed locations for sample taking
    """
    # If not connected, give up:
    if ui.status['connected'] == 0:
        return
    # Get the program information:
    program = ui.program
    # Get status area:
    status_area = ui.ui_components['status_area']
    # Get chart components:
    chart_status = status_area.properties['chart_status']
    x_axis = chart_status.axisX()
    y_axis = chart_status.axisY()
    # Try to get program chart:
    try:
        chart_program = status_area.properties['chart_program']
    except KeyError:
        chart_program = None
    # If there is a chart program, try to remove existing series:
    if chart_program:
        chart_status.removeSeries(chart_program)
    # Create the scatter series for the program:
    prog_series = QScatterSeries()
    prog_series.setMarkerShape(QScatterSeries.MarkerShapeCircle)
    prog_series.setMarkerSize(8)
    prog_series.setColor(QColor(55, 110, 220, 255))
    # If traverse x axis is longer than y axis, rotate the axes:
    max_x = ui.config.values['max_x']
    max_y = ui.config.values['max_y']
    if max_x > max_y:
        rotate_axes = True
    else:
        rotate_axes = False
    # Loop through program points:
    x_vals = program['x']
    y_vals = program['y']
    for index, x_val in enumerate(x_vals):
        y_val = y_vals[index]
        # check for rotated axes and get x and y values:
        if rotate_axes:
            x_pos = 1 - (y_val / ui.config.values['max_y'])
            y_pos = x_val / ui.config.values['max_x']
        else:
            x_pos = x_val / ui.config.values['max_x']
            y_pos = y_val / ui.config.values['max_y']
        prog_series.append(x_pos, y_pos)
    # Add serieses to chart:
    chart_status.addSeries(prog_series)
    # Attach axes:
    prog_series.attachAxis(x_axis)
    prog_series.attachAxis(y_axis)
    # Store series information:
    status_area.properties['chart_program'] = prog_series
    # Reset program updated flag:
    program['updated'] = False

def plot_status(ui):
    """
    Plot traverse status
    """
    # Get status area:
    status_area = ui.ui_components['status_area']
    # Get chart components:
    chart_status = status_area.properties['chart_status']
    x_axis = chart_status.axisX()
    y_axis = chart_status.axisY()
    current_pos_old = status_area.properties['current_pos']
    # If traverse x axis is longer than y axis, rotate the axes:
    max_x = ui.config.values['max_x']
    max_y = ui.config.values['max_y']
    if max_x > max_y:
        rotate_axes = True
    else:
        rotate_axes = False
    # Create the scatter series for current location:
    current_pos = QScatterSeries()
    current_pos.setMarkerShape(QScatterSeries.MarkerShapeCircle)
    current_pos.setMarkerSize(12)
    current_pos.setColor(QColor(55, 220, 110, 255))
    if (ui.status['connected'] and
            ui.status['x'] is not None and
            ui.status['y'] is not None):
        if rotate_axes:
            x_pos = 1 - (ui.status['y'] / ui.config.values['max_y'])
            y_pos = ui.status['x'] / ui.config.values['max_x']
        else:
            x_pos = ui.status['x'] / ui.config.values['max_x']
            y_pos = ui.status['y'] / ui.config.values['max_y']
        current_pos.append(x_pos, y_pos)
    # Remove existing series if there is one:
    if current_pos_old:
        chart_status.removeSeries(current_pos_old)
    # Add serieses to chart:
    chart_status.addSeries(current_pos)
    # Attach axes:
    current_pos.attachAxis(x_axis)
    current_pos.attachAxis(y_axis)
    # Store series information:
    status_area.properties['current_pos'] = current_pos

def value_to_units(ui, value, axis='x'):
    """
    Convert motor position value to units
    """
    # If x axis:
    if axis == 'x':
        ax_max = ui.config.values['max_x']
        ax_dist = ui.config.values['x_dist']
        ax_units = ui.config.values['x_units']
    # Else, y axis:
    else:
        ax_max = ui.config.values['max_y']
        ax_dist = ui.config.values['y_dist']
        ax_units = ui.config.values['y_units']
    # Convert value:
    ax_value = (value / ax_max) * ax_dist
    # Return value and units:
    return ax_value, ax_units

def units_to_value(ui, value, axis='x'):
    """
    Convert motor position units to value
    """
    # If x axis:
    if axis == 'x':
        ax_max = ui.config.values['max_x']
        ax_dist = ui.config.values['x_dist']
    # Else, y axis:
    else:
        ax_max = ui.config.values['max_y']
        ax_dist = ui.config.values['y_dist']
    # Convert value:
    ax_value = (value / ax_dist) * ax_max
    # Values need to be integers:
    ax_value = round(ax_value)
    # Return value:
    return ax_value

def update_status_labels(ui, x_value, y_value):
    """
    Update status information
    """
    # Get status area:
    status_area = ui.ui_components['status_area']
    # Get values of interest:
    x_slabel = status_area.properties['x_svalue']
    y_slabel = status_area.properties['y_svalue']
    x_plabel = status_area.properties['x_pvalue']
    y_plabel = status_area.properties['y_pvalue']
    # Convert values to units:
    x_uvalue, x_units = value_to_units(ui, x_value, 'x')
    y_uvalue, y_units = value_to_units(ui, y_value, 'y')
    # Text values ... size:
    x_svalue = '{:.1f}'.format(ui.config.values['x_dist']).zfill(7)
    x_stext = '{0:08d} : {1} {2}'.format(ui.config.values['max_x'], x_svalue,
                                         x_units)
    y_svalue = '{:.1f}'.format(ui.config.values['y_dist']).zfill(7)
    y_stext = '{0:08d} : {1} {2}'.format(ui.config.values['max_y'], y_svalue,
                                         y_units)
    # Position:
    x_uvalue = '{:.1f}'.format(x_uvalue).zfill(7)
    y_uvalue = '{:.1f}'.format(y_uvalue).zfill(7)
    x_text = '{0:08d} : {1} {2}'.format(x_value, x_uvalue, x_units)
    y_text = '{0:08d} : {1} {2}'.format(y_value, y_uvalue, y_units)
    # Set the text values:
    x_slabel.setText(x_stext)
    y_slabel.setText(y_stext)
    x_plabel.setText(x_text)
    y_plabel.setText(y_text)

def update_motion_labels(ui):
    """
    Update motion settings information
    """
    # Get motion setting area:
    motion_settings_area = ui.ui_components['motion_settings']
    # Check velocity value and update if available:
    vel_value = ui.vixim.vel
    if vel_value:
        vel_text = '{:.2f}'.format(vel_value).zfill(6)
        vel_label = motion_settings_area.properties['vel_value']
        vel_label.setText(vel_text)
    # Check acceleration value and update if available:
    accel_value = ui.vixim.accel
    if accel_value:
        accel_text = '{:.2f}'.format(ui.vixim.accel).zfill(6)
        accel_label = motion_settings_area.properties['accel_value']
        accel_label.setText(accel_text)
    # Check deceleration value and update if available:
    decel_value = ui.vixim.accel
    if decel_value:
        decel_text = '{:.2f}'.format(ui.vixim.decel).zfill(6)
        decel_label = motion_settings_area.properties['decel_value']
        decel_label.setText(decel_text)
