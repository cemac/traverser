#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Run the traverser GUI application
"""

# Standard library imports:
import sys
# Third party imports:
from PyQt5.QtWidgets import QApplication
# Package imports:
from traverser.ui import TraverserUI

def main():
    """
    Create the Qt application and run.
    """
    # Create application:
    TRAVERSER_APP = QApplication(sys.argv)
    # Create UI:
    TRAVERSER_UI = TraverserUI()
    # Exec-ing the app this way should make sure the appropriate exit code is
    # returned:
    sys.exit(TRAVERSER_APP.exec_())

if __name__ == '__main__':
    main()
