import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from knajpa.models.services import Service
from knajpa.handlers.objhandler import ObjectHandler
from knajpa.utils import InvalidRequestError


class ServiceHandler(ObjectHandler):
    """ Adapts service info and stores it to data storage. """

    def __init__(self):
        ObjectHandler.__init__(self, Service)
        

    def _select_cmd_handler(self):
        """ Selects appropriate handler for the requested command. """

        cmd = self.request.get('cmd')
        
        if 'post' == cmd:
            return (self._write, 'service-post.xml')
        elif 'get' == cmd:
            return (self._read, 'service-get.xml')
        elif 'list' == cmd:
            return (self._get_list, 'service-list.xml')
        else:
            raise(InvalidRequestError('invalid command requested'))

    
    
application = webapp.WSGIApplication(
    [('/services', ServiceHandler)], debug = True)
        
        
def main():
    run_wsgi_app(application)

        
if __name__ == '__main__':
    main()
