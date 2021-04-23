# -*- coding: utf-8 -*-
"""
Traverser motion control area
"""

# Third party imports:
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QGridLayout, QLabel, QPushButton
# Package imports:
from traverser.ui_components.ui_component import UIComponent

class MotionControl(UIComponent):
    """
    Motion control area for Traverser UI
    """
    def __init__(self, ui):
        # Run parent init first:
        super().__init__(ui, 3)
        # Button size:
        self.button_size = 45
        # Run component init:
        self.init(ui)

    def button_control(self, label, tooltip='', checkable=True,
                       enabled=False):
        """
        Create the control button
        """
        # Create the QPushButton:
        button_control = QPushButton(label, self)
        # Fixed size to ensure squareness ... :
        button_control.setFixedSize(self.button_size, self.button_size)
        # Set checkable property:
        button_control.setCheckable(checkable)
        # Set tooltip:
        button_control.setToolTip(tooltip)
        # Set enabled / disabled:
        button_control.setEnabled(enabled)
        # Return the button:
        return button_control

    def init(self, ui):
        """
        Main component init
        """
        # Get self grid:
        grid = self.properties['grid']
        # Create a label for the area:
        self.properties['label'] = QLabel('Motion Control', self)
        label = self.properties['label']
        label.setTextFormat(Qt.PlainText)
        label.setFont(ui.fonts['bold'])
        grid.addWidget(label, 0, 0, 1, 1)

        # Create frame for control buttons:
        self.properties['control_frame'] = QFrame(ui)
        control_frame = self.properties['control_frame']
        # Create grid for control buttons:
        self.properties['control_grid'] = QGridLayout(control_frame)
        control_grid = self.properties['control_grid']
        # Grid spacing:
        grid_spacing = ui.window_properties['grid_spacing']
        control_grid.setSpacing(grid_spacing)
        # Set fixed size for grid:
        control_frame.setFixedWidth((self.button_size * 3) +
                                    (5 * grid_spacing))
        control_frame.setFixedHeight((self.button_size * 3) +
                                     (5 * grid_spacing))
        # Add frame to existing grid:
        grid.addWidget(control_frame, 1, 1, 1, 3, Qt.AlignLeft)

        # Create the control buttons ... y plus:
        ui.ui_buttons['control_yplus'] = self.button_control('Y+')
        button_control_yplus = ui.ui_buttons['control_yplus']
        control_grid.addWidget(button_control_yplus, 1, 1, 1, 1)
        # ... y minus ... :
        ui.ui_buttons['control_yminus'] = self.button_control('Y-')
        button_control_yminus = ui.ui_buttons['control_yminus']
        control_grid.addWidget(button_control_yminus, 3, 1, 1, 1)
        # ... x minus ... :
        ui.ui_buttons['control_xminus'] = self.button_control('X-')
        button_control_xminus = ui.ui_buttons['control_xminus']
        control_grid.addWidget(button_control_xminus, 2, 0, 1, 1,
                               Qt.AlignRight)
        # ... x plus ... :
        ui.ui_buttons['control_xplus'] = self.button_control('X+')
        button_control_xplus = ui.ui_buttons['control_xplus']
        control_grid.addWidget(button_control_xplus, 2, 2, 1, 1, Qt.AlignLeft)
        # ... go home ... :
        ui.ui_buttons['control_gh'] = self.button_control('GH', 'Go Home')
        button_control_gh = ui.ui_buttons['control_gh']
        control_grid.addWidget(button_control_gh, 3, 0, 1, 1, Qt.AlignRight)
        # ... stop!:
        ui.ui_buttons['control_stop'] = self.button_control('!', 'Stop', False,
                                                            True)
        button_control_stop = ui.ui_buttons['control_stop']
        # Add style for red colouring and bold font:
        stop_style = 'color: #993333;'
        button_control_stop.setStyleSheet(stop_style)
        button_control_stop.setFont(ui.fonts['bold'])
        control_grid.addWidget(button_control_stop, 3, 2, 1, 1, Qt.AlignLeft)
