""" Current file contains functionality to handle search requests from user. """

import logging as log

# app engine imports
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

# whoosh library have to be added to system path before using
import os, sys
sys.path.append(os.path.abspath(os.curdir) + '/../libs')

from libs.models.imodel import BaseIndexableModel

# whoosh imports
from whoosh.fields import Schema, TEXT, ID
from whoosh.index import getdatastoreindex
from whoosh.qparser import QueryParser


SCHEMA_DOCUMENTS = Schema(title=TEXT(stored=True),
                          id=ID(stored=True),
                          content=TEXT(stored=True))


class DocumentsQueue(db.Model):
    """Contains only links to documents which should be processed"""
    document = db.ReferenceProperty(BaseIndexableModel, required=True)


class SearchHandler(webapp.RequestHandler):
    """Handles search request by using full text search functionality"""
    
    def get(self):
        """"""
        log.debug("processing search request")
            
        index = getdatastoreindex("articles", schema=SCHEMA_DOCUMENTS)
        parser = QueryParser("content", schema=index.schema)
        query = parser.parse(self.request.get("query"))
        results = index.searcher().search(query)
        
        # log results
        log.debug("search results are %s" % results)
        
        # analyse results here
        return self.response.out.write("<item>Founded 0 objects</item>")


class IndexProcessor(object):
    """Processes requests of indexing operations"""
    
    def add_doc_to_index(self, doc):
        """Just stores document id to queue and it will be processed by scheduler"""
        doc_to_index = DocumentsQueue(doc)
        doc_to_index.put()
    
    
    def exec_add_docs_to_index(self):
        """It's temporary decision and have to be moved to task scheduler"""
        # check unindexed documents queue
        query = DocumentsQueue.all()
        # NOTE: here is used fetch without params because it's suspected that
        # there always will be just few documents in the queue
        docs_to_index = query.fetch()
        
        if None != docs_to_index:
            # get index writer and index required documents
            index = getdatastoreindex("articles", schema=SCHEMA_DOCUMENTS)
            writer = index.writer()
            
            for doc in docs_to_index:
                # retrieve content of appropriate documents and write index it
                writer.add_document(title=doc.document.get_title(),
                                    id=doc.document.get_id(),
                                    content=doc.document.get_content())
            
            writer.commit()


application = webapp.WSGIApplication([('/search', SearchHandler)], debug=True)


def main():
    run_wsgi_app(application)


if __name__ == "__main__":
    log.basicConfig(level=log.DEBUG)
    main()
