import logging as log

from google.appengine.ext import db
from google.appengine.ext.db.polymodel import PolyModel

from google.appengine.api import urlfetch

# todo: this params have to be configurable through settings
DOCS_QUEUE_THRESHOLD = 1
#INDEXER_URL = 'http://www.knajpa.com.ua/index'
INDEXER_URL = 'http://127.0.0.1:8080/index'

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
    
    # add document to indexing queue
    docs_queue = DocumentsQueue.get_instance()
    docs_queue.documents.append(self.key().id())
    docs_queue.put()
    
    # initiate indexer if indexing queue size achieves threshold value
    log.debug("Index queue length is %d." % len(docs_queue.documents))
    if DOCS_QUEUE_THRESHOLD <= len(docs_queue.documents):
      log.debug("Activate indexing service.")
      rpc = urlfetch.create_rpc(deadline=1)
      urlfetch.make_fetch_call(rpc, INDEXER_URL)
      
      # uncomment following piece of code for local development
      try:
        result = rpc.get_result()
        if result.status_code == 200:
          log.info("Indices were updated")
      except urlfetch.DownloadError:
        log.error("Indices were not updated")
    
    log.debug("document has been added to the index queue")
    log.debug(self.class_key())
    

class DocumentsQueue(db.Model):
  """Contains only links to documents which should be processed"""
  documents = db.ListProperty(int, default=None)
  
  @staticmethod
  def get_instance():
    """Retrieves the documents queue instance"""
    instance = DocumentsQueue.all().get()
    
    if not instance:
      # create documents queue instance if it does not exist
      instance = DocumentsQueue()
      instance.put()
      
    return instance
