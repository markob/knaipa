from google.appengine.ext import db
from google.appengine.ext.db import polymodel


class Address(polymodel.PolyModel):
    city = db.StringProperty(required=True)
    street = db.StringProperty(required=True)
    buildingNumber = db.IntegerProperty(required=True)


class Contact(Address):
    name = db.StringProperty(required=True)
    surname = db.StringProperty()
    nickname = db.StringProperty(required=True)
    phone = db.PhoneNumberProperty()
    mobile = db.PhoneNumberProperty()
    birth = db.DateProperty()


class Company(Address):
    name = db.StringProperty(required=True)
    phone = db.PhoneNumberProperty()
    fax = db.PhoneNumberProperty()
