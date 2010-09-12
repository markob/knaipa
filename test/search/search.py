"""This file contents several tests for search engine."""
import logging as log
import urllib2

APPSERVER_URL = "http://localhost:8080"


class AppEngineRemoteControl(object):
  """This class has abilities to send commands to application and handle responses from it."""
  
  def __init__(self, app_url):
    object.__init__(self)
    self._app_url = app_url
    
  def send_cmd(self, cmd, params):
    pass

def main():
  # change application mode to 'test'
  send_cmd(APPSERVER_URL, "")
