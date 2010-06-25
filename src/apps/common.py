"""Common API's for all applications"""
import logging as log
from google.appengine.ext.webapp.util import run_wsgi_app

def main(application):
  """Just launch appropriate application"""
  # set logger level
  log.getLogger().setLevel(log.DEBUG)
  # run application
  run_wsgi_app(application)


def set_system_path():
  """Updates system path with application modules"""
  # Add libs to system path
  import os, sys
  sys.path.append(os.curdir)
  sys.path.append(os.curdir + '/../libs')
