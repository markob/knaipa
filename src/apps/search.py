""" Current file contains functionality to handle search requests from user. """

import logging as log

# app engine imports
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

# whoosh library have to be added to system path before using
import os, sys
sys.path.append(os.path.abspath(os.curdir) + '/../libs')

from libs.search import search_query

class SearchHandler(webapp.RequestHandler):
    """Handles search request by using full text search functionality"""
    
    def get(self):
        """Processes search request and retrieves results"""
        
        result = search_query(self.request.get("query"))
        
        # analyse results here
        return self.response.out.write(result)


application = webapp.WSGIApplication([('/search', SearchHandler)], debug=True)


def main():
    run_wsgi_app(application)


if __name__ == "__main__":
    log.basicConfig(level=log.DEBUG)
    main()
