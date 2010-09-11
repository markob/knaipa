'''
Created on Sep 11, 2010

@author: apetrenko
'''
from google.appengine.ext import db
from knajpa.models.imodels import DocumentsQueue
import logging

class DatastoreService():
    
    @staticmethod
    def put(model):
        if not isinstance(model, db.Model):
            raise TypeError('Incorrect type. The model must be db.Model but it was ' + str(model))
        
        model.put()
        
        docs_queue = DocumentsQueue.get_instance()
        docs_queue.documents.append(model.key().id())
        docs_queue.put()
        
        logging.debug("document has been added to the index queue")
        logging.debug(model)
                                        
