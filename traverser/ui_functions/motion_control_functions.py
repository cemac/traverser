# -*- coding: utf-8 -*-
"""
Motion control functions
"""

# Standard lib imports:
import time
# Package imports:
from traverser.ui_functions.vixim_functions import await_run

def start_it(start_thread, ui):
    """
    Run start up sequence
    """
    # If not connected:
    if ui.status['connected'] != 1:
        # Give up / return:
        err_msg = 'Not connected'
        ui.log_message(err_msg, False)
        return
    # Get other motion buttons which can't be active at the same time:
    button_control_yminus = ui.ui_buttons['control_yminus']
    button_control_yplus = ui.ui_buttons['control_yplus']
    button_control_xminus = ui.ui_buttons['control_xminus']
    button_control_xplus = ui.ui_buttons['control_xplus']
    button_control_gh = ui.ui_buttons['control_gh']
    button_vel = ui.ui_buttons['vel']
    button_accel = ui.ui_buttons['accel']
    button_decel = ui.ui_buttons['decel']
    motion_buttons = [button_control_yminus, button_control_yplus,
                      button_control_xminus, button_control_xplus,
                      button_control_gh, button_vel, button_accel,
                      button_decel]
    # Make sure no other motion buttons are enabled:
    for motion_button in motion_buttons:
        motion_button.setChecked(False)
        motion_button.setEnabled(False)
    # Get start button and check:
    button_start = ui.ui_buttons['start']
    button_start.setChecked(True)
    button_start.setEnabled(False)
    # Send the start message:
    start_thread.has_lock = True
    cmd_status, err_msg = await_run(ui, 'stop')
    cmd_status, err_msg = await_run(ui, 'start')
    start_thread.has_lock = False
    ui.log_message(err_msg, cmd_status)
    # Un check start button:
    button_start.setEnabled(True)
    button_start.setChecked(False)
    # Re-enable motion buttons:
    for motion_button in motion_buttons:
        motion_button.setEnabled(True)

def toggle_yplus(ui):
    """
    Toggle yplus movement
    """
    # Get the button:
    button_control_yplus = ui.ui_buttons['control_yplus']
    # Get the y axis motor id:
    y_motor = ui.config.values['y_motor']
    # Get other motion buttons which can't be active at the same time:
    button_control_yminus = ui.ui_buttons['control_yminus']
    button_control_gh = ui.ui_buttons['control_gh']
    motion_buttons = [button_control_yminus, button_control_gh]
    # If not connected:
    if ui.status['connected'] != 1:
        # Give up / return:
        err_msg = 'Not connected'
        ui.log_message(err_msg, False)
        button_control_yplus.setChecked(False)
        return
    # If button is checked after the current click:
    if button_control_yplus.isChecked():
        # Make sure no other motion buttons are active:
        for motion_button in motion_buttons:
            motion_button.setChecked(False)
        # Send the go message:
        cmd_status, err_msg = await_run(ui, 'drive_stop', [y_motor])
        cmd_status, err_msg = await_run(
            ui, 'drive_go', [y_motor, 'f', ui.vixim.vel, ui.vixim.accel,
            ui.vixim.decel]
        )
        ui.log_message(err_msg, cmd_status)
        # If that failed, give up:
        if not cmd_status:
            button_control_yplus.setChecked(False)
            return
        # Else, check the button:
        button_control_yplus.setChecked(True)
    # Else, not checked:
    else:
        # Stop the drives:
        cmd_status, err_msg = await_run(ui, 'drive_stop', [y_motor])
        ui.log_message(err_msg, cmd_status)
        # If that failed, give up:
        if not cmd_status:
            button_control_yplus.setChecked(True)
            return
        # Else, uncheck the button:
        button_control_yplus.setChecked(False)

