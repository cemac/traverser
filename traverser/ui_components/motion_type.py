# -*- coding: utf-8 -*-
"""
Traverser motion type area
"""

# Third party imports:
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QPushButton
# Package imports:
from traverser.ui_components.ui_component import UIComponent

class MotionType(UIComponent):
    """
    Motion Type area for traverser UI
    """
    def __init__(self, ui):
        # Run parent init first:
        super().__init__(ui, 10)
        # Run component init:
        self.init(ui)

    def button_type(self, label, checkable=False, enabled=False):
        """
        Create the motion type button
        """
        # Create the QPushButton:
        button_type = QPushButton(label, self)
        button_type.setCheckable(checkable)
        button_type.setEnabled(enabled)
        # Return the button:
        return button_type

    def type_property(self, ui, enabled=False):
        """
        Return a motion type property display / update object
        """
        # Value for the property:
        property_value = QLabel(' -- ', self)
        property_value.setTextFormat(Qt.PlainText)
        property_value.setAlignment(Qt.AlignCenter|Qt.AlignVCenter)
        # Button to change values:
        property_button = QPushButton('Change value', self)
        property_button.setEnabled(enabled)
        # Return the label and value:
        return property_value, property_button

    def init(self, ui):
        """
        Main component init
        """
        # Get self grid:
        grid = self.properties['grid']
        # Create a label for the area:
        self.properties['label'] = QLabel('Motion Type', self)
        label = self.properties['label']
        label.setTextFormat(Qt.PlainText)
        label.setFont(ui.fonts['bold'])
        grid.addWidget(label, 0, 0, 1, 5)
        # Create the motion type button:
        ui.ui_buttons['motion_type'] = self.button_type('Constant', True)
        button_motion_type = ui.ui_buttons['motion_type']
        grid.addWidget(button_motion_type, 1, 0, 1, 3)
        # Distance settings:
        [self.properties['dist_value'],
         ui.ui_buttons['dist']] = self.type_property(ui)
        dist_value = self.properties['dist_value']
        dist_button = ui.ui_buttons['dist']
        grid.addWidget(dist_value, 1, 3, 1, 4)
        grid.addWidget(dist_button, 1, 7, 1, 3)
