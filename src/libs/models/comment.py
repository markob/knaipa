from google.appengine.ext import db

from libs.utils import DataMapperUtils
from xml.dom import minidom

class Comment(db.Model):
    """ Entity of this type contents comment to article. """
    text = db.TextProperty(required=True)
    author = db.ReferenceProperty(required=True)
    article = db.ReferenceProperty(required=True)
    posted = db.DateTimeProperty(required=True)

    def getXML(self):
        xmlDoc = minidom.Document()
        
        return xmlDoc
