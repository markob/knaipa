import logging

from xml.dom import minidom

class ObjectConverter(object):
    """ Converts article object retirieved from client and does
    appropriate processing before to store it in data storage and
    vice versa. """

    def __init__(self, scheme):
        """ Initializes new parser object for the specified scheme. """
        self.__scheme = scheme
        
    
    def decodeXML2Objects(self, xmlStr):
        """ Parses XML object and generates a list of objects according
        to appropriate scheme. """
        xmlDoc = minidom.parseString(xmlStr)

        # scan document for appropriate scheme entries
        # get list of all object properties
        props = xmlDoc.getElementsByTagName('property')

        # try to extract all properties described in scheme from object
        for propName in scheme:
            for prop in props:
                if propName == prop.getAttribute('name'):
                    # property was founded
                    break;

            if None == founded:
                # was not 

        return lstObjects

    def encodeObjects2XML(self, objects):
        """ Generates XML DOM object from objects list and apporpriate
        document scheme. """
