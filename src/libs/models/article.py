from google.appengine.ext import db

from xml.dom import minidom
from libs.utils import DataMapperUtils

class Article(db.Model):
    text = db.TextProperty(required=True) # text of the article
    author = db.ReferenceProperty(required=True) # reference to the author

    _items = ('text',)#, 'author')

    #def getXML(self):
    #    xmlDoc = minidom.Document()
    #    
    #    root = xmlDoc.createElement('data')
    #    xmlDoc.appendChild(root)

    #    node = DataMapperUtils.genXMLNode(xmlDoc, self.text, 'text')
    #    root.appendChild(node)
        
    #    return xmlDoc.toxml('utf8')
    
