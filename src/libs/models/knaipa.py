import logging

from google.appengine.ext import db

class (db.Model):
    """ Describes data model for storing articles """

    # TODO: following property should be replaced by reference
    knaipa = db.StringProperty(required=True)
    title = db.StringProperty(required=True)
    description = db.StringProperty(required=True)
    cut = db.StringProperty(required=True)
    text = db.TextProperty(required=True)
    #author = db.ReferenceProperty(required=True)
    modified = db.DateTimeProperty(auto_now=True)
