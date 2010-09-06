""" Current file contains functionality to handle search requests from user. """

import logging as log

# app engine imports
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from knajpa.utils import main
from knajpa.search.indexer import search_query

import os
TEMPLATE_PATH = os.path.dirname(__file__) + "/../../../webapp/templates/search/search-results.xml"

class SearchHandler(webapp.RequestHandler):
    """Handles search request by using full text search functionality"""
    
    def get(self):
        """Processes search request and retrieves results"""
        log.debug("Search request: %s" % self.request.url)
        
        results = search_query(self.request.get("query"))
        
        self.response.headers['Content-Type'] = 'text/xml'
        return self.response.out.write(template.render(TEMPLATE_PATH, {'documents': results}))


application = webapp.WSGIApplication([('/search', SearchHandler)], debug=True)


if __name__ == "__main__":
    main(application)
