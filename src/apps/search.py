""" Current file contains functionality to handle search requests from user. """

import logging as log

# app engine imports
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

# whoosh library have to be added to system path before using
import os, sys
sys.path.append(os.path.abspath(os.curdir) + '/../libs')

# whoosh imports
from whoosh.fields import Schema, TEXT
from whoosh.index import getdatastoreindex
from whoosh.qparser import QueryParser


SCHEMA_ARTICLES = Schema(content=TEXT(stored=True))


class DocumentsQueue(db.Model):
    """Contains only links to documents which should be processed"""
    uri = db.URLProperty(required=True)


class SearchHandler(webapp.RequestHandler):
    """Handles search request by using full text search functionality"""
    
    def get(self):
        """"""
        log.debug("processing search request")
            
        index = getdatastoreindex("articles", schema=SCHEMA_ARTICLES)
        parser = QueryParser("content", schema=index.schema)
        query = parser.parse(self.request.get("query"))
        results = index.searcher().search(query)
        
        # log results
        log.debug("search results are %s" % results)
        
        # analyse results here
        return self.response.out.write("<item>Founded 0 objects</item>")


class IndexProcessor(object):
    """Processes requests of indexing operations"""
    
    def add_doc_to_index(self):
        """Just stores document uri to queue and it will be processed by scheduler"""
        doc_uri = DocumentsQueue(self.request.get('uri'))
        doc_uri.put()
        
        return self.response.out.write("")
    
    
    def exec_add_docs_to_index(self):
        """It's temporary decision and have to be moved to task scheduler"""
        # check unindexed documents queue
        docs_in_queue = DocumentsQueue.all()
        docs_uri = docs_in_queue.get()
        
        if None != docs_uri:
            # get index writer and index required documents
            index = getdatastoreindex("articles", schema=SCHEMA_ARTICLES)
            writer = index.writer()
            
            for doc_uri in docs_uri:
                # retrieve content of appropriate documents and write index it
                writer.add_document(content=doc_uri)
                writer.commit()
    

application = webapp.WSGIApplication([('/search', SearchHandler)], debug=True)


def main():
    run_wsgi_app(application)


if __name__ == "__main__":
    log.basicConfig(level=log.DEBUG)
    main()
