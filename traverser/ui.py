# -*- coding: utf-8 -*-
"""
Traverser UI class
"""

# Standard lib imports:
import datetime
import os
import sys
from functools import partial
# Third party imports:
from PyQt5.Qt import QTextCursor
from PyQt5.QtCore import Qt, pyqtSignal, QMutex
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QApplication, QFileDialog, QMessageBox,
                             QVBoxLayout, QWidget)
# Package imports:
from traverser import APP_NAME, APP_VERSION
#from traverser.vixim import VixIM
from traverser.dummy_vixim import VixIM
# UI components:
from traverser.ui_components.config_window import ConfigWindow
from traverser.ui_components.connect_area import ConnectArea
from traverser.ui_components.exit_area import ExitArea
from traverser.ui_components.frame_column import FrameColumn
from traverser.ui_components.instrument_area import InstrumentArea
from traverser.ui_components.log_area import LogArea
from traverser.ui_components.main_frame import MainFrame
from traverser.ui_components.motion_control import MotionControl
from traverser.ui_components.motion_settings import MotionSettings
from traverser.ui_components.program_control import ProgramControl
from traverser.ui_components.program_window import ProgramWindow
from traverser.ui_components.status_area import StatusArea
# UI functions:
from traverser.ui_functions.connect_functions import toggle_connect
from traverser.ui_functions.config_functions import get_config
from traverser.ui_functions.exit_functions import program_exit
from traverser.ui_functions.instrument_functions import toggle_inst_connect
from traverser.ui_functions.motion_control_functions import (
    toggle_yplus, toggle_yminus, toggle_xplus, toggle_xminus, toggle_gh
)
from traverser.ui_functions.motion_settings_functions import set_motion
from traverser.ui_functions.status_functions import plot_status, plot_program
# UI threads:
from traverser.ui_threads.poll_instrument import PollInstrument
from traverser.ui_threads.poll_status import PollStatus
from traverser.ui_threads.run_program import RunProgram
from traverser.ui_threads.start_motion import StartMotion
from traverser.ui_threads.stop_motion import StopMotion

