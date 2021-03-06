"""The file contains functionality to setup and generate search engine indices."""

import logging as log

from knajpa.models.docsqueue import DocumentsQueue
from knajpa.models.documents import IndexableDocument
from knajpa.utils import update_lib_path
update_lib_path()

# whoosh imports
from whoosh.fields import Schema, TEXT, STORED
from whoosh.index import getdatastoreindex
from whoosh.qparser import MultifieldParser


DOCUMENTS_SCHEMA = Schema(id=STORED,
                          type=STORED,
                          title=TEXT(field_boost=2.0),
                          content=TEXT)

from knajpa.registry import Registry


class SearchEngine(object):
  
  @staticmethod
  def _compile_query(str, index):
    parser = MultifieldParser(["title", "content"], schema=index.schema)

    query_str = ""
    query_terms = str.split()
    try:
      query_str += query_terms.pop(0)
      while True:
        term = query_terms.pop(0)
        query_str += " OR "
        query_str += term
    except IndexError:
      log.debug("Query String: %s" % query_str)
      
    return parser.parse(query_str)

  
  @staticmethod
  def _get_config(config_name):
    """Reads appropriate configuration value from the Registry"""
    return Registry[config_name]
  
  
  @staticmethod
  def search_query(str):
    """Launches search through indexes and returns result"""
    log.debug("""Search request is processing. Search engine is looking for '%s'.""" % str)
    
    index = getdatastoreindex(SearchEngine._get_config('datastore'), schema=DOCUMENTS_SCHEMA)
    query = SearchEngine._compile_query(str, index)
    results = index.searcher().search(query)
    
    found_count = results.scored_length()
    log.debug("Search results: was found %d documents:" % found_count)
    
    for document in results:
      log.debug(" * %s" % document['id'])
    
    # get found documents ids and return as the result 
    docs_found = [{'id': document['id'], 'type': document['type']} for document in results]
    
    return docs_found
    
  
  @staticmethod  
  def add_docs_to_index():
    """It's temporary decision and have to be moved to task scheduler"""
    # check unindexed documents queue
    queue = DocumentsQueue.get_instance()
    
    if queue.documents:
      # get index writer and index required documents
      index = getdatastoreindex("knajpa", schema=DOCUMENTS_SCHEMA)
      writer = index.writer()
    
    while True:
      try:
        doc_id = queue.documents.pop()
        log.debug("document with id %d is going to index" % doc_id)
        
        # retrieve content of appropriate documents and write index it
        document = IndexableDocument.get_by_id(doc_id)
        writer.add_document(id=document.get_id(),
                            title=document.get_title(),
                            type=unicode(document.class_name()),
                            content=document.get_content())
        
        log.debug("remaining documents: %s" % queue.documents)
      except IndexError:
        break
      
    writer.commit()
    queue.put()

