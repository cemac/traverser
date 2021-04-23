# -*- coding: utf-8 -*-
"""
UI dialogue functions
"""

# Third party imports:
from PyQt5.QtWidgets import QInputDialog

def get_double(ui, title, label, default, min_val, max_val, decimals=2):
    """
    Dialogue to return a decimal value
    """
    # Get value from input dialogue:
    value, status = QInputDialog.getDouble(ui, title, label, default, min_val,
                                           max_val, decimals)
    # Return value if o.k. is clicked:
    if status:
        return True, value
    # Else return False / none:
    else:
        return False, None
