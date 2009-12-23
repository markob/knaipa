import logging

from google.appengine.ext import db

class Image(db.Model):
    """ Describes data model for images which are storing
    separately from other information """

    data = db.BlobProperty(required=True)
    created = db.DateTimeProperty(required=True, auto_now_add=True)
    author = db.ReferenceProperty(required=True)
