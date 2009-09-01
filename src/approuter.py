import logging

# add application path to the modules path
import sys, os
sys.path.insert(0, os.path.abspath('.'))

# import some utilities
from libs.utils import genLazyClassLoaderProxy as getHandler

# app engine modules import
from google.appengine.ext.webapp import WSGIApplication
from google.appengine.ext.webapp.util import run_wsgi_app

from google.appengine.ext import webapp

class TestPage(webapp.RequestHandler):
    def get(self):
        
        self.response.out.write("Test handler was done.")

# application main routing table
routingTable = [('/search(?:/(.*))?', getHandler('SearchProcessor', 'apps.search')),
                ('/test/?', TestPage),
                ('.*', getHandler('Page404', 'apps.404'))]
application = WSGIApplication(routingTable, debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
else:
    logging.debug('Uncovered use case was reached.')
