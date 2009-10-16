from google.appengine.ext import db

class PersonInfo(db.Model):
    """ This model contains general information about person. """

    # All essential data about a person
    firstName = db.StringProperty(required=True) # first name of the person
    secondName = db.StringProperty(required=True) # second name of the person
    nickName = db.StringProperty(required=True) # nickname used as username
    bornDate = db.DateProperty(required=True) # date when a person was born
    sex = db.StringProperty(required=True, choices=set(["male", "female", "undefined"]))

    # Other (optional) data about a person
    avatar = db.BlobProperty()
    mobilePhone = db.PhoneNumberProperty()
    landPhone = db.PhoneNumberProperty()
    address = db.PostalAddressProperty()
