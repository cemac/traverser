# -*- coding: utf-8 -*-
"""
Traverser motion settings
"""

# Third party imports:
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QPushButton
# Package imports:
from traverser.ui_components.ui_component import UIComponent

class MotionSettings(UIComponent):
    """
    Motion settings area for traverser UI
    """
    def __init__(self, ui):
        # Run parent init first:
        super().__init__(ui, 3)
        # Run component init:
        self.init(ui)

    def motion_property(self, ui, label, enabled=False):
        """
        Return a motion property display / update object
        """
        # Label for the property:
        text_label = '{0} :'.format(label)
        property_label = QLabel(text_label, self)
        property_label.setTextFormat(Qt.PlainText)
        property_label.setFont(ui.fonts['bold'])
        property_label.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        # Value for the property:
        property_value = QLabel(' -- ', self)
        property_value.setTextFormat(Qt.PlainText)
        property_value.setAlignment(Qt.AlignCenter|Qt.AlignVCenter)
        # Button to change values:
        property_button = QPushButton('Change value', self)
        property_button.setEnabled(enabled)
        # Return the label and value:
        return property_label, property_value, property_button

    def init(self, ui):
        """
        Main component init
        """
        # Get self grid:
        grid = self.properties['grid']
        # Create a label for the area:
        self.properties['label'] = QLabel('Motion Settings', self)
        label = self.properties['label']
        label.setTextFormat(Qt.PlainText)
        label.setFont(ui.fonts['bold'])
        grid.addWidget(label, 0, 0, 1, 1)
        # Add properties ... velocity:
        [self.properties['vel_label'], self.properties['vel_value'],
         ui.ui_buttons['vel']] = self.motion_property(ui, 'Velocity')
        vel_label = self.properties['vel_label']
        vel_value = self.properties['vel_value']
        vel_button = ui.ui_buttons['vel']
        grid.addWidget(vel_label, 1, 0, 1, 1)
        grid.addWidget(vel_value, 1, 1, 1, 1)
        grid.addWidget(vel_button, 1, 2, 1, 1)
        # Acceleration:
        [self.properties['accel_label'], self.properties['accel_value'],
         ui.ui_buttons['accel']] = self.motion_property(ui, 'Acceleration')
        accel_label = self.properties['accel_label']
        accel_value = self.properties['accel_value']
        accel_button = ui.ui_buttons['accel']
        grid.addWidget(accel_label, 2, 0, 1, 1)
        grid.addWidget(accel_value, 2, 1, 1, 1)
        grid.addWidget(accel_button, 2, 2, 1, 1)
        # Deceleration:
        [self.properties['decel_label'], self.properties['decel_value'],
         ui.ui_buttons['decel']] = self.motion_property(ui, 'Deceleration')
        decel_label = self.properties['decel_label']
        decel_value = self.properties['decel_value']
        decel_button = ui.ui_buttons['decel']
        grid.addWidget(decel_label, 3, 0, 1, 1)
        grid.addWidget(decel_value, 3, 1, 1, 1)
        grid.addWidget(decel_button, 3, 2, 1, 1)
