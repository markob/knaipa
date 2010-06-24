"""This file contains configs are common for all applications"""

# Add libs to system path
import os, sys
sys.path.append(os.curdir + '/../libs')

# set logger to 'debug' mode
import logging as log
log.basicConfig(level=log.DEBUG)
