import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from libs.models.knaipa import Knaipa
from libs.objhandler import ObjectHandler
from libs.utils import InvalidRequestError


class KnaipaHandler(webapp.RequestHandler):
    """ Adapts knaipa info and stores it to data storage. """

    def __init__(self):
        ObjectHandler.__init__(self, Knaipa)
        

    def _get_cmd_handler(self):
        """ Selects appropriate handler for the requested command. """

        cmd = self.request.get('cmd')
        
        if 'post' == cmd:
            return (self._write, 'knaipa-post.xml')
        elif 'get' == cmd:
            return (self._read, 'knaipa-get.xml')
        elif 'list' == cmd:
            return (self._get_list, 'knaipa-list.xml')
        else:
            raise(InvalidRequestError('invalid command requested'))

    
    
application = webapp.WSGIApplication(
    [('/knaipa', KnaipaHandler)], debug = True)
        
        
def main():
    run_wsgi_app(application)

        
if __name__ == '__main__':
    main()
