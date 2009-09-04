from xml.dom import minidom
from libs.models.info import *

from google.appengine.ext import db


class InfoMapper:
    """  """

    @staticmethod        
    def genXMLByModel(model):
        """ Creates XML DOM object based on certain Model item.
            Retrieves completed XML string as a result.
        """
        
        doc = minidom.Document()
        
        root = doc.createElement(model.)
        doc.appendChild(root)
        
        node = doc.createElement('title')
        node.setAttribute('value', str(timeToStart.days))
        root.appendChild(node)
        
        node = doc.createElement('hours')
        node.setAttribute('value', str(timeToStart.seconds/3600))
        root.appendChild(node)
        
        node = doc.createElement('minutes')
        node.setAttribute('value', str((timeToStart.seconds%3600)/60))
        root.appendChild(node)
        
        node = doc.createElement('seconds')
        node.setAttribute('value', str(timeToStart.seconds%60))
        root.appendChild(node)
        
        return doc.toxml('utf-8')

    @staticmethod
    def genModelByXML(xml):
        pass
