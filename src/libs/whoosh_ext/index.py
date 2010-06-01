"""GAE storage index file mapper. It is used to store whoosh index file in GAE storage."""

import logging as logger
from google.appengine.ext import db

#TODO: current mapper is very stupid and can cause problems (file size, memory slow access).
class GAE_IndexFile(db.Model):
    """Maps index file structure to GAE storage."""
    # it's just a simple blob which contains appropriate data
    data = db.BlobProperty(required=True)

