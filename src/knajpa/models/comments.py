import logging

from google.appengine.ext import db

from articles import Article
from uzvers import Uzver

class Comment(db.Model):
    """ Describes data model for storing articles """
    
    article = db.ReferenceProperty(Article, required=True)
    author = db.ReferenceProperty(Uzver, required=True)
    created = db.DateTimeProperty(auto_now=True)
    title = db.StringProperty(required=True)
    text = db.TextProperty(required=True)
