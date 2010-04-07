import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from google.appengine.ext import db

from libs.utils import InvalidRequestError, ModelProcessor

import os

templates_path = os.path.join(os.path.dirname(__file__), '../templates')


class ObjectHandler(webapp.RequestHandler):
    def __init__(self, data_model):
        self._data_model = data_model


    def get(self):
        """ Just hooks all GET requests and passes it to processor. """
        
        return self._handle_request()


    def post(self):
        """ Just hooks all POST requests and passes it to processor. """

        return self._handle_request()


    def _handle_request(self):
        """ Processes input request and creates appropriate reqponse. """

        try:
            handler, template_name = self._select_cmd_handler()
            resp_data = handler(self.request)

            template_path = os.path.join(templates_path, template_name)
            
            self.response.headers['Content-Type'] = 'text/xml'
            return self.response.out.write(
                template.render(template_path, resp_data))

        except InvalidRequestError, err:
            return self.error(404)
        

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
            raise(InvalidRequestError('Invalid instance id requested'))

        instance = self._get(instance_id)
        
        return ModelProcessor(self._data_model).gen_model_data(instance)


    def _get(self, id):
        """ Retrieves instance with the specified key from datastore. """
        
        instance = self._data_model.get_by_id(int(id))
        if not instance:
            raise(InvalidRequestError('Requested instance does not exist'))

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

        instance_id = request.get(id)

        if instance_id:
            self._data_model.delete(instance_id)
            return instance_id
        else:
            raise(InvalidRequestError('Requested instance does not exist'))
