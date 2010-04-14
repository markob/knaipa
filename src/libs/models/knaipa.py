import logging

from google.appengine.ext import db

class Knaipa(db.Epando):
    """ Describes data model for storing information about knaipa. """

    name = db.StringProperty(required=True)
    category = db.CategoryProperty(required=True)
    location = db.GeoPtProperty(required=True)
    description = db.StringProperty(required=True)
    updated = db.DateTimeProperty(auto_now=True)