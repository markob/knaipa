from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from knajpa.handlers.objhandler import ResourceNotExist
from knajpa.services.db.restaurant import KnajpaService, KnajpaItem
from knajpa.utils import main, InvalidRequestError
import logging
import os

templates_path = os.path.join(os.path.dirname(__file__), '../../../', 'webapp/templates')
logging.info("Templates path: " + templates_path)

class KnajpaHandler(webapp.RequestHandler):
   
    _cmd_handlers = { }
    
    def get(self):
        return self._handle_request()
    
    def post(self):
        return self._handle_request()
    
    def __init__(self):
        self._cmd_handlers = { 'list'  : (self._get_list, 'restaurant/knajpa-list.xml'),
                               'add'   : (self._add, 'restaurant/knajpa-add.xml'),
                               'get'   : (self._read, 'restaurant/knajpa-get.xml'),
                               'error' : (lambda self: None, 'restaurant/knajpa-error.xml') }
        
    
    def _select_cmd_handler(self):
        """ Selects appropriate handler for the requested command. """

        cmd = self.request.get('cmd')
        logging.info('I am in handling request')
        try:
            return self._cmd_handlers[cmd]
        except KeyError:
            raise(InvalidRequestError('invalid command requested'))
        
    def _render_response(self, resp_data, template_name):
        """ Renders responce with the appropriate data and template """
        template_path = os.path.join(templates_path, template_name)

        self.response.headers['Content-Type'] = 'text/xml'
        return self.response.out.write(template.render(template_path, resp_data))
     
     
    def _handle_request(self):
        try:
            handler, template_name = self._select_cmd_handler()
            resp_data = handler(self.request)

            return self._render_response(resp_data, template_name)

        except InvalidRequestError, err:
            return self.response.out.write(err)
        except ResourceNotExist, err:
            return self.response.out.write(err)
     
     
     
     
    def _add(self, request):
        title = request.get('title')
        address = request.get('address')
        ia = request.get('ia')
        ja = request.get('ja')
        
        logging.info('I am adding new knajpa with name %s', title)
        knajpaitem = KnajpaItem(title)
        knajpaitem.add_address(address, float(ia), float(ja))
        
        return {'id': KnajpaService.create_new_knajpa(knajpaitem)} 
        
    def _get_list(self, request):
        logging.info('I am getting list')
        list_of_knajp = KnajpaService.get_knajpa_list(10, 0)
        return {'list': list_of_knajp, 'count':KnajpaService.count_knajpa()} 
                  
        
    def _read(self, request):
        logging.info('I am reading')
        pass   

application = webapp.WSGIApplication(
                [('/knajpa', KnajpaHandler)], debug=True)


def main():
    run_wsgi_app(application)


if __name__ == '__main__':
    main()
