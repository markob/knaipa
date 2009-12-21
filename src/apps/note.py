from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from google.appengine.ext import db
from libs.models.knaipa import Knaipa

class NewItem(webapp.RequestHandler):
    """ This handler is responsible for insertion of a new item to the store. """
    
    def get(self):
        return self.response.out.write("Add new item to the storage.")
    

class EditItem(webapp.RequestHandler):
    """ This handler is responsible for existing item editing """
    
    def get(self, item):
        # try to find and load existing item from storage
        ##itemData = Knaipa.
        
        ##itemData.
        
        return self.response.out.write("Edit the existing item.")
    
    def post(self, item):
        pass
    

application = webapp.WSGIApplication([('new', NewItem),
                                      ('edit/item=(.*)', EditItem),
                                      ('delete/item=(.*)', DeleteItem)],
                                     debug=True)

def main():
    run_wsgi_app(application)
    

if __name__ == '__main__':
    main()
