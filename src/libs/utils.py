""" Utilities are used in other modules and contain common solutions
for them """

import logging

from google.appengine.ext import db
from xml.dom import minidom
from libs import xml_tools as XMLTools


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
        data = self._parse_request(request)
        
        # create and return model instance
        model_instance = self._cls_model(**data)

        return model_instance


    def update_from_request(self, request, model_instance):
        """ Extracts the model data from request and updates a model
        instance. """

        # extract model data from request
        data = self._parse_request(request)

        # update model instance data
        for name, value in data:
            setattr(model_instance, name, value)


    def gen_xml(self, model_instance):
        xmlDoc = minidom.Document()

        root = xmlDoc.createElement(self._cls_model.kind().lower())
        xmlDoc.appendChild(root)

        properties = self._cls_model.properties()

        for prop_name in properties:
            prop_type = properties[prop_name]
            
            node = self._gen_xml_for_prop(xmlDoc,
                                          prop_name,
                                          getattr(model_instance, prop_name),
                                          prop_type.data_type)
            root.appendChild(node)

        return xmlDoc.toxml('utf8')


    def _parse_request(self, request):
        """ Extract data from request and fill them into dict. """

        data = {}

        properties = self._cls_model.properties()
        
        for prop_name in properties:
            value = request.get(prop_name)

            prop_type = properties[prop_name]

            if not value and not prop_type.default_value():
                raise(InvalidRequestError, 'request data is not completed')

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
