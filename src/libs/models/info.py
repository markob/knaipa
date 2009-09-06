from google.appengine.ext import db
from google.appengine.ext.db import polymodel

from libs.utils import DataMapperUtils
from address import *

from xml.dom import minidom


class Knaipa(polymodel.PolyModel):
    name = db.StringProperty(required=True)
    phone = db.PhoneNumberProperty()
    date = db.DateProperty(auto_now=True)
    
    def getXML(self):
        xml = minidom.Document()
        
        root = xml.createElement('knaipa')
        xml.appendChild(root)

        node = DataMapperUtils.genStringNode(xml, self.name, 'name')
        root.appendChild(node)

        node = DataMapperUtils.genStringNode(xml, self.phone, 'phone')
        root.appendChild(node)
        
        node = DataMapperUtils.genDateNode(xml, self.date)
        root.appendChild(node)
        
        return xml.toxml('utf8')


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
