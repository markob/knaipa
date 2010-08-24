'''
Created on Aug 7, 2010

@author: apetrenko
'''
from knajpa.models.restaurant import Knajpa, Address
import datetime
import logging

class KnajpaService():

    @staticmethod
    def create_new_knajpa(knajpaitem):
        m_knajpa = Knajpa(name=knajpaitem.name, dateOfCreate=knajpaitem.dateOfCreate, dateOfUpdate=knajpaitem.dateOfUpdate)
        m_knajpa.put()
        logging.info("Add knajpa to datastore %s" , str(m_knajpa.key().id()));
        
        for address in knajpaitem.get_address_list():
            m_address = Address(knajpa=m_knajpa.key(), address=address.completeAddress , ia=address.ia, ja=address.ja)
            m_address.put()
            logging.info("Add m_address %s for knajpa %s to datastore" , str(m_address.key().id()), str(m_knajpa.key().id()));
        
        return m_knajpa.key().id()

    @staticmethod
    def get_knajpa(id):
        return KnajpaItem.create_knajpa_item_based_on_model(Knajpa.get(id)) 

    @staticmethod
    def get_knajpa_list(limit, offset):
        knajpa_items = []
        for item in Knajpa.all():
            logging.info('method get_knajpa_list : %s', str(item))
            knajpa_items.append(KnajpaItem.create_knajpa_item_based_on_model(item))

        return knajpa_items
    
    @staticmethod
    def count_knajpa():
        return Knajpa.all().count()


class KnajpaItem():
    
    id = 0L
    
    name = '';
    
    dateOfCreate = datetime.datetime.today() ;
    
    dateOfUpdate = datetime.datetime.today() ;
    
    _addresses = [];
    
    def __init__(self, title):
        self.name = title
    
    def add_address(self, address, ia, ja):
        self._addresses.append(AddressItem(address=address, ia=ia, ja=ja))
        return self._addresses
        pass

    def get_address_list(self):
        return self._addresses

    def clear_address_list(self):
        self._addresses = []

    @staticmethod
    def create_knajpa_item_based_on_model(model):
        item = KnajpaItem(model.name)
        item.dateOfCreate = model.dateOfCreate
        item.dateOfUpdate = model.dateOfUpdate
        item.id = model.key().id()
        
        item.clear_address_list()
        for address in model.addresses:
            item.add_address(address.address, ia=address.ia, ja=address.ja)

        return item
        
        

class AddressItem():
    completeAddress = ''
    ia = 0.0
    ja = 0.0
    
    def __init__(self, address, ia, ja):
        self.completeAddress = address
        self.ia = ia
        self.ja = ja
        
