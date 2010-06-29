import logging as log

from google.appengine.ext import db
from google.appengine.ext.db.polymodel import PolyModel


class BaseDocument(PolyModel):
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
        log.debug("document id has been requested")
        return self.key().id_or_name()
    
    def put(self):
        """Stores the document and adds it id to the index queue"""
        PolyModel.put(self)
        log.debug("document has been added to the storage with id %s" % self.get_id())
        
        doc_to_index = DocumentsQueue(self.key())
        doc_to_index.put()
        log.debug("document has been added to the index queue")


class DocumentsQueue(db.Model):
    """Contains only links to documents which should be processed"""
    document = db.ListProperty(db.Key, required=True)
