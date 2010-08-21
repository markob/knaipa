import logger
from knajpa.handlers.objhandler import ObjectHandler
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from knajpa.models.restaurant import Knajpa
from knajpa.utils import main, InvalidRequestError, ModelProcessor
from google.appengine.datastore.datastore_index import prop_name

class KnajpaHandler(ObjectHandler):

    def __init__(self):
        ObjectHandler.__init__(self, Knajpa)
    
         # add cmd handlers
        self._cmd_handlers = { 'list'  : (self._get_list, 'restaurant/knajpa-list.xml'),
                               'add'   : (self._add, 'restaurant/knajpa-add.xml'),
                               'get'   : (self._read, 'restaurant/knajpa-get.xml'),
                               'error' : (lambda self: None, 'restaurant/knajpa-error.xml') }
        
    
    def _select_cmd_handler(self):
        """ Selects appropriate handler for the requested command. """

        cmd = self.request.get('cmd')

        try:
            return self._cmd_handlers[cmd]
        except KeyError:
            raise(InvalidRequestError('invalid command requested'))

     
    def _add(self):
        model_processor= ModelProcessor(self._data_model)
        model_processor._parse_request(self.request, True)
#        model_data = model_processor.gen_model_data(self._data_model)
        
        
        
        

application = webapp.WSGIApplication(
                [('/knajpa', KnajpaHandler)], debug=True)


def main():
    run_wsgi_app(application)


if __name__ == '__main__':
    main()
