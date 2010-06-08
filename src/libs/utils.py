""" Utilities are used in other modules and contain common solutions for them """

import logging

from google.appengine.ext import db

from libs import xml_tools as XMLTools #@UnresolvedImport


def login_required():
    """ Redirects user to login page if it's not logged in. """
    pass


class InvalidRequestError(Exception):
    """ Invalid request exception. """

    def __init__(self, msg):
        self.message = 'Bad Request Error: ' + str(msg)
        logging.error(self.message)


    def __str__(self):
        return self.message


class ModelProcessor(object):
    """ Contains tools to simplify models processing. """

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

        model_data = {'id': model_instance.key().id()}

        # get all mandatory properties from instance
        properties = self._cls_model.properties()
        for prop_name in properties:
            model_data[prop_name] = getattr(model_instance, prop_name)

        # get all optional properties from instance
        if issubclass(self._cls_model, db.Expando):
            properties = model_instance.instance_properties()
            for prop_name in properties:
                model_data[prop_name] = getattr(model_instance, prop_name)

        return model_data


    def _parse_request(self, request, allParamsRequired):
        """ Extract data from request and fill them into dict. """

        data = {}

        # extract all mandatory data
        properties = self._cls_model.properties()
        for prop_name in properties:
            value = request.get(prop_name)

            prop_type = properties[prop_name]

            if not value and not prop_type.default_value():
                if allParamsRequired:
                    raise(InvalidRequestError, 'request data is not completed')
                else:
                    continue

            data[prop_name] = value

        # extract optional data if required
        if issubclass(self._cls_model, db.Expando):
            for field_name in request.fields:
                if field_name not in data:
                    data[field_name] = request.get(field_name)

        return data


    def _gen_xml_for_prop(self, xmlDoc, name, value, data_type):
        handlersMap = {
           db.StringProperty.data_type: XMLTools.genStringNode,
           db.TextProperty.data_type: XMLTools.genTextNode,
           db.DateProperty.data_type: XMLTools.genDateNode,
           db.TimeProperty.data_type: XMLTools.genTimeNode,
           db.DateTimeProperty.data_type: XMLTools.genDateTimeNode }

        return handlersMap[data_type](xmlDoc, value, name)
