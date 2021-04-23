# -*- coding: utf-8 -*-
"""
Traverser program control area
"""

# Third party imports:
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QPushButton
# Package imports:
from traverser.ui_components.ui_component import UIComponent

class ProgramControl(UIComponent):
    """
    Program control area for traverser UI
    """
    def __init__(self, ui):
        # Run parent init first:
        super().__init__(ui, 3)
        # Run component init:
        self.init(ui)

    def button_prog(self, label, checkable=False, enabled=True):
        """
        Create a button
        """
        # Create the QPushButton:
        button_connect = QPushButton(label, self)
        button_connect.setCheckable(checkable)
        button_connect.setEnabled(enabled)
        # Return the button:
        return button_connect

    def init(self, ui):
        """
        Main component init
        """
        # Get self grid:
        grid = self.properties['grid']
        # Create a label for the area:
        self.properties['label'] = QLabel('Program Control', self)
        label = self.properties['label']
        label.setTextFormat(Qt.PlainText)
        label.setFont(ui.fonts['bold'])
        grid.addWidget(label, 0, 0, 1, 1)
        # Create the program config buttion:
        ui.ui_buttons['prog_config'] = self.button_prog('Configure', False,
                                                        False)
        button_prog_config = ui.ui_buttons['prog_config']
        grid.addWidget(button_prog_config, 1, 0, 1, 1)
        # Create the start button:
        ui.ui_buttons['prog_run'] = self.button_prog('Run', True, False)
        button_prog_run = ui.ui_buttons['prog_run']
        # Add style for green colouring:
        run_style = 'color: #339933;';
        button_prog_run.setStyleSheet(run_style)
        grid.addWidget(button_prog_run, 1, 2, 1, 1)
