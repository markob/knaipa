import logging

from google.appengine.ext import webapp
from google.appengine.api import memcache

class Loginer(webapp.RequestHandler):
    """ Checks provided user auth info and makes it loggined. """

    def get(self, ):
        pass

    def post(self):
        pass
