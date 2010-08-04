import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from google.appengine.ext import db

from libs.utils import InvalidRequestError, ModelProcessor #@UnresolvedImport

import os

templates_path = os.path.join(os.path.dirname(__file__), '../templates')


# Object Handler Exception that means that the resource does not exist
class ResourceNotExist(Exception): pass


class ObjectHandler(webapp.RequestHandler):
    _cmd_handlers = { }
    
    def __init__(self, data_model):
        self._data_model = data_model


    def get(self):
        """ Just hooks all GET requests and passes it to processor. """
        
        return self._handle_request()


    def post(self):
        """ Just hooks all POST requests and passes it to processor. """

        return self._handle_request()


    def _render_response(self, resp_data, template_name):
        """ Renders responce with the appropriate data and template """
        template_path = os.path.join(templates_path, template_name)

        self.response.headers['Content-Type'] = 'text/xml'
        return self.response.out.write(template.render(template_path, resp_data))



    def _handle_request(self):
        """ Processes input request and creates appropriate reqponse. """
        try:
            handler, template_name = self._select_cmd_handler()
            resp_data = handler(self.request)

            return self._render_response(resp_data, template_name)

        except InvalidRequestError, err:
            return self.error(404)
        except ResourceNotExist, err:
            return self._render_response({'error': err}, self._cmd_handlers['error'][1])
        

    def _write(self, request):
        """ Parses request data and store instance object. """
    
        instance_id = request.get('id')
        processor = ModelProcessor(self._data_model)
        
        if instance_id:
            # get instance from datastore
            instance = self._get(instance_id)
            
            #update the instance
            processor.update_from_request(request, instance)
        else:
            # create new instance
            instance = processor.create_from_request(request)

        # save instance
        instance.put()
            
        return {'instance_id': instance.key().id()}


    def _read(self, request):
        """ Retrieves requested instance from datastore. """

        instance_id = request.get('id')

        if not instance_id:
            raise(ResourceNotExist('Invalid instance id requested'))

        instance = self._get(instance_id)
        
        return ModelProcessor(self._data_model).gen_model_data(instance)


    def _get(self, id):
        """ Retrieves instance with the specified key from datastore. """
        
        instance = self._data_model.get_by_id(int(id))
        if not instance:
            raise(ResourceNotExist('Requested instance does not exist'))

        return instance


    def _get_list(self, request):
        """ Retieves a list of all instances. """

        instances = self._data_model.all()
        out_list = []

        model_processor = ModelProcessor(self._data_model)
        
        for item in instances:
            out_list.append(model_processor.gen_model_data(item))
                    
        return {'instances_list': out_list}


    def _delete(self, request):
        """ Removes an article with the specified id from the storage. """

        instance_id = request.get('id')

        if instance_id:
            instance = self._data_model.get_by_id(int(instance_id))
            if instance:
                db.delete(instance)
            else:
                raise(ResourceNotExist('Requested instance does not exit'))
            return instance_id
        else:
            raise(ResourceNotExist('Requested instance does not exist'))
