from google.appengine.ext import db
from google.appengine.ext.db import polymodel

from address import *


class Knaipa(polymodel.PolyModel):
    title = db.StringProperty(required=True)
    


class Restaurant(Knaipa):
     pass


class Cafeteria(Knaipa):
    pass



class Cafe(Knaipa):
    pass


class Pub(Knaipa):
    pass


class Mess(Knaipa):
    pass