def toggle_yminus(ui):
    """
    Toggle yminus movement
    """
    # Get the button:
    button_control_yminus = ui.ui_buttons['control_yminus']
    # Get the y axis motor id:
    y_motor = ui.config.values['y_motor']
    # Get other motion buttons which can't be active at the same time:
    button_control_yplus = ui.ui_buttons['control_yplus']
    button_control_gh = ui.ui_buttons['control_gh']
    motion_buttons = [button_control_yplus, button_control_gh]
    # If not connected:
    if ui.status['connected'] != 1:
        # Give up / return:
        err_msg = 'Not connected'
        ui.log_message(err_msg, False)
        button_control_yminus.setChecked(False)
        return
    # If button is checked after the current click:
    if button_control_yminus.isChecked():
        # Make sure no other motion buttons are active:
        for motion_button in motion_buttons:
            motion_button.setChecked(False)
        # Send the go message:
        cmd_status, err_msg = await_run(ui, 'drive_stop', [y_motor])
        cmd_status, err_msg = await_run(
            ui, 'drive_go', [y_motor, 'b', ui.vixim.vel, ui.vixim.accel,
            ui.vixim.decel]
        )
        ui.log_message(err_msg, cmd_status)
        # If that failed, give up:
        if not cmd_status:
            button_control_yminus.setChecked(False)
            return
        # Else, check the button:
        button_control_yminus.setChecked(True)
    # Else, not checked:
    else:
        # Stop the drives:
        cmd_status, err_msg = await_run(ui, 'drive_stop', [y_motor])
        ui.log_message(err_msg, cmd_status)
        # If that failed, give up:
        if not cmd_status:
            button_control_yminus.setChecked(True)
            return
        # Else, uncheck the button:
        button_control_yminus.setChecked(False)

def toggle_xplus(ui):
    """
    Toggle xplus movement
    """
    # Get the button:
    button_control_xplus = ui.ui_buttons['control_xplus']
    # Get the x axis motor id:
    x_motor = ui.config.values['x_motor']
    # Get other motion buttons which can't be active at the same time:
    button_control_xminus = ui.ui_buttons['control_xminus']
    button_control_gh = ui.ui_buttons['control_gh']
    motion_buttons = [button_control_xminus, button_control_gh]
    # If not connected:
    if ui.status['connected'] != 1:
        # Give up / return:
        err_msg = 'Not connected'
        ui.log_message(err_msg, False)
        button_control_xplus.setChecked(False)
        return
    # If button is checked after the current click:
    if button_control_xplus.isChecked():
        # Make sure no other motion buttons are active:
        for motion_button in motion_buttons:
            motion_button.setChecked(False)
        # Send the go message:
        cmd_status, err_msg = await_run(ui, 'drive_stop', [x_motor])
        cmd_status, err_msg = await_run(
            ui, 'drive_go', [x_motor, 'f', ui.vixim.vel, ui.vixim.accel,
            ui.vixim.decel]
        )
        ui.log_message(err_msg, cmd_status)
        # If that failed, give up:
        if not cmd_status:
            button_control_xplus.setChecked(False)
            return
        # Else, check the button:
        button_control_xplus.setChecked(True)
    # Else, not checked:
    else:
        # Stop the drives:
        cmd_status, err_msg = await_run(ui, 'drive_stop', [x_motor])
        ui.log_message(err_msg, cmd_status)
        # If that failed, give up:
        if not cmd_status:
            button_control_xplus.setChecked(True)
            return
        # Else, uncheck the button:
        button_control_xplus.setChecked(False)

def toggle_xminus(ui):
    """
    Toggle xminus movement
    """
    # Get the button:
    button_control_xminus = ui.ui_buttons['control_xminus']
    # Get the x axis motor id:
    x_motor = ui.config.values['x_motor']
    # Get other motion buttons which can't be active at the same time:
    button_control_xplus = ui.ui_buttons['control_xplus']
    button_control_gh = ui.ui_buttons['control_gh']
    motion_buttons = [button_control_xplus, button_control_gh]
    # If not connected:
    if ui.status['connected'] != 1:
        # Give up / return:
        err_msg = 'Not connected'
        ui.log_message(err_msg, False)
        button_control_xminus.setChecked(False)
        return
    # If button is checked after the current click:
    if button_control_xminus.isChecked():
        # Make sure no other motion buttons are active:
        for motion_button in motion_buttons:
            motion_button.setChecked(False)
        # Send the go message:
        cmd_status, err_msg = await_run(ui, 'drive_stop', [x_motor])
        cmd_status, err_msg = await_run(
            ui, 'drive_go', [x_motor, 'b', ui.vixim.vel, ui.vixim.accel,
            ui.vixim.decel]
        )
        ui.log_message(err_msg, cmd_status)
        # If that failed, give up:
        if not cmd_status:
            button_control_xminus.setChecked(False)
            return
        # Else, check the button:
        button_control_xminus.setChecked(True)
    # Else, not checked:
    else:
        # Stop the drives:
        cmd_status, err_msg = await_run(ui, 'drive_stop', [x_motor])
        ui.log_message(err_msg, cmd_status)
        # If that failed, give up:
        if not cmd_status:
            button_control_xminus.setChecked(True)
            return
        # Else, uncheck the button:
        button_control_xminus.setChecked(False)

