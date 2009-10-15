from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from libs.models.info import Knaipa

class GetFullInfo(webapp.RequestHandler):
    """ This handler is responsible for insertion of a new item to the store. """
    
    def get(self):
        knaipa = Knaipa(name='Mess', phone='380634363925')
        
        self.response.headers["Content-Type"] = "text/xml"
        
        return self.response.out.write(knaipa.getXML())
    

application = webapp.WSGIApplication([('.*', GetFullInfo)], debug=True)

def main():
    run_wsgi_app(application)
    

if __name__ == '__main__':
    main()
