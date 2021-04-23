# -*- coding: utf-8 -*-
"""
Traverser configuration window
"""

# Standard lib imports:
from functools import partial
import os
# Third party imports:
from PyQt5.Qt import QIntValidator, QDoubleValidator
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QFileDialog, QLabel, QLineEdit, QPushButton,
                             QVBoxLayout, QWidget)
# Package imports:
from traverser import APP_NAME, APP_VERSION
from traverser.functions import convert_numeric
from traverser.ui_components.frame_column import FrameColumn
from traverser.ui_components.main_frame import MainFrame
from traverser.ui_components.ui_component import UIComponent
from traverser.ui_functions.config_functions import read_config, write_config

class ConfigArea(UIComponent):
    """
    Config area for confguration window
    """
    def __init__(self, config_window, ui):
        # Run parent init first:
        super().__init__(config_window, 2, show_frame=False)
        # Store config window and ui:
        self.config_window = config_window
        self.ui = ui
        # Run component init:
        self.init(config_window, ui)

    def setting_label(self, label):
        """
        Label for setting name
        """
        # Create and return the label:
        setting_label = QLabel('{0} :'.format(label), self)
        setting_label.setTextFormat(Qt.PlainText)
        setting_label.setFont(self.config_window.fonts['standard'])
        return setting_label

    def setting_check(self, setting_edit, config, setting):
        """
        Check things when a value is changed
        """
        # Get the value:
        value = convert_numeric(setting_edit.text())
        # If value is empty, reset:
        if not value:
            setting_edit.setText('{0}'.format(config.values[setting]))

    def setting_updated(self, setting_edit, config, setting,
                        value_labels=None, call_backs=None):
        """
        Update things when a value is changed
        """
        # Get the value:
        value = convert_numeric(setting_edit.text())
        # Update config:
        config.values[setting] = value
        # Update value labels:
        if value_labels:
            for value_label in value_labels:
                value_label.setText('{0}'.format(value))
        # run call back functions if defined:
        if call_backs:
            for call_back in call_backs:
                call_back()

    def setting_edit(self, s_type, min_val, max_val, value_labels,
                     config, setting, call_backs=None):
        """
        Create line edit to display / change a vlue
        """
        # Get value from input dialogue:
        default = config.values[setting]
        # Create the line edit:
        setting_edit = QLineEdit('{0}'.format(default))
        setting_edit.setAlignment(Qt.AlignRight)
        # Add validators ... int:
        if s_type == 'int':
            setting_edit.setValidator(QIntValidator(min_val, max_val))
        if s_type == 'dbl':
            setting_edit.setValidator(QDoubleValidator(min_val, max_val, 2))
        # Check for empty values on text changes:
        setting_edit.textChanged.connect(partial(
            self.setting_check, setting_edit, config, setting
        ))
        # Update values on update:
        setting_edit.editingFinished.connect(partial(
            self.setting_updated, setting_edit, config, setting, value_labels,
            call_backs
        ))
        # Return the value editor:
        return setting_edit

    def add_setting(self, ui, row, setting, s_type, s_label, s_min=None,
                    s_max=None, s_values=None, call_backs=None):
        """
        Add row to display and adjust a config setting
        """
        # Get the grid for the settings window:
        grid = self.properties['grid']
        # Add label for setting name:
        label_name = 'label_{0}'.format(setting)
        self.properties[label_name] = self.setting_label(s_label)
        label = self.properties[label_name]
        grid.addWidget(label, row, 0, 1, 1)
        # Add value editor:
        edit_name = 'edit_{0}'.format(setting)
        self.properties[edit_name] = self.setting_edit(
            s_type, s_min, s_max, s_values, ui.config, setting, call_backs
        )
        edit = self.properties[edit_name]
        grid.addWidget(edit, row, 1, 1, 1)

    def load_config(self, ui):
        """
        Load config from file
        """
        # Get the file name using file browser:
        config_file = QFileDialog.getOpenFileName(
            self, 'Select config file', ui.working_dir, 'ini files (*.ini)'
        )[0]
        # If no config file, give up:
        if not config_file:
            return
        # Read the config:
        status, config = read_config(ui.config, config_file)
        # If status is not True, give up:
        if status is not True:
            return
        # Set the working directory to the config file directory:
        ui.working_dir = os.path.dirname(config_file)
        # Update serial port label in UI:
        sp_value = ui.ui_components['connect_area'].properties['sp_label']
        sp_value.setText('{0}'.format(ui.config.values['serial_port']))
        # Re-init vixim:
        ui.init_vixim()
        # Re-init status area:
        ui.ui_components['status_area'].init()

    def init(self, config_window, ui):
        """
        Main component init
        """
        # Get self grid:
        grid = self.properties['grid']
        # Create a label for the area:
        self.properties['label'] = QLabel('Configuration Settings', self)
        label = self.properties['label']
        label.setTextFormat(Qt.PlainText)
        label.setFont(ui.fonts['bold'])
        grid.addWidget(label, 0, 0, 1, 2)
        # Serial port setting:
        s_values = [ui.ui_components['connect_area'].properties['sp_label']]
        self.add_setting(ui, 1, 'serial_port', 'str', 'Serial Port', 0, 0,
                         s_values, [ui.init_vixim])
        # Baud rate setting:
        self.add_setting(ui, 2, 'baud_rate', 'int', 'Baud Rate', 0, 115200,
                         None, [ui.init_vixim])
        # Velocity setting:
        self.add_setting(ui, 3, 'vel', 'dbl', 'Velocity', 0, 50,
                         None, [ui.init_vixim])
        # Acceleration setting:
        self.add_setting(ui, 4, 'accel', 'dbl', 'Acceleration', 0, 100,
                         None, [ui.init_vixim])
        # Deceleration setting:
        self.add_setting(ui, 5, 'decel', 'dbl', 'Deceleration', 0, 100,
                         None, [ui.init_vixim])
        # X motor setting:
        self.add_setting(ui, 6, 'x_motor', 'int', 'X Motor', 1, 2,
                         None, [ui.init_vixim])
        # Y motor setting:
        self.add_setting(ui, 7, 'y_motor', 'int', 'Y Motor', 1, 2,
                         None, [ui.init_vixim])
        # Max X setting:
        self.add_setting(ui, 8, 'max_x', 'int', 'Max X', 0, 5000000,
                         None, [ui.ui_components['status_area'].init,
                                ui.init_vixim])
        # Max Y setting:
        self.add_setting(ui, 9, 'max_y', 'int', 'Max Y', 0, 5000000,
                         None, [ui.ui_components['status_area'].init,
                                ui.init_vixim])
        # X distance:
        self.add_setting(ui, 10, 'x_dist', 'dbl', 'X distance', 0, 5000000,
                         None, None)
        # Y distance:
        self.add_setting(ui, 11, 'y_dist', 'dbl', 'Y distance', 0, 5000000,
                         None, None)
        # X units:
        self.add_setting(ui, 12, 'x_units', 'str', 'X units', 0, 0,
                         None, None)
        # Y units:
        self.add_setting(ui, 13, 'y_units', 'str', 'Y units', 0, 0,
                         None, None)
        # Instrument poll interval
        self.add_setting(ui, 14, 'poll_instrument', 'dbl',
                         'Poll Instrument (s)', 0.5, 60, None, None)

        # Insert blank label to create a spacer:
        grid.addWidget(QLabel(' '), 98, 0, 1, 3)
        # Load config button:
        self.properties['button_load'] = QPushButton('Load', self)
        button_load = self.properties['button_load']
        grid.addWidget(button_load, 99, 0, 1, 1)
        button_load.clicked.connect(partial(
            self.load_config, ui
        ))
        # Re-init config window after load:
        button_load.clicked.connect(partial(self.init, config_window, ui))
        # Save config button:
        self.properties['button_save'] = QPushButton('Save', self)
        button_save = self.properties['button_save']
        grid.addWidget(button_save, 99, 1, 1, 1)
        button_save.clicked.connect(partial(
            write_config, ui, ui.config
        ))

