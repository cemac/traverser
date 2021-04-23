# -*- coding: utf-8 -*-
"""
Traverser program configuration window
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
from traverser.ui_functions.program_functions import (
    init_program, load_program, set_program
)

class ProgramArea(UIComponent):
    """
    Program area for program window
    """
    def __init__(self, program_window, ui):
        # Run parent init first:
        super().__init__(program_window, 2, show_frame=False)
        # Store config window and ui:
        self.program_window = program_window
        self.ui = ui
        # Run component init:
        self.init(program_window, ui)

    def setting_label(self, label):
        """
        Label for setting name
        """
        # Create and return the label:
        setting_label = QLabel('{0} :'.format(label), self)
        setting_label.setTextFormat(Qt.PlainText)
        setting_label.setFont(self.program_window.fonts['standard'])
        return setting_label

    def setting_check(self, setting_edit, program, setting):
        """
        Check things when a value is changed
        """
        # Get the value:
        value = convert_numeric(setting_edit.text())
        # If value is empty, reset:
        if not value:
            setting_edit.setText('{0}'.format(program[setting]))

    def update_program(self):
        """
        Update the program
        """
        # Get values:
        program = self.ui.program
        min_x = program['min_x']
        max_x = program['max_x']
        x_inc = program['x_inc']
        min_y = program['min_y']
        max_y = program['max_y']
        y_inc = program['y_inc']
        order = program['order']
        pre_delay = program['pre_delay']
        post_delay = program['post_delay']
        # Set the program:
        set_program(self.ui, min_x, max_x, min_y, max_y, x_inc, y_inc,
                    pre_delay, post_delay, order)

    def setting_updated(self, setting_edit, program, setting):
        """
        Update things when a value is changed
        """
        # Get the value:
        value = convert_numeric(setting_edit.text())
        # Update config:
        program[setting] = value
        # Update program:
        self.update_program()

    def setting_edit(self, s_type, min_val, max_val, program,
                     setting):
        """
        Create line edit to display / change a vlue
        """
        # Get value from input dialogue:
        default = program[setting]
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
            self.setting_check, setting_edit, program, setting
        ))
        # Update values on update:
        setting_edit.editingFinished.connect(partial(
            self.setting_updated, setting_edit, program, setting
        ))
        # Return the value editor:
        return setting_edit

    def add_setting(self, ui, row, setting, s_type, s_label, s_min=None,
                    s_max=None):
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
            s_type, s_min, s_max, ui.program, setting
        )
        edit = self.properties[edit_name]
        grid.addWidget(edit, row, 1, 1, 1)

    def set_order(self, ui, button_xy, button_yx, order):
        """
        Set program order
        """
        # If xy:
        if order == 'xy':
            button_xy.setChecked(True)
            button_yx.setChecked(False)
        else:
            button_yx.setChecked(True)
            button_xy.setChecked(False)
        # Save the value:
        ui.program['order'] = order
        # Update program:
        self.update_program()

    def load_program(self, ui):
        """
        Load program from file
        """
        # Get the file name using file browser:
        program_file = QFileDialog.getOpenFileName(
            self, 'Select program file', ui.working_dir, 'csv files (*.csv)'
        )[0]
        # If no file, give up:
        if not program_file:
            return
        # Read the config:
        status, err_msg = load_program(ui, program_file)
        # If status is not True, give up:
        if status is not True:
            ui.log_message(err_msg, status)
            return
        # Set the working directory to the program file directory:
        ui.working_dir = os.path.dirname(program_file)

    def init(self, program_window, ui):
        """
        Main component init
        """
        # Get self grid:
        grid = self.properties['grid']
        # Create a label for the area:
        self.properties['label'] = QLabel('Program Settings', self)
        label = self.properties['label']
        label.setTextFormat(Qt.PlainText)
        label.setFont(ui.fonts['bold'])
        grid.addWidget(label, 0, 0, 1, 2)
        # Get units:
        x_units = ui.config.values['x_units']
        y_units = ui.config.values['y_units']
        # Min x setting:
        s_label = 'Min X ({0})'.format(x_units)
        self.add_setting(ui, 1, 'min_x', 'int', s_label, 0,
                         ui.config.values['x_dist'])
        # Max x setting:
        s_label = 'Max X ({0})'.format(x_units)
        self.add_setting(ui, 2, 'max_x', 'int', s_label, 0,
                         ui.config.values['x_dist'])
        # X increment setting:
        s_label = 'X increment ({0})'.format(x_units)
        self.add_setting(ui, 3, 'x_inc', 'int', s_label, 0,
                         ui.config.values['x_dist'])
        # Min y setting:
        s_label = 'Min Y ({0})'.format(y_units)
        self.add_setting(ui, 4, 'min_y', 'int', s_label, 0,
                         ui.config.values['y_dist'])
        # Max y setting:
        s_label = 'Max Y ({0})'.format(y_units)
        self.add_setting(ui, 5, 'max_y', 'int', s_label, 0,
                         ui.config.values['y_dist'])
        # Y increment setting:
        s_label = 'Y increment ({0})'.format(y_units)
        self.add_setting(ui, 6, 'y_inc', 'int', s_label, 0,
                         ui.config.values['y_dist'])
        # Order:
        self.properties['label_order'] = self.setting_label('Order')
        label_order = self.properties['label_order']
        grid.addWidget(label_order, 7, 0, 1, 1)
        self.properties['button_xy'] = QPushButton('X Y', self)
        button_xy = self.properties['button_xy']
        button_xy.setCheckable(True)
        grid.addWidget(button_xy, 7, 1, 1, 1)
        self.properties['button_yx'] = QPushButton('Y X', self)
        button_yx = self.properties['button_yx']
        button_yx.setCheckable(True)
        grid.addWidget(button_yx, 8, 1, 1, 1)
        if ui.program['order'] == 'xy':
            button_xy.setChecked(True)
        else:
            button_yx.setChecked(True)
        button_xy.clicked.connect(partial(self.set_order, ui, button_xy,
                                          button_yx, 'xy'))
        button_yx.clicked.connect(partial(self.set_order, ui, button_xy,
                                          button_yx, 'yx'))
        # Pre measurement reading delay:
        s_label = 'Pre delay (s)'
        self.add_setting(ui, 9, 'pre_delay', 'dbl', s_label, 0, 60)
        # Post measurement reading delay:
        s_label = 'Post delay (s)'
        self.add_setting(ui, 10, 'post_delay', 'dbl', s_label, 0, 60)
        # Insert blank label to create a spacer:
        grid.addWidget(QLabel(' '), 98, 0, 1, 3)
        # Load program button:
        self.properties['button_load'] = QPushButton('Load', self)
        button_load = self.properties['button_load']
        grid.addWidget(button_load, 99, 1, 1, 1)
        button_load.clicked.connect(partial(
            self.load_program, ui
        ))
        # Close program window after load:
        button_load.clicked.connect(program_window.close)

class ProgramWindow(QWidget):
    """
    QWidget class for setting program values
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
        # Program settings area:
        self.ui_components['program_area'] = ProgramArea(self, ui)
        program_area = self.ui_components['program_area']
        column_grid.addWidget(program_area, 1, 0, 1, 1)

    def open(self):
        """
        Open the program settings window
        """
        # If no program exists, make one up:
        if self.ui.program['x'] is None and self.ui.program['y'] is None:
            init_program(self.ui)
            self.ui_components['program_area'].init(self, self.ui)
        # Show the window:
        self.show()
        # enable the program running button:
        button_prog_run = self.ui.ui_buttons['prog_run']
        button_prog_run.setEnabled(True)

    def close(self):
        """
        Close the program settings window
        """
        # Hide the window:
        self.hide()
