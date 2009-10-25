""" Utilities are used in other modules and contain common solutions for them """

import logging

from google.appengine.ext import db

from xml.dom import minidom


def loginRequired(func):
    """ Login decorator checks if user is logged in. It redirects to create account
        page in case when user isn't logged in. """
    
    def wrapper(self, *args, **kw):
        user = users.get_current_user()
        
        if not user:
            logging.debug('Anonymous user tried to get access.')
            self.redirect(users.create_login_url(self.request.uri))
        else:
            func(self, *args, **kw)
    
    return wrapper


class DataMapperUtils(object):
        
    @staticmethod
    def genStringNode(dom, str, name):
        root = dom.createElement(name)
        
        text = dom.createTextNode(str)
        root.appendChild(text)
        
        return root

    
    @staticmethod
    def genDateNode(dom, date, name='date'):
        root = dom.createElement(name)
        
        node = dom.createElement('year')
        root.appendChild(node)
        text = dom.createTextNode(str(date.year))
        node.appendChild(text)
        
        node = dom.createElement('month')
        root.appendChild(node)
        text = dom.createTextNode(str(date.month))
        node.appendChild(text)
        node = dom.createElement('day')
        root.appendChild(node)
        text = dom.createTextNode(str(date.day))
        node.appendChild(text)
        
        return root
    
    
    @staticmethod
    def genTimeNode(dom, time, name='time'):
        root = dom.createElement(name)
        
        node = dom.createElement('hour')
        root.appendChild(node)
        text = dom.createTextNode(str(time.hour))
        node.appendChild(text)
        
        node = dom.createElement('minute')
        root.appendChild(node)
        text = dom.createTextNode(str(time.minute))
        node.appendChild(text)

        node = dom.createElement('second')
        root.appendChild(node)
        text = dom.createTextNode(str(time.day))
        node.appendChild(text)
        
        return root


    @staticmethod
    def genDateTimeNode(dom, datetime, name='datetime'):
        root = DataMapperUtils.genDateNode(dom, datetime, name)

        node = dom.createElement('hour')
        root.appendChild(node)
        text = dom.createTextNode(str(datetime.hour))
        node.appendChild(text)
        
        node = dom.createElement('minute')
        root.appendChild(node)
        text = dom.createTextNode(str(datetime.minute))
        node.appendChild(text)

        node = dom.createElement('second')
        root.appendChild(node)
        text = dom.createTextNode(str(datetime.day))
        node.appendChild(text)
        
        return root


    @staticmethod
    def genTextNode(dom, text, name='text'):
        root = dom.createElement(name)

        node = dom.createCDATASection(text)
        root.appendChild(node)

        return root
    

    @staticmethod
    def genXMLNode(xmlDoc, data, name):
        handlersMap = {
            db.StringProperty.data_type: DataMapperUtils.genStringNode,
            db.TextProperty.data_type: DataMapperUtils.genTextNode,
            db.DateProperty.data_type: DataMapperUtils.genDateNode,
            db.TimeProperty.data_type: DataMapperUtils.genTimeNode,
            db.DateTimeProperty.data_type: DataMapperUtils.genDateTimeNode }
        
        return handlersMap[type(data)](xmlDoc, data, name)

    
    @staticmethod
    def genXML(model):
        xmlDoc = minidom.Document()

        root = xmlDoc.createElement('data')
        xmlDoc.appendChild(root)

        for name in model._items:
            node = DataMapperUtils.genXMLNode(xmlDoc, getattr(model, name), name)
            root.appendChild(node)
        
        return xmlDoc.toxml('utf8')
