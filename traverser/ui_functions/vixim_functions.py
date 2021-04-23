# -*- coding: utf-8 -*-
"""
VixIM related functions
"""

def await_run(ui, run_cmd_name, args=None):
    """
    Get lock for serial / VixIM access and run command
    """
    # Acquire the lock:
    ui.vixim_lock.lock()
    # If no arguments, set to empty:
    if args is None:
        args = []
    # Run the command:
    run_cmd = getattr(ui.vixim, run_cmd_name)
    status, err_msg = run_cmd(*args)
    # Release the lock:
    ui.vixim_lock.unlock()
    # Return the result:
    return status, err_msg
