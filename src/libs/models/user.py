import logging

from google.appengine.ext import db

class User(db.Model):
    """ Contains base user information as name, login,
    time of account creation, password hash etc. """

    login = db.StringProperty(required=True)
    passwd = db.ByteStringProperty(required=True)
    name = db.StringProperty()
    created = db.DateTimeProperty(required=True, auto_now_add=True)