def toggle_gh(ui):
    """
    Toggle go home movement
    """
    # Get the go home button:
    button_control_gh = ui.ui_buttons['control_gh']
    # Get other motion buttons:
    button_control_yplus = ui.ui_buttons['control_yplus']
    button_control_yminus = ui.ui_buttons['control_yminus']
    button_control_xplus = ui.ui_buttons['control_xplus']
    button_control_xminus = ui.ui_buttons['control_xminus']
    motion_buttons = [button_control_yplus, button_control_yminus,
                      button_control_xplus, button_control_xminus]
    # If not connected:
    if ui.status['connected'] != 1:
        # Give up / return:
        err_msg = 'Not connected'
        ui.log_message(err_msg, False)
        button_control_gh.setChecked(False)
        return
    # If go home button is checked after the current click:
    if button_control_gh.isChecked():
        # Make sure no other motion buttons are active:
        for motion_button in motion_buttons:
            motion_button.setChecked(False)
        # Send the go home message:
        cmd_status, err_msg = await_run(ui, 'go_home')
        ui.log_message(err_msg, cmd_status)
        # If that failed, give up:
        if not cmd_status:
            button_control_gh.setChecked(False)
            return
        # Else, uncheck the button:
        button_control_gh.setChecked(True)
    # Else, not checked:
    else:
        # Stop the drives:
        x_motor = ui.config.values['x_motor']
        y_motor = ui.config.values['y_motor']
        for i in [x_motor, y_motor]:
            cmd_status, err_msg = await_run(ui, 'drive_stop', [i])
            ui.log_message(err_msg, cmd_status)
            # If that failed, give up:
            if not cmd_status:
                button_control_gh.setChecked(True)
                return
            # Else, uncheck the button:
            button_control_gh.setChecked(False)

def stop_it(stop_thread, ui):
    """
    Stop the motors
    """
    # Stop the starting thread ... :
    start_thread = ui.ui_threads['start']
    start_thread.stop_it()
    start_thread.release_lock.emit()
    stop_thread.stop_thread.emit('start', True)
    # Stop the program thread ... :
    prog_run_thread = ui.ui_threads['prog_run']
    prog_run_thread.stop_it()
    prog_run_thread.release_lock.emit()
    stop_thread.stop_thread.emit('prog_run', True)
    ui.program['running'] = False
    # Get other motion buttons:
    button_start = ui.ui_buttons['start']
    button_control_yplus = ui.ui_buttons['control_yplus']
    button_control_yminus = ui.ui_buttons['control_yminus']
    button_control_xplus = ui.ui_buttons['control_xplus']
    button_control_xminus = ui.ui_buttons['control_xminus']
    button_control_gh = ui.ui_buttons['control_gh']
    button_vel = ui.ui_buttons['vel']
    button_accel = ui.ui_buttons['accel']
    button_decel = ui.ui_buttons['decel']
    button_prog_config = ui.ui_buttons['prog_config']
    button_prog_run = ui.ui_buttons['prog_run']
    motion_buttons = [button_start,
                      button_control_yplus, button_control_yminus,
                      button_control_xplus, button_control_xminus,
                      button_control_gh, button_vel, button_accel,
                      button_decel, button_prog_config]
    # Make sure no other motion buttons are active:
    for motion_button in motion_buttons:
        motion_button.setChecked(False)
        motion_button.setEnabled(False)
    button_prog_run.setChecked(False)
    button_prog_run.setEnabled(False)
    # Send the stop message:
    stop_done = False
    while stop_done is False:
        try:
            cmd_status, err_msg = await_run(ui, 'stop')
            stop_done = True
        except:
            time.sleep(0.1)
    # Log the message:
    ui.log_message(err_msg, cmd_status)
    # Restart the starting thread ... :
    stop_thread.start_thread.emit('start')
    # And the program running thread:
    stop_thread.start_thread.emit('prog_run')
    # If connected:
    if ui.status['connected'] == 1:
        # Re-enable motion buttons:
        for motion_button in motion_buttons:
            motion_button.setEnabled(True)
        # If program is set, re enable run button:
        # If no program exists, make one up:
        if ui.program['x'] is not None and ui.program['y'] is not None:
            button_prog_run.setEnabled(True)
