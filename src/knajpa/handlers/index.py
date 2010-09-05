import logging as log

from google.appengine.ext import webapp
from knajpa.utils import main

from knajpa.search.indexer import add_docs_to_index


class IndexRequestHandler(webapp.RequestHandler):
    """Processes document indexer requests"""
    
    def get(self):
        """Checks documents in the indexer queue and index if exists"""
        log.debug("document index request")
        
        add_docs_to_index()
        
        self.response.set_status(200)


application = webapp.WSGIApplication([('/tasks/index', IndexRequestHandler)], debug = True)

if __name__ == '__main__':
    main(application)
