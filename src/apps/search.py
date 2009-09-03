import logging

from google.appengine.ext import webapp


class SearchProcessor(webapp.RequestHandler):
    def get(self, query=''):
        
        self.response.out.write("query string is \"%s\"." % query)
