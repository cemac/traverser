# -*- coding: utf-8 -*-
"""
Traverser connect / disconnect area
"""

# Third party imports:
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QPushButton
# Package imports:
from traverser.ui_components.ui_component import UIComponent

class ConnectArea(UIComponent):
    """
    Connect / disconnect area for traverser UI
    """
    def __init__(self, ui):
        # Run parent init first:
        super().__init__(ui, 3)
        # Run component init:
        self.init(ui)

    def button_connect(self, label, checkable=False, enabled=True):
        """
        Create the connect button
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
        # Create a label for the port:
        self.properties['label'] = QLabel('Serial Port :', self)
        label = self.properties['label']
        label.setTextFormat(Qt.PlainText)
        label.setFont(ui.fonts['bold'])
        label.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        grid.addWidget(label, 0, 0, 1, 1)
        # Create a label for the port information:
        self.properties['sp_label'] = QLabel(ui.config.values['serial_port'],
                                             self)
        sp_label = self.properties['sp_label']
        sp_label.setTextFormat(Qt.PlainText)
        sp_label.setAlignment(Qt.AlignCenter|Qt.AlignVCenter)
        grid.addWidget(sp_label, 0, 1, 1, 1)
        # Create the connect button:
        ui.ui_buttons['connect'] = self.button_connect('Connect', True)
        button_connect = ui.ui_buttons['connect']
        grid.addWidget(button_connect, 0, 2, 1, 1)
        # Create the configure buttion:
        ui.ui_buttons['configure'] = self.button_connect('Configure')
        button_configure = ui.ui_buttons['configure']
        grid.addWidget(button_configure, 1, 0, 1, 1)
        # Create the start button:
        ui.ui_buttons['start'] = self.button_connect('Start', True, False)
        button_start = ui.ui_buttons['start']
        # Add style for green colouring:
        start_style = 'color: #339933;'
        button_start.setStyleSheet(start_style)
        grid.addWidget(button_start, 1, 2, 1, 1)
