# -*- coding: utf-8 -*-
"""
Traverser ui main frame column
"""

# Package imports:
from traverser.ui_components.ui_component import UIComponent

class FrameColumn(UIComponent):
    """
    Column for for traverser UI main frame
    Creates a single column
    """
    def __init__(self, ui):
        # Run parent init first:
        super().__init__(ui, 1, main_frame=False, show_frame=False)
