import logging

from google.appengine.ext import db

class Article(db.Model):
    """ Describes data model for storing articles """

    text = db.TextProperty(required=True)
    author = db.ReferenceProperty(required=True)
    created = db.DateTimeProperty(required=True, auto_now_add=True)


