import logging as log

from google.appengine.api import urlfetch
from knajpa.models.docsqueue import DocumentsQueue

from knajpa.configs import SettingsManager
DOCS_QUEUE_MAX_SIZE = SettingsManager['docs_to_index_queue_max_size']


def AddDocumentToIndexQueue(document):
  # add document to indexing queue
  docs_queue = DocumentsQueue.get_instance()
  docs_queue.documents.append(document.key().id())
  docs_queue.put()
  
  # initiate indexer if indexing queue size achieves threshold value
  log.debug("Index queue length is %d." % len(docs_queue.documents))
  if DOCS_QUEUE_MAX_SIZE <= len(docs_queue.documents):
    ActivateDocumentIndexer()



def ActivateDocumentIndexer():
  log.debug("Activate indexing service.")
  
  indexer_activation_url = SettingsManager['host_name'] + '/index'
  log.debug("Indexer Activation URL is '%s'" % indexer_activation_url)
  
  rpc = urlfetch.create_rpc(deadline=1)
  urlfetch.make_fetch_call(rpc, indexer_activation_url)

  # following code assumed that devserver launches application in debug mode      
  if __debug__:
    try:
      result = rpc.get_result()
      if result.status_code == 200:
        log.info("Indices were updated")
    except urlfetch.DownloadError:
      log.error("Indices were not updated")
