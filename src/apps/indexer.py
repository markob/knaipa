import logging as log

from google.appengine.ext import webapp
from search import add_docs_to_index


class IndexRequestHandler(webapp.RequestHandler):
    """Processes document indexer requests"""
    
    def get(self):
        """Checks documents in the indexer queue and index if exists"""
        log.debug("document index request")
        
        add_docs_to_index()

application = webapp.WSGIApplication([('/index', IndexRequestHandler)], debug = True)

def main():
    webapp.util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
