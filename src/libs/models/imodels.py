import logging as log
from google.appengine.ext import db

class BaseDocument(db.Model):
    """It's interface class for all indexable document models"""
    
    def get_title(self):
        """Overridden descendant have to return a document title here"""
        log.warning("It's interface method and have to be overridden in descendants.")
        raise NotImplementedError

    def get_content(self):
        """Overridden descendant have to return a document content here"""
        log.warning("It's interface method and have to be overridden in descendants.")
        raise NotImplementedError
    
    def get_id(self):
        """Retrieves the document instance id if it exists"""
        if not self.is_saved():
            return None
        else:
            return self.key().id_or_name()
