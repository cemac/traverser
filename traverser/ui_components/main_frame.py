# -*- coding: utf-8 -*-
"""
Traverser UI main frame
"""

# Package imports:
from traverser.ui_components.ui_component import UIComponent

class MainFrame(UIComponent):
    """
    Main frame for traverser UI
    Creates a three column layout by default
    """
    def __init__(self, ui, ncols=3):
        # Run parent init first:
        super().__init__(ui, ncols, main_frame=True)
