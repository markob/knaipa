import logging as log

from google.appengine.ext import db
from imodels import  BaseDocument


class Article(BaseDocument):
    """ Describes data model for storing articles """
    
    #services = db.ListProperty(db.Key, required=True)
    title = db.StringProperty(required=True)
    description = db.StringProperty(required=True)
    cut = db.StringProperty(required=True)
    text = db.TextProperty(required=True)
    modified = db.DateTimeProperty(auto_now=True)
    
    def get_title(self):
        """Retrieves only title of an article"""
        log.debug("Article title is %s" % self.title)
        return self.title
    
    def get_content(self):
        """Retrieves only text content of an article"""
        log.debug("Article content is %s" % self.text)
        return self.text
