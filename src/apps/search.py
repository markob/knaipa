""" Current file contains functionality to handle search requests from user. """

# app engine imports
from google.appengine.ext import webapp

from common import main, set_system_path
set_system_path()

from libs.indexing import search_query

class SearchHandler(webapp.RequestHandler):
    """Handles search request by using full text search functionality"""
    
    def get(self):
        """Processes search request and retrieves results"""
        
        result = search_query(self.request.get("query"))
        
        # analyse results here
        return self.response.out.write(result)


application = webapp.WSGIApplication([('/search', SearchHandler)], debug=True)


if __name__ == "__main__":
    main(application)
