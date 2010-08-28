from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from knajpa.handlers.objhandler import ResourceNotExist
from knajpa.services.db.restaurant import KnajpaService, KnajpaItem, \
    GroupContent
from knajpa.utils import main, InvalidRequestError
import logging
import os
import re

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
        knajpaitem = self._create_knajpaItem_from_request(request)
        return {'id': KnajpaService.create_new_knajpa(knajpaitem)} 
        
    def _get_list(self, request):
        logging.info('I am getting list')
        list_of_knajp = KnajpaService.get_knajpa_list(100, 0)
        return {'list': list_of_knajp, 'count':KnajpaService.count_knajpa()} 
                  
        
    def _read(self, request):
        logging.info('I am reading')
        pass   



    def _create_knajpaItem_from_request(self, request):
        title = request.get('title')
        address = request.get('address')
        ia = request.get('ia')
        ja = request.get('ja')

        
        group_item_names = self._get_map_group_item_names(request)
        
        logging.info('I am adding new knajpa with name %s', title)
        knajpaitem = KnajpaItem(title)
        knajpaitem.add_address(address, float(ia), float(ja))

        for key in  group_item_names:
            group = key
            items = group_item_names[key]
            
            group_name = request.get(group)
            group_content = GroupContent(name=group_name)  
            
            for item in items:
                item_name = request.get(item + '_name')
                item_value = request.get(item + '_value')
                group_content.add_content_item(item_name, item_value)
            
            knajpaitem.add_group(group_content)
            
        return   knajpaitem
        
        
    def _get_map_group_item_names(self, request):
        list_attr = request.arguments()
        group_item_names = {}
        for attr_name in list_attr:
            m = re.match("((g[0-9]{1,})_item[0-9]{1,})_name", attr_name)
            if m != None:
                i_name = m.group(1)
                g_name = m.group(2)
                if g_name in group_item_names:
                    
                    item_names = group_item_names[g_name]
                    item_names.append(i_name)
                else:
                    group_item_names[g_name] = []
                    
        return group_item_names


application = webapp.WSGIApplication(
                [('/knajpa', KnajpaHandler)], debug=True)


def main():
    run_wsgi_app(application)


if __name__ == '__main__':
    main()
