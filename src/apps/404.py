import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class NotFoundPage(webapp.RequestHandler):
    def get(self):
        
        self.response.out.write("Requested resource was not found.")


application = webapp.WSGIApplication([('.*', NotFoundPage)], debug=True)

def main():
    run_wsgi_app(application)
    

if __name__ == '__main__':
    main()