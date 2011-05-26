from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from knajpa.handlers.objhandler import ResourceNotExist
from knajpa.services.db.restaurant import KnajpaService, KnajpaItem, GroupContent
from knajpa.utils import main, InvalidRequestError
import logging
import os
import re
from knajpa.registry import Registry



templates_path = os.path.join(os.path.dirname(__file__), '../../../', 'webapp/templates')
logging.debug("Templates path: " + templates_path)

class KnajpaHandler(webapp.RequestHandler):
   
    _cmd_handlers = { }
    
    def get(self):
        self._update_info()
        return self._handle_request()
    
    def post(self):
        self._update_info()
        return self._handle_request()
    
    def __init__(self):
        self._cmd_handlers = { 'list'  : (self._get_list, 'restaurant/knajpa-list.xml'),
                               'add'   : (self._write, 'restaurant/knajpa-add.xml'),
                               'get'   : (self._read, 'restaurant/knajpa-get.xml'),
                               'error' : (lambda self: None, 'restaurant/knajpa-error.xml') }
        
    
    def _select_cmd_handler(self):
        """ Selects appropriate handler for the requested command. """

        cmd = self.request.get('cmd')
        logging.debug('I am in handling request')
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
     
     
    def _write(self, request):
        knajpaitem = self._create_knajpaItem_from_request(request)
        return {'id': KnajpaService.update_knajpa(knajpaitem)} 
        
    def _get_list(self, request):
        logging.debug('I am getting list')
        list_of_knajp = KnajpaService.get_knajpa_list(100, 0)
        return {'list': list_of_knajp, 'count': KnajpaService.count_knajpa()} 
                  
        
    def _read(self, request):
        logging.debug('I am reading')
        id = request.get('id')
        if not id:
            raise(ResourceNotExist('Invalid instance id requested'))
        
        return {'knajpa': KnajpaService.get_knajpa(long(id))} 



    def _create_knajpaItem_from_request(self, request):
        id = request.get('id')
        title = request.get('title')
        address = request.get('address')
        ia = request.get('ia')
        ja = request.get('ja')

        logging.info('I am adding new knajpa with name %s', title)
        knajpaitem = KnajpaItem(title)
        if(re.match ("^[0-9]+$", id) != None and long(id) > 0):
                knajpaitem.id = long(id)
                
        knajpaitem.add_address(address, float(ia), float(ja))

        group_item_names = self._get_map_group_item_names(request)
        for key in  group_item_names:
            group = key
            items = group_item_names[key]
            
            group_name = request.get(group)
            group_id = self._get_from_request(request, group + '_id', -1L)
            group_content = GroupContent(group_name, long(group_id))  
            
            for item in items:
                item_id = self._get_from_request(request, item + '_id', -1L)
                item_name = request.get(item + '_name')
                item_value = request.get(item + '_value')
                group_content.add_content_item(item_name, item_value, long(item_id))
            
            knajpaitem.add_group(group_content)
            
        return   knajpaitem
    
    
    def _get_from_request(self, request, param, default_value):
        value = request.get(param)
        if((value == None)or(value != None and len(value) == 0)):
            value = default_value
        return value   
        
    def _get_map_group_item_names(self, request):
        list_attr = request.arguments()
        logging.debug("list_attr:" + str(list_attr))        
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
                    group_item_names[g_name] = [i_name, ]
                    
        logging.debug("group_itme:" + str(group_item_names))           
        return group_item_names


    def _update_info(self):
        """ Updates request related information in Settings Manager. """
        host_url_end_index = self.request.url.rfind(self.request.path)
        
        # host_url_end_index 
        if 0 == host_url_end_index:
          raise(InvalidRequestError)
        
        Registry['host_name'] = self.request.url[0:host_url_end_index]
        logging.debug("Host URL is '%s'" % Registry['host_name'])



application = webapp.WSGIApplication(
                [('/knajpa', KnajpaHandler)], debug=True)


def main():
    run_wsgi_app(application)


if __name__ == '__main__':
    main()
