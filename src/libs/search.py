""" The file contains functionality to setup and generate search engine indices. """

import logging as log

from libs.models.imodels import DocumentsQueue

# whoosh imports
from whoosh.fields import Schema, TEXT, ID
from whoosh.index import getdatastoreindex
from whoosh.qparser import QueryParser


DOCUMENTS_SCHEMA = Schema(title=TEXT(stored=True),
                          id=ID(stored=True),
                          content=TEXT(stored=True))
    

def search_query(str):
    """"""
    log.debug("Search request is processing.")
    
    index = getdatastoreindex("articles", schema=DOCUMENTS_SCHEMA)
    parser = QueryParser("content", schema=index.schema)
    query = parser.parse(str)
    results = index.searcher().search(query)
        
    # log results
    log.debug("search results are %s" % results)
    
    
def exec_add_docs_to_index():
    """It's temporary decision and have to be moved to task scheduler"""
    # check unindexed documents queue
    query = DocumentsQueue.all()
    # NOTE: here is used fetch without params because it's suspected that
    # there always will be just few documents in the queue
    docs_to_index = query.fetch()
        
    if None != docs_to_index:
        # get index writer and index required documents
        index = getdatastoreindex("articles", schema=DOCUMENTS_SCHEMA)
        writer = index.writer()
            
        for doc in docs_to_index:
            # retrieve content of appropriate documents and write index it
            writer.add_document(title=doc.document.get_title(),
                                id=doc.document.get_id(),
                                content=doc.document.get_content())
            
        writer.commit()
