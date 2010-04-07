import logging

from google.appengine.ext import db

class Service(db.Expando):
    """ Describes data model for storing information about knaipa. """

    name = db.StringProperty(required=True)
    category = db.CategoryProperty(required=True)
    location = db.GeoPtProperty(required=True)
    description = db.StringProperty(required=True)
    added = db.DateTimeProperty(auto_now_add=True)
    updated = db.DateTimeProperty(auto_now=True)
