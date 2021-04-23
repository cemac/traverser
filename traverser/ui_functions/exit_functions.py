# -*- coding: utf-8 -*-
"""
Exit functions
"""

# Package imports:
from traverser.ui_functions.vixim_functions import await_run

def program_exit(ui):
    """
    Exit the program
    """
    # Set exiting flag to true:
    ui.exiting = 1
    # If connected:
    if ui.status['connected'] == 1:
        # Try to stop and switch off the drives:
        cmd_status, err_msg = await_run(ui, 'stop')
        ui.log_message(err_msg, cmd_status)
        # Try to disconnect:
        cmd_status, err_msg = await_run(ui, 'disconnect')
        ui.log_message(err_msg, cmd_status)
        # Try to stop threads:
        try:
            for key, value in ui.threads:
                stop_thread.stop_thread.emit(key)
        except:
            pass
    # Exit the program:
    ui.closeEvent(True)