class ConfigWindow(QWidget):
    """
    QWidget class for setting configuration values
    """
    def __init__(self, ui):
        # Run parent init first:
        super().__init__()
        # Parent UI:
        self.ui = ui
        # Window properties. Height and width are initial / minimum sizes:
        self.window_properties = {
            'width': 450,
            'height': 0,
            'max_width': 500,
            'max_height': 0,
            'grid_spacing': 5
        }
        # Set up the UI layout:
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(self.window_properties['grid_spacing'])
        self.layout.setAlignment(Qt.AlignTop)
        # Define the fonts to use:
        self.fonts = {
            'standard': QFont(),
            'bold': QFont()
        }
        # Set font sizes:
        self.fonts['standard'].setPointSize(9)
        self.fonts['bold'].setPointSize(9)
        self.fonts['bold'].setBold(True)
        # Set default font:
        self.setFont(self.fonts['standard'])
        # UI components get stored here:
        self.ui_components = {}
        # UI buttons get stored here:
        self.ui_buttons = {}
        # Init the UI:
        self.init_ui(ui)

    def init_ui(self, ui):
        """
        Init the configuration settings window
        """
        # Set minimum windows width / height:
        self.setMinimumWidth(self.window_properties['width'])
        self.setMinimumHeight(self.window_properties['height'])
        # Set maximum windows width / height:
        self.setMaximumWidth(self.window_properties['max_width'])
        self.setMaximumHeight(self.window_properties['max_height'])
        # Set window title:
        self.setWindowTitle('{0} {1}'.format(APP_NAME,
                                             APP_VERSION))
        # Create the main UI frame which provides 3 columns:
        self.ui_components['main_frame'] = MainFrame(self, 1)
        main_frame = self.ui_components['main_frame']
        # Add main frame to layout:
        self.layout.addWidget(main_frame)
        # Get the main grid:
        main_grid = main_frame.properties['grid']
        # Single column:
        self.ui_components['column'] = FrameColumn(self)
        column = self.ui_components['column']
        main_grid.addWidget(column, 0, 0, 1, 1)
        column_grid = column.properties['grid']
        column_grid.setAlignment(Qt.AlignTop)
        # Configuration settings area:
        self.ui_components['config_area'] = ConfigArea(self, ui)
        config_area = self.ui_components['config_area']
        column_grid.addWidget(config_area, 1, 0, 1, 1)

    def open(self):
        """
        Open the configuration settings window
        """
        # Show the window:
        self.show()

    def close(self):
        """
        Close the configuration settings window
        """
        # Hide the window:
        self.hide()
