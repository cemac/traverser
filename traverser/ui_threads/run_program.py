# -*- coding: utf-8 -*-
"""
Program running thread
"""

# Standard lib imports:
import time
# Third party imports:
from PyQt5.QtCore import QThread, pyqtSignal
# Package imports:
from traverser.ui_functions.program_functions import run_it

class RunProgram(QThread):
    """
    Qthread class used for stopping VixIM motion
    """
    # Define signal to unlock vixim lock:
    release_lock = pyqtSignal()

    def __init__(self, ui, poll_int=0.2):
        # Qthread init:
        QThread.__init__(self)
        # Store self properties ... ui:
        self.ui = ui
        # Polling interval:
        self.poll_int = poll_int
        # When this is true motion will be started:
        self.__start = False
        # Whether this thread has the vixim lock:
        self.has_lock = False
        # Connect lock releasing signal to function:
        self.release_lock.connect(self.__release_lock)

    def __release_lock(self):
        """
        Release the vixim lock
        """
        # Check if lock flag is set, and if so, release it:
        if self.has_lock is True:
            self.ui.vixim_lock.unlock()
            self.has_lock = False

    def start_it(self):
        """
        Set start flag to True
        """
        self.__start = True

    def stop_it(self):
        """
        Set start flag to False
        """
        self.__start = False

    def run(self):
        """
        Run / loop forever, checking for start signal
        """
        while True:
            # If start flag is True:
            if self.__start is True:
                # Start the program:
                run_it(self, self.ui)
                # Reset the flag:
                self.stop_it()
            time.sleep(self.poll_int)
