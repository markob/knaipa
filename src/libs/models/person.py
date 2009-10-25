from google.appengine.ext import db

from xml.dom import minidom
from libs.utils import DataMapperUtils

class PersonInfo(db.Model):
    """ This model contains general information about person. """

    # All essential data about a person
    firstName = db.StringProperty(required=True) # first name of the person
    secondName = db.StringProperty(required=True) # second name of the person
    nickName = db.StringProperty(required=True) # nickname used as username
    bornDate = db.DateProperty(required=True) # date when a person was born
    sex = db.StringProperty(required=True, choices=set(['male', 'female', 'undefined']))

    # Other (optional) data about a person
    avatar = db.BlobProperty()
    mobilePhone = db.PhoneNumberProperty()
    landPhone = db.PhoneNumberProperty()
    address = db.PostalAddressProperty()

    _items = ('firstName', 'secondName', 'nickName', 'bornDate', 'sex',
              'avatar', 'mobilePhone', 'landPhone', 'address')

#    def getXML(self):
#        xmlDoc = minidom.Document()

#        root = xmlDoc.createElement('data')
#        xmlDoc.appendChild(root)

#        node = DataMapperUtils.genStringNode(xmlDoc, self.firstName, 'firstName')
#        root.appendChild(node)

#        node = DataMapperUtils.genStringNode(xmlDoc, self.secondName, 'secondName')
#        root.appendChild(node)

#        node = DataMapperUtils.genStringNode(xmlDoc, self.nickName, 'nickName')
#        root.appendChild(node)

#        node = DataMapperUtils.genDateNode(xmlDoc, self.bornDate, 'bornDate')
#        root.appendChild(node)

#        node = DataMapperUtils.genStringNode(xmlDoc, self.sex, 'sex')
#        root.appendChild(node)

#        return xmlDoc.toxml('utf8')
