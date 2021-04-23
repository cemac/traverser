# -*- coding: utf-8 -*-
"""
Traverser exit button area
"""

# Third party imports:
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QPushButton
# Package imports:
from traverser.ui_components.ui_component import UIComponent

class ExitArea(UIComponent):
    """
    Exit button area for traverser UI
    """
    def __init__(self, ui):
        # Run parent init first:
        super().__init__(ui, 3)
        # Run component init:
        self.init(ui)

    def button_exit(self, ui):
        """
        Create the exit button
        """
        # Create the QPushButton:
        button_exit = QPushButton('Exit', self)
        # Return the button:
        return button_exit

    def init(self, ui):
        """
        Main component init
        """
        # Get self grid:
        grid = self.properties['grid']
        # Create the exit button:
        ui.ui_buttons['exit'] = self.button_exit(ui)
        button_exit = ui.ui_buttons['exit']
        grid.addWidget(button_exit, 0, 2, 1, 1)
