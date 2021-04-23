# -*- coding: utf-8 -*-
"""
Package Requirements:
  * PyQt5
  * PyQtChart
  * pySerial
"""

# stdlib imports:
import os
import re
# third party imports:
from setuptools import setup

# get the path separator:
PS = os.path.sep

# package name:
PACKAGE_NAME = 'traverser'

# get version from __init__.py:
VRE = re.compile(r'^APP_VERSION\s?=\s?.*$')
with open(PS.join([PACKAGE_NAME, '__init__.py'])) as f:
    for l in f:
        if VRE.match(l):
            PACKAGE_VERSION = l.strip().split()[-1].strip("'").strip('"')

setup(name=PACKAGE_NAME,
      version=PACKAGE_VERSION,
      author='CEMAC Support',
      author_email='cemac-support@leeds.ac.uk',
      url='',
      packages=[
          '{0}'.format(PACKAGE_NAME),
          '{0}.instruments'.format(PACKAGE_NAME),
          '{0}.ui_components'.format(PACKAGE_NAME),
          '{0}.ui_functions'.format(PACKAGE_NAME),
          '{0}.ui_threads'.format(PACKAGE_NAME),
      ])
