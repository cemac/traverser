# -*- coding: utf-8 -*-
"""
Traverser UI component class
"""

# Third party imports:
from PyQt5.QtWidgets import QFrame, QGridLayout, QWidget

class UIComponent(QFrame):
    """
    Traverser UI component

    extends QFrame class
    """
    def __init__(self, ui, n_cols, main_frame=False, show_frame=True):
        # Run parent init first:
        super().__init__()
        # Class properties:
        self.properties = {
            'main_frame': main_frame,
            'frame': None,
            'grid': None,
            'n_cols': n_cols,
            'col_width': None
        }
        # Get the UI grid spacing:
        grid_spacing = ui.window_properties['grid_spacing']
        # Create a QFrame for the area:
        self.properties['frame'] = self
        frame = self.properties['frame']
        # Visible frame?:
        if show_frame:
            frame.setFrameShape(QFrame.StyledPanel)
            frame.setFrameShadow(QFrame.Raised)
        # Create a grid layout:
        self.properties['grid'] = QGridLayout(frame)
        grid = self.properties['grid']
        # Set the grid spacing:
        grid.setSpacing(grid_spacing)
        # If this is the main frame:
        if main_frame:
            # Get width from main ui window:
            parent_width = ui.window_properties['width']
        else:
            # Get width from main frame:
            ui_main_frame = ui.ui_components['main_frame']
            parent_width = ui_main_frame.properties['col_width']
        # Calculate a column width:
        self.properties['col_width'] = ((parent_width -
                                         ((n_cols + 1) * grid_spacing)) /
                                        n_cols)
        col_width = self.properties['col_width']
        # Set the column widths:
        for i in range(n_cols):
            grid.setColumnMinimumWidth(i, col_width)
