'''
Created on Sep 11, 2010

@author: apetrenko
'''
from google.appengine.ext import db
from knajpa.search.utils import AddDocumentToIndexQueue
import logging

class DatastoreService():
    
    @staticmethod
    def put(model):
        if not isinstance(model, db.Model):
            raise TypeError('Incorrect type. The model must be db.Model but it was ' + str(model))
        
        model.put()
        AddDocumentToIndexQueue (model)
        logging.debug("document has been added to the index queue")
                                        
