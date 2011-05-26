from google.appengine.ext import db
from knajpa.models.articles import Article

class Knajpa(db.Model):
    name = db.StringProperty(required=True)
    dateOfCreate = db.DateTimeProperty(required=True)
    dateOfUpdate = db.DateTimeProperty(required=True)
    
class Address(db.Model):
    knajpa = db.ReferenceProperty(Knajpa, collection_name='addresses')
    ia = db.FloatProperty(required=True)
    ja = db.FloatProperty(required=True)
    address = db.PostalAddressProperty(required=True)

class PhoneNumber(db.Model):
    knajpa = db.ReferenceProperty(Knajpa, collection_name='phonenumbers')
    phone_type = db.StringProperty()
    number = db.PhoneNumberProperty() 

class ArticleForKnajpa(db.Model):
    article = db.ReferenceProperty(Article, required=True, collection_name='articles')
    knajpa = db.ReferenceProperty(Knajpa, required=True, collection_name='knajpas')

#Content
class Group(db.Model):
    name = db.StringProperty(required=True)
    priority = db.IntegerProperty(default= -1L);
    knajpa = db.ReferenceProperty(Knajpa, collection_name='contentGroups')
    
class Item(db.Model):
    name = db.StringProperty(required=True)
    value = db.StringProperty(required=True)
    priority = db.IntegerProperty(default= -1L);
    group = db.ReferenceProperty(Group, collection_name='items')
