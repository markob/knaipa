"""The file contains functionality to setup and generate search engine indices."""

import logging as log

from models.imodels import DocumentsQueue, BaseDocument

# whoosh imports
from whoosh.fields import Schema, TEXT, ID
from whoosh.index import getdatastoreindex
from whoosh.qparser import QueryParser


DOCUMENTS_SCHEMA = Schema(title=TEXT(stored=True),
                          id=ID(stored=True),
                          content=TEXT(stored=True))
    

def search_query(str):
    """Launches search through indexes and returns result"""
    log.debug("Search request is processing.")
    
    index = getdatastoreindex("knajpa", schema=DOCUMENTS_SCHEMA)
    parser = QueryParser("content", schema=index.schema)
    query = parser.parse(str)
    results = index.searcher().search(query)
        
    # log results
    log.debug("search results are %s" % results)
    
    
def add_docs_to_index():
  """It's temporary decision and have to be moved to task scheduler"""
  # check unindexed documents queue
  queue = DocumentsQueue.get_instance()
  
  if queue.documents:
    # get index writer and index required documents
    index = getdatastoreindex("knajpa", schema=DOCUMENTS_SCHEMA)
    writer = index.writer()
    
    for key in queue.documents:
      log.debug("document with key %s is going to index" % key)
      
      # retrieve content of appropriate documents and write index it
      document = BaseDocument.get(key)
      
      writer.add_document(title=document.get_title(),
                          id=document.get_id(),
                          content=document.get_content())
      queue.documents.remove(key)
      
    writer.commit()
    queue.put()
