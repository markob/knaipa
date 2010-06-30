import logging as log

import common
common.set_system_path()

from google.appengine.ext import webapp
from indexing import add_docs_to_index #@UnresolvedImport

from common import main


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
