from google.appengine.ext import db
from knajpa.models.restaurant import Knajpa

'''
Created on Aug 29, 2010

@author: apetrenko
'''

class Image(db.Model):

    knajpa = db.ReferenceProperty(Knajpa, collection_name='images')
    url = db.StringProperty()
    alt = db.StringProperty()
