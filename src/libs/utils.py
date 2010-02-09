""" Utilities are used in other modules and contain common solutions
for them """

import logging

from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import template

from xml.dom import minidom
from libs import xml_tools as XMLTools

import os

templates_path = os.path.join(os.path.dirname(__file__), '../templates')


class InvalidRequestError(Exception):
    """ Invalid request exception. """

    def __init__(self, msg):
        self.message = 'Bad Request Error: ' + str(msg)
        logging.error(self.message)


    def __str__(self):
        return self.message


class ModelProcessor(object):
    """ Contans tools simlify models processing. """

    def __init__(self, cls_model):
        """ Binds processor to the specified model type. """
        
        self._cls_model = cls_model


    def create_from_request(self, request):
        """ Extracts the model data from request and creates a model
        instance. """

        # extract model data from request
        data = self._parse_request(request, True)
        
        # create and return model instance
        model_instance = self._cls_model(**data)

        return model_instance


    def update_from_request(self, request, model_instance):
        """ Extracts the model data from request and updates a model
        instance. """

        # extract model data from request
        data = self._parse_request(request, False)

        if len(data) > 0:
            # update model instance data
            for name, value in data:
                setattr(model_instance, name, value)
        else:
            raise(InvalidRequestError, 'empty request retrieved')


    def gen_model_data(self, model_instance):

        properties = self._cls_model.properties()
        model_data = {'id': model_instance.key().id()}
        
        for prop_name in properties:
            model_data[prop_name] = getattr(model_instance, prop_name)

        return model_data


    def _parse_request(self, request, allParamsRequired):
        """ Extract data from request and fill them into dict. """

        data = {}

        properties = self._cls_model.properties()
        
        for prop_name in properties:
            value = request.get(prop_name)

            prop_type = properties[prop_name]

            if not value and not prop_type.default_value():
                if allParamsRequired:
                    raise(InvalidRequestError,
                          'request data is not completed')
                else:
                    continue

            data[prop_name] = value

        return data


    def _gen_xml_for_prop(self, xmlDoc, name, value, data_type):
        handlersMap = {
           db.StringProperty.data_type: XMLTools.genStringNode,
           db.TextProperty.data_type: XMLTools.genTextNode,
           db.DateProperty.data_type: XMLTools.genDateNode,
           db.TimeProperty.data_type: XMLTools.genTimeNode,
           db.DateTimeProperty.data_type: XMLTools.genDateTimeNode }

        return handlersMap[data_type](xmlDoc, value, name)


    
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
            handler, template_name = self._get_cmd_handler()
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
            raise(InvalidRequestError('Requested instance does not exists'))

        return instance


    def _get_list(self, request):
        """ Retieves a list of all instances. """

        instances = self._data_model.all()
        out_list = []

        model_processor = ModelProcessor(self._data_model)
        
        for item in instances:
            out_list.append(model_processor.gen_model_data(item))
                    
        return {'instances_list': out_list}
