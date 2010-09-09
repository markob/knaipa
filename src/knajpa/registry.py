"""This file contains Registry to store all settings."""
import logging as log

import UserDict
from knajpa.models.settings import Settings
import pickle

class __Registry(UserDict):
  
  def dump(self):
    """Stores current registry content to datastore."""
    settings = Settings.all().get()
    settings.data = pickle.dumps(self.data, pickle.HIGHEST_PROTOCOL)
    settings.put()
    
    log.debug("Dumped Registry: %s" % self.data)

  
  def load(self):
    """Reads stored registry content from datastore to the registry"""
    settings = Settings.all().get()
    self.data = pickle.loads(settings.data)
    
    log.debug("Loaded Registry: %s" % self.data)
  

Registry = __Registry()
