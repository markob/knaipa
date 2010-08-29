'''
Created on Aug 7, 2010

@author: apetrenko
'''
from knajpa.models.restaurant import Knajpa, Address, Group, Item
import datetime
import logging
#from io import Uns#upportedOperation

class KnajpaService():

    @staticmethod
    def create_new_knajpa(knajpaitem):
        if not isinstance(knajpaitem , KnajpaItem):
            raise TypeError('incorrect type of parameter knajpaitem')
        
        m_knajpa = Knajpa(name=knajpaitem.name, dateOfCreate=knajpaitem.dateOfCreate, dateOfUpdate=knajpaitem.dateOfUpdate)
        m_knajpa.put()
        logging.info("Add knajpa to datastore %s" , str(m_knajpa.key().id()));
        
        for address in knajpaitem.get_address_list():
            m_address = Address(knajpa=m_knajpa.key(), address=address.completeAddress , ia=address.ia, ja=address.ja)
            m_address.put()
            logging.info("Add m_address %s for knajpa %s to datastore" , str(m_address.key().id()), str(m_knajpa.key().id()));
        
        for group in knajpaitem.get_groups_list():
            m_group = Group(knajpa=m_knajpa.key(), name=group.name)
            m_group.put()
            logging.info("Add m_group %s for knajpa %s to datastore", str(m_group.key().id()), str(m_knajpa.key().id()))
            
            for item in group.get_content_item_list():
                m_item = Item(name=item.name, value=item.value, group=m_group.key())
                m_item.put()
                logging.info("Add m_item %s to group %s for knajpa %s to datastore", str(m_item.key().id()), m_group.key().name(), str(m_knajpa.key().id()))

        return m_knajpa.key().id()

    @staticmethod
    def get_knajpa(id):
        return KnajpaItem.create_knajpa_item_based_on_model(Knajpa.get_by_id(id)) 

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


class KnajpaItem(object):
    
    id = 0L
    
    name = '';
    
    dateOfCreate = datetime.datetime.today() ;
    
    dateOfUpdate = datetime.datetime.today() ;
    
    _addresses = [];
    
    _phonenumbers = [];
    
    _groups = []
    
    
    def __init__(self, title):
        self.name = title
        self._addresses = []
        self._phonenumbers = []
        self._groups = []
    
    def add_address(self, address, ia, ja):
        self._addresses.append(AddressItem(address=address, ia=ia, ja=ja))
        return self._addresses
        pass

    def get_address_list(self):
        return self._addresses

    def clear_address_list(self):
        self._addresses = []

    def add_phonenumber(self, type, number):
#        self._phonenumbers.append(PhoneNumberItem())
#        raise UnsupportedOperation("it's not implemented yet")
        pass

    def add_group(self, group):
        if not isinstance(group, GroupContent):
            raise TypeError('incorrect group type')
        self._groups.append(group)

    def get_group(self, name):
        for group in self._groups : 
            if group.name == name:
                return group
        return None
    
    def get_groups_list(self):
        return self._groups
    
    def clear_group_list(self):
        self._groups = []
    
    @staticmethod
    def create_knajpa_item_based_on_model(model):
        item = KnajpaItem(model.name)
        item.dateOfCreate = model.dateOfCreate
        item.dateOfUpdate = model.dateOfUpdate
        item.id = model.key().id()
        
        item.clear_address_list()
        for address in model.addresses:
            item.add_address(address.address, ia=address.ia, ja=address.ja)

#        for phoneNumber in model.phonenumbers:
#            pass
        item.clear_group_list()
        for group in model.contentGroups :
            group_content = GroupContent(name=group.name)
            
            for group_item in group.items:
                group_content.add_content_item(group_item.name, group_item.value)
            
            item.add_group(group_content)

        return item
        

class AddressItem():
    completeAddress = ''
    ia = 0.0
    ja = 0.0
    
    def __init__(self, address, ia, ja):
        self.completeAddress = address
        self.ia = ia
        self.ja = ja

class GroupContent():
    name = ''
    _items = []
    
    def __init__(self, name):
        self._validateParameters(name)
        self.name = name
        self._items = []
        
    
    def add_content_item(self, name, value):
        self._validateParameters(name)
        self._items.append(ContentItem(name, value))
    
    def remove_content_item(self, name):
        self._validateParameters(name)
        self._items.remove(name)

    def get_content_item_list(self):
        return self._items
    
    def update_content_item(self, name, value):
        for item in self._items:
            if item.name == name:
                item.value = value
    
    def _validateParameters(self, name):
        if (name == None):
            raise ValueError('parameter name could not be empty')

class ContentItem():
    name = ''
    value = ''
    def __init__(self, name, value):
        self.name = name
        self.value = value
           
    
    
        
class PhoneNumberItem():
    pass
