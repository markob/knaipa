import logging as log

from google.appengine.ext import webapp
from knajpa.utils import main

from knajpa.search.api import SearchEngine


class IndexRequestHandler(webapp.RequestHandler):
    """Processes document indexer requests"""
    
    def get(self):
        """Checks documents in the indexer queue and index if exists"""
        log.debug("document index request")
        
        SearchEngine.add_docs_to_index()
        
        self.response.set_status(200)
        self.response.out.write("")


application = webapp.WSGIApplication([('/index', IndexRequestHandler)], debug = True)

if __name__ == '__main__':
    main(application)
