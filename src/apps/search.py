""" Current file contains functionality to handle search requests from user. """

import logging as log

# app engine imports
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

# whoosh library have to be added to system path before using
import os, sys
sys.path.append(os.path.abspath(os.curdir) + '/../libs')

# whoosh imports
from whoosh.fields import Schema, TEXT
from whoosh.index import getdatastoreindex
from whoosh.qparser import QueryParser


SCHEMA_ARTICLES = Schema(content=TEXT(stored=True))


class SearchHandler(webapp.RequestHandler):
    """Handles search request by using full text search functionality"""
    
    def get(self):
        """"""
        log.debug("processing search request")
            
        index = getdatastoreindex("articles", schema=SCHEMA_ARTICLES)
        parser = QueryParser("content", index.schema)
        query = parser.parse(self.request.get("query"))
        results = index.searcher().search(query)
        
        # log results
        log.debug("search results are %s" % results)
        
        # analyse results here
        return self.response.out.write("<item>Founded 0 objects</item>")


    def put(self):
        """"""
        index = getdatastoreindex("articles", schema=SCHEMA_ARTICLES)
        writer = index.writer()
        writer.add_document(content=self.request.get("content"))
        writer.commit()
        
        self.redirect("/")


application = webapp.WSGIApplication([('/search', SearchHandler)], debug=True)


def main():
    run_wsgi_app(application)


if __name__ == "__main__":
    log.basicConfig(level=log.DEBUG)
    main()
