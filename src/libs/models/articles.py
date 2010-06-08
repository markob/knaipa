import logging as log

from google.appengine.ext import db

#from libs.uzvers import Uzver #@UnresolvedImport
from libs.models.imodel import BaseIndexableModel

class Article(BaseIndexableModel):
    """ Describes data model for storing articles """
    
    #services = db.ListProperty(db.Key, required=True)
    title = db.StringProperty(required=True)
    description = db.StringProperty(required=True)
    cut = db.StringProperty(required=True)
    text = db.TextProperty(required=True)
    #author = db.ReferenceProperty(Uzver, required=True)
    modified = db.DateTimeProperty(auto_now=True)
    
    def get_title(self):
        """Retrieves only title of an article"""
        log.debug("Article title is %d" % self.title)
        return self.title
    
    def get_content(self):
        """Retrieves only text content of an article"""
        log.debug("Article content is %d" % self.text)
        return self.text



