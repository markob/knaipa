from google.appengine.ext import db


class Knaipa(db.Model):
    title = db.StringProperty(required=True)
    type = db.StringProperty(required=True, choices=set(['cafe',                                           'restaurant',
                                                         'cafeteria',
                                                         'pub']))
    
