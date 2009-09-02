from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app


class SearchProcessor(webapp.RequestHandler):
    def get(self, query=''):
        
        self.response.out.write("query string is \"%s\"." % query)
    

application = webapp.WSGIApplication([('.*', SearchProcessor)], debug=True)

def main():
    run_wsgi_app(application)
    

if __name__ == '__main__':
    main()
