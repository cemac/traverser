# -*- coding: utf-8 -*-
"""
traverser instruments init
"""

# Standard lib imports:
import glob
import importlib
import os

# Dict for storing instrument information:
INSTRUMENTS = {
    'instruments_dir': os.path.dirname(__file__),
    'instruments': []
}

# Init temporary variables:
I = None
FILE_NAME = None
MOD_NAME = None
MOD_CLASS = None

# Loop through file in instruments directory:
for I in glob.glob(os.sep.join([INSTRUMENTS['instruments_dir'], '*.py'])):
    # Get file name:
    FILE_NAME = os.path.basename(I)
    # Skip these files:
    if FILE_NAME in ['instrument.py', '__init__.py']:
        continue
    # Full module name:
    MOD_NAME = '.'.join(
        ['traverser', 'instruments', FILE_NAME.split('.py')[0]]
    )
    # Try to get the TraverserInstrument class:
    try:
        MOD_CLASS = importlib.import_module(MOD_NAME).TraverserInstrument
    except NameError:
        continue
    # Store the instrument information:
    INSTRUMENTS['instruments'].append({
        'name': MOD_CLASS().get_name(),
        'class': MOD_CLASS
    })

# Clear temporary variables:
del(I, FILE_NAME, MOD_NAME, MOD_CLASS)
