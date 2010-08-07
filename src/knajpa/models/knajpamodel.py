from google.appengine.ext import db

class Knajpa(db.Model):
    name = db.StringProperty(required=True)