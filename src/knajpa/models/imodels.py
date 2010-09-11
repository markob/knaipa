import logging as log

from google.appengine.ext.db.polymodel import PolyModel

from knajpa.search.utils import AddDocumentToIndexQueue


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
    return unicode(self.key().id_or_name())
  
  def put(self):
    """Stores the document and adds it id to the index queue"""
    super(BaseDocument, self).put()
    log.debug("document has been added to the storage with id %d" % self.key().id())
    
    AddDocumentToIndexQueue(self)
        
    log.debug("document has been added to the index queue")
    log.debug(self.class_key())
