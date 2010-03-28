import logging

from google.appengine.ext import db

from libs.models.services import Service
from libs.uzvers import Uzver

class Article(db.Model):
    """ Describes data model for storing articles """
    
    services = db.ListProperty(Reference, required=True)
    title = db.StringProperty(required=True)
    description = db.StringProperty(required=True)
    cut = db.StringProperty(required=True)
    text = db.TextProperty(required=True)
    author = db.ReferenceProperty(Uzver, required=True)
    modified = db.DateTimeProperty(auto_now=True)


