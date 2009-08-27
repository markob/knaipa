import logging

from google.appengine.ext import webapp

class Page404(webapp.RequestHandler):
    def get(self):
        
        self.response.out.write("Requested resource was not found.")
