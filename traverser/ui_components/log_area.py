# -*- coding: utf-8 -*-
"""
Traverser log area
"""

# Third party imports:
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QPushButton, QTextEdit
# Package imports:
from traverser.ui_components.ui_component import UIComponent

class LogArea(UIComponent):
    """
    Log area for traverser UI
    """
    def __init__(self, ui):
        # Run parent init first:
        super().__init__(ui, 3)
        # Run component init:
        self.init(ui)

    def button_clear(self, ui):
        """
        Create the clear button
        """
        # Create the QPushButton:
        button_clear = QPushButton('Clear', self)
        # Return the button:
        return button_clear

    def init(self, ui):
        """
        Main component init
        """
        # Get self grid:
        grid = self.properties['grid']

        # Create a label for the area:
        self.properties['label'] = QLabel('Log', self)
        label = self.properties['label']
        label.setTextFormat(Qt.PlainText)
        label.setFont(ui.fonts['bold'])
        grid.addWidget(label, 0, 0)

        # Create the clear button:
        ui.ui_buttons['log_clear'] = self.button_clear(ui)
        button_clear = ui.ui_buttons['log_clear']
        grid.addWidget(button_clear, 0, 2)

        # Add the log message area:
        ui.ui_log['text'] = QTextEdit(ui)
        log_text = ui.ui_log['text']
        log_text.setReadOnly(True)
        grid.addWidget(log_text, 1, 0, 1, 3)