class TraverserUI(QWidget):
    """
    Main QWidget class for the application. Creates the UI, spawns the various
    threads for polling and running the program, etc.
    """
    # Message logging signal:
    _log_message = pyqtSignal(str, bool)
    # Log file setting signal:
    _set_log_file = pyqtSignal()
    # Alert displaying signal:
    _display_alert = pyqtSignal(str)

    def __init__(self):
        # Run parent init first:
        super().__init__()
        # UI Window properties. Height and width are initial / minimum sizes:
        self.window_properties = {
            'width': 1250,
            'height': 625,
            'max_width': 2000,
            'max_height': 1100,
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
        # Configuration:
        self.config = get_config(self)
        # Motor controller:
        self.vixim = None
        # Status information:
        self.status = {
            # Connection status:
            'connected': 0,
            # Current posision:
            'x': None,
            'y': None
        }
        # Flag to indicate program is exiting:
        self.exiting = 0
        # Instrument gets stored here:
        self.instrument = None
        self.instrument_values = None
        # Program information gets stored here:
        self.program = {
            'x': None,
            'y': None,
            'min_x': 0,
            'max_x': 0,
            'x_inc': 0,
            'min_y': 0,
            'max_y': 0,
            'y_inc': 0,
            'order': 'xy',
            'pre_delay': 0,
            'post_delay': 0,
            'log_file': None,
            'running': False,
            'updated': False
        }
        # UI components get stored here:
        self.ui_components = {}
        # UI buttons get stored here:
        self.ui_buttons = {}
        # UI threads get stored here:
        self.ui_threads = {}
        # UI log information:
        self.ui_log = {}
        # Init the motor controller object:
        self.init_vixim()
        # Vixim / serial access lock:
        self.vixim_lock = QMutex()
        # Set inital working directory to home:
        self.working_dir = os.path.expanduser('~')
        # Init the UI:
        self.init_ui()

    @staticmethod
    def display_alert(alert_msg):
        """
        Display an alert message
        """
        # Create the QMessageBox:
        alert = QMessageBox()
        # Add a bit of redness to the acknowledgement button:
        alert.setStyleSheet('QPushButton {background-color: #ff3333;}')
        # Set the title and text of the alert:
        alert.setWindowTitle(APP_NAME)
        alert.setText(alert_msg)
        # Alert!:
        alert.exec_()

    def closeEvent(self, event):
        """
        Close the UI and application
        """
        # Quite the application:
        QApplication.instance().quit()

    def log_clear(self):
        """
        Clear the log messages
        """
        # Get the log information:
        log_text = self.ui_log['text']
        # Clear the log:
        log_text.clear()

    def __log_message(self, log_msg, status=True):
        """
        Function to log a message
        """
        # Give up if the UI does not exist:
        try:
            # Get the log information:
            log_text = self.ui_log['text']
        except AttributeError:
            return
        # Create a cursor, set position to 0 to insert text at the top:
        log_cursor = QTextCursor(log_text.document())
        log_cursor.setPosition(0)
        log_text.setTextCursor(log_cursor)
        # Get current date:
        log_dt = datetime.datetime.now()
        log_date = log_dt.strftime('%Y-%m-%d %H:%M:%S')
        # Formatted log message:
        log_message = '{0} : {1}'.format(log_date, log_msg)
        # If status is true, this is not an error message:
        if status:
            # Use default text color:
            log_html = '{0}<br>'.format(log_message)
        # Else this is an error message:
        else:
            # Set text to red:
            log_html = '<font color="#990000">{0}</font><br>'
            log_html = log_html.format(log_message)
        # Add the message:
        log_text.insertHtml(log_html)

    def log_message(self, log_msg, status=True):
        """
        Send signal to log a message
        """
        # If not exiting, emit the signal:
        try:
            if self.exiting == 0:
                self._log_message.emit(log_msg, status)
        except AttributeError:
            return

    def init_vixim(self):
        """
        Init VixIM object
        """
        # Get config values:
        config_values = self.config.values
        # Work out limits:
        if config_values['x_motor'] == 1:
            limits = {
                1: config_values['max_x'],
                2: config_values['max_y']
            }
        else:
            limits = {
                1: config_values['max_y'],
                2: config_values['max_x']
            }
        # Create the VixIM object:
        try:
            self.vixim = VixIM(
                port=config_values['serial_port'],
                baud_rate=config_values['baud_rate'],
                timeout=config_values['timeout'],
                vel=config_values['vel'],
                accel=config_values['accel'],
                limits=limits
            )
        except:
            self.display_alert("Failed to create VixIM object")
            sys.exit(1)

    def init_buttons(self):
        """
        Set up buttons functionality
        """
        # Connect / disconnect button:
        button_connect = self.ui_buttons['connect']
        button_connect.clicked.connect(partial(toggle_connect, self))
        # Configure button:
        button_configure = self.ui_buttons['configure']
        button_configure.clicked.connect(self.config_window.open)
        # Motion control buttons ... y plus / y minus:
        button_control_yplus = self.ui_buttons['control_yplus']
        button_control_yplus.clicked.connect(partial(toggle_yplus, self))
        button_control_yminus = self.ui_buttons['control_yminus']
        button_control_yminus.clicked.connect(partial(toggle_yminus, self))
        # x plus / minus:
        button_control_xplus = self.ui_buttons['control_xplus']
        button_control_xplus.clicked.connect(partial(toggle_xplus, self))
        button_control_xminus = self.ui_buttons['control_xminus']
        button_control_xminus.clicked.connect(partial(toggle_xminus, self))
        # Go home:
        button_control_gh = self.ui_buttons['control_gh']
        button_control_gh.clicked.connect(partial(toggle_gh, self))
        # Velocity setting:
        button_vel = self.ui_buttons['vel']
        button_vel.clicked.connect(partial(set_motion, self, 'vel'))
        # Accel setting:
        button_accel = self.ui_buttons['accel']
        button_accel.clicked.connect(partial(set_motion, self, 'accel'))
        # Decel setting:
        button_decel = self.ui_buttons['decel']
        button_decel.clicked.connect(partial(set_motion, self, 'decel'))
        # Program configure:
        button_prog_config = self.ui_buttons['prog_config']
        button_prog_config .clicked.connect(self.program_window.open)
        # Exit button:
        button_exit = self.ui_buttons['exit']
        button_exit.clicked.connect(partial(program_exit, self))
        # Instrument connect button:
        button_inst_connect = self.ui_buttons['inst_connect']
        button_inst_connect.clicked.connect(partial(toggle_inst_connect,
                                                    self))
        # Log clearing button:
        button_log_clear = self.ui_buttons['log_clear']
        button_log_clear.clicked.connect(self.log_clear)

    def stop_thread(self, thread_name, force=False):
        """
        Stop a thread
        """
        # Get the thread and stop it:
        thread = self.ui_threads[thread_name]
        if force is True:
            thread.terminate()
        else:
            thread.quit()

    def start_thread(self, thread_name):
        """
        Start a thread
        """
        # Get the thread and start it:
        thread = self.ui_threads[thread_name]
        thread.start()

    def init_threads(self):
        """
        Set up UI threads
        """
        # Motion starting thread:
        self.ui_threads['start'] = StartMotion(self)
        thread_start = self.ui_threads['start']
        thread_start.start()
        # Connect start button to start thread:
        button_start = self.ui_buttons['start']
        button_start.clicked.connect(thread_start.start_it)
        # Motion stopping thread:
        self.ui_threads['stop'] = StopMotion(self)
        thread_stop = self.ui_threads['stop']
        thread_stop.stop_thread.connect(self.stop_thread)
        thread_stop.start_thread.connect(self.start_thread)
        thread_stop.start()
        # Connect stop button to stop thread:
        button_control_stop = self.ui_buttons['control_stop']
        button_control_stop.clicked.connect(thread_stop.stop_it)
        # Program running thread:
        self.ui_threads['prog_run'] = RunProgram(self)
        thread_prog_run = self.ui_threads['prog_run']
        thread_prog_run.start()
        # Connect run button to run thread:
        button_prog_run = self.ui_buttons['prog_run']
        button_prog_run.clicked.connect(thread_prog_run.start_it)
        # Create the status polling thread:
        poll_status = 0.5
        self.ui_threads['status'] = PollStatus(self, poll_status)
        thread_status = self.ui_threads['status']
        thread_status.plot_status.connect(
            partial(plot_status, self)
        )
        thread_status.plot_program.connect(
            partial(plot_program, self)
        )
        thread_status.start()
        # Create the instrument polling thread:
        poll_inst = self.config.values['poll_instrument']
        self.ui_threads['instrument'] = PollInstrument(
            self, self.config, 'poll_instrument', poll_inst
        )
        thread_instrument = self.ui_threads['instrument']
        thread_instrument.start()

    def set_log_file(self):
        """
        Set program log file
        """
        # Get log file with file dialogue:
        log_file = QFileDialog.getSaveFileName(self, 'Select Output File',
                                               self.working_dir,
                                               'csv files (*.csv)')[0]
        # Check value:
        if log_file is None or log_file == '':
            log_file = False
        # Update program log file:
        self.program['log_file'] = log_file

    def init_ui(self):
        """
        Init the application and UI
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
        self.ui_components['main_frame'] = MainFrame(self)
        main_frame = self.ui_components['main_frame']
        # Add main frame to layout:
        self.layout.addWidget(main_frame)
        # Get the main grid:
        main_grid = main_frame.properties['grid']

        # First column ...
        self.ui_components['column_a'] = FrameColumn(self)
        column_a = self.ui_components['column_a']
        main_grid.addWidget(column_a, 0, 0, 1, 1)
        column_a_grid = column_a.properties['grid']
        column_a_grid.setAlignment(Qt.AlignTop)
        # Connect / disconnect:
        self.ui_components['connect_area'] = ConnectArea(self)
        connect_area = self.ui_components['connect_area']
        column_a_grid.addWidget(connect_area, 0, 0, 1, 1)
        # Motion control area:
        self.ui_components['motion_control'] = MotionControl(self)
        motion_control = self.ui_components['motion_control']
        column_a_grid.addWidget(motion_control, 1, 0, 1, 1)
        # Motion settings area:
        self.ui_components['motion_settings'] = MotionSettings(self)
        motion_settings = self.ui_components['motion_settings']
        column_a_grid.addWidget(motion_settings, 2, 0, 1, 1)
        # Program control:
        self.ui_components['program_control'] = ProgramControl(self)
        program_control = self.ui_components['program_control']
        column_a_grid.addWidget(program_control, 3, 0, 1, 1)

        # Second column ...
        self.ui_components['column_b'] = FrameColumn(self)
        column_b = self.ui_components['column_b']
        main_grid.addWidget(column_b, 0, 1, 1, 1)
        column_b_grid = column_b.properties['grid']
        column_b_grid.setAlignment(Qt.AlignTop)
        # Status area:
        self.ui_components['status_area'] = StatusArea(self)
        status_area = self.ui_components['status_area']
        column_b_grid.addWidget(status_area, 0, 0, 1, 1)

        # Third column ...
        self.ui_components['column_c'] = FrameColumn(self)
        column_c = self.ui_components['column_c']
        main_grid.addWidget(column_c, 0, 2, 1, 1)
        column_c_grid = column_c.properties['grid']
        column_c_grid.setAlignment(Qt.AlignTop)
        # Exit area:
        self.ui_components['exit_area'] = ExitArea(self)
        exit_area = self.ui_components['exit_area']
        column_c_grid.addWidget(exit_area, 0, 0, 1, 1)
        # Instrument area:
        self.ui_components['instrument_area'] = InstrumentArea(self)
        instrument_area = self.ui_components['instrument_area']
        column_c_grid.addWidget(instrument_area, 1, 0, 1, 1)
        # Log area:
        self.ui_components['log_area'] = LogArea(self)
        log_area = self.ui_components['log_area']
        column_c_grid.addWidget(log_area, 2, 0, 1, 1)

        # Signals ... logging signal:
        self._log_message.connect(self.__log_message)
        # Log file setting signal:
        self._set_log_file.connect(self.set_log_file)
        # Alert displaying signal:
        self._display_alert.connect(self.display_alert)

        # Configuration settings window:
        self.config_window = ConfigWindow(self)

        # Program settings window:
        self.program_window = ProgramWindow(self)

        # Init buttons:
        self.init_buttons()

        # Init threads:
        self.init_threads()

        # Display the application:
        self.show()
