"""The file contains functionality to setup and generate search engine indices."""

import logging as log

from models.imodels import DocumentsQueue
from models.documents import IndexableDocument

# whoosh imports
from whoosh.fields import Schema, TEXT, ID
from whoosh.index import getdatastoreindex
from whoosh.qparser import QueryParser


DOCUMENTS_SCHEMA = Schema(id=ID(stored=True),
                          title=TEXT(stored=True),
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
    
    for doc_id in queue.documents:
      log.debug("document with id %d is going to index" % doc_id)
      
      # retrieve content of appropriate documents and write index it
      document = IndexableDocument.get_by_id(doc_id)
      
      writer.add_document(id=document.get_id(),
                          title=document.get_title(),
                          content=document.get_content())
      queue.documents.remove(doc_id)
      
    writer.commit()
    queue.put()
