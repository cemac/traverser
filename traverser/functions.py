# -*- coding: utf-8 -*-
"""
functions

traverser functions
"""

def convert_numeric(value_in):
    """
    Try to convert a string value to an integer or float, or return
    original value
    """
    # Try int first:
    try:
        value_out = int(value_in)
    except ValueError:
        # Try float:
        try:
            value_out = float(value_in)
        # Otherwise use original value:
        except ValueError:
            value_out = value_in
    # Return value:
    return value_out
