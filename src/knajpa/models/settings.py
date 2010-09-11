from google.appengine.ext import db
from google.appengine.ext.db import Expando

class Settings(Expando):
  """It's just a container to store dictionary like object with out indexing."""
  data = db.StringProperty(default=None)
