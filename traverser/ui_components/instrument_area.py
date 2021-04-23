# -*- coding: utf-8 -*-
"""
Traverser instrument area
"""

# Standard lib imports:
from functools import partial
# Third party imports:
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QMenu, QPushButton
# Package imports:
from traverser import instruments
from traverser.ui_components.ui_component import UIComponent

class InstrumentArea(UIComponent):
    """
    Instrument selection area for traverser UI
    """
    def __init__(self, ui):
        # Run parent init first:
        super().__init__(ui, 3)
        # Run component init:
        self.init(ui)

    def set_instrument(self, ui, inst_name, inst_class):
        """
        Set the current instrument
        """
        # If an instrument is selected:
        if ui.instrument is not None:
            # Try to disconnect first:
            status, status_message = ui.instrument.disconnect()
            if not status:
                err_name = ui.instrument.get_name()
                err_msg = 'Failed to disconnect {0}'.format(err_name)
                if status_message:
                    err_msg += '({0})'.format(status_message)
                ui.log_message(err_msg, False)
        # Remove value labels:
        grid = self.properties['grid']
        for i, i_id in enumerate(self.values['ids']):
            grid.removeWidget(self.values['labels'][i])
            grid.removeWidget(self.values['values'][i])
            self.values['labels'][i].setParent(None)
            self.values['values'][i].setParent(None)
        self.values['ids'] = []
        self.values['labels'] = []
        self.values['values'] = []
        # Set the new instrument:
        ui.instrument = inst_class()
        # Update label:
        name_label = self.properties['name_label']
        name_label.setText(inst_name)
        # Try to connect:
        status, status_message = ui.instrument.connect()
        err_name = ui.instrument.get_name()
        if not status:
            err_msg = 'Failed to connect to {0}'.format(err_name)
            if status_message:
                err_msg += '({0})'.format(status_message)
            ui.log_message(err_msg, status)
        else:
            err_msg = 'Connected {0}'.format(err_name)
            ui.log_message(err_msg, status)
        # If not connected, return:
        if not ui.instrument.connected:
            return
        # Enable and check the connect button:
        button_inst_connect = ui.ui_buttons['inst_connect']
        button_inst_connect.setEnabled(True)
        button_inst_connect.setChecked(True)
        button_inst_connect.setText('Disconnect')
        # Set up instrument values ... acquire a reading:
        ui.instrument_values = ui.instrument.acquire()
        instrument_values = ui.instrument_values
        # First row for instrument values:
        id_count = 2
        # Loop through value ids:
        for i, i_id in enumerate(instrument_values['ids']):
            # Add label:
            self.values['ids'].append(i_id)
            i_label = QLabel('{0} :'.format(i_id), self)
            i_label.setTextFormat(Qt.PlainText)
            i_label.setFont(ui.fonts['bold'])
            i_label.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
            grid.addWidget(i_label, id_count, 0, 1, 1)
            self.values['labels'].append(i_label)
            # Add value:
            if instrument_values['error'][i] is True:
                i_text = 'Error'
                i_style = 'color: #993333;'
            else:
                i_value = instrument_values['values'][i]
                i_units = instrument_values['units'][i]
                i_text = '{0} {1}'.format(i_value, i_units)
                i_style = 'color: #000000;'
            i_value = QLabel(i_text, self)
            i_value.setTextFormat(Qt.PlainText)
            i_value.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
            i_value.setStyleSheet(i_style)
            i_value.setFont(ui.fonts['standard'])
            grid.addWidget(i_value, id_count, 1, 1, 2)
            self.values['values'].append(i_value)
            # Increment the count
            id_count += 1

    def button_connect(self):
        """
        Create the connect button
        """
        # Create the QPushButton:
        button_connect = QPushButton('Connect', self)
        button_connect.setCheckable(True)
        # Return the button:
        return button_connect

    def init(self, ui):
        """
        Main component init
        """
        # Get self grid:
        grid = self.properties['grid']
        # Create a label for the area:
        self.properties['label'] = QLabel('Instrument', self)
        label = self.properties['label']
        label.setTextFormat(Qt.PlainText)
        label.setFont(ui.fonts['bold'])
        grid.addWidget(label, 0, 0, 1, 1)
        # Create drop down to select instrument:
        self.properties['menu'] = QMenu()
        menu = self.properties['menu']
        # Loop through instruments, adding to menu:
        for i in instruments.INSTRUMENTS['instruments']:
            inst_name = i['name']
            inst_class = i['class']
            inst_act = menu.addAction(inst_name)
            inst_act.triggered.connect(partial(self.set_instrument, ui,
                                               inst_name, inst_class))
        # Create the select instrument button:
        ui.ui_buttons['inst_select'] = QPushButton('Select', self)
        button_inst_select = ui.ui_buttons['inst_select']
        button_inst_select.setMenu(menu)
        grid.addWidget(button_inst_select, 0, 1, 1, 2)
        # Current instrument name:
        self.properties['name_label'] = QLabel(' -- ', self)
        name_label = self.properties['name_label']
        name_label.setTextFormat(Qt.PlainText)
        name_label.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
        grid.addWidget(name_label, 1, 1, 1, 2)
        # Dict for storing current value items:
        self.values = {
            'ids': [],
            'labels': [],
            'values': []
        }
        # Create the connect button and disable:
        ui.ui_buttons['inst_connect'] = self.button_connect()
        button_inst_connect = ui.ui_buttons['inst_connect']
        grid.addWidget(button_inst_connect, 99, 2, 1, 1)
        button_inst_connect.setDisabled(True)
