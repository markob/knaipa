from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class GetFullInfo(webapp.RequestHandler):
    """ This handler is responsible for insertion of a new item to the store. """
    
    def get(self):
        return self.response.out.write("Here is item full info.")
    

application = webapp.WSGIApplication([('.*', GetFullInfo)], debug=True)

def main():
    run_wsgi_app(application)
    

if __name__ == '__main__':
    main()
