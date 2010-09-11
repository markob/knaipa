'''
Created on Aug 7, 2010

@author: apetrenko
'''
from google.appengine.api.datastore_errors import EntityNotFoundError
from knajpa.services.db.datastoreService import DatastoreService

from knajpa.models.restaurant import Knajpa, Address, Group, Item
import datetime
import logging
from google.appengine.ext import db

logging.getLogger().setLevel(logging.DEBUG)

class KnajpaService():

    @staticmethod
    def _updateAddresses(knajpaitem, m_knajpa, is_create):
        for address in knajpaitem.get_address_list():
            
            if is_create :
                m_address = Address(knajpa=m_knajpa.key(), address=address.completeAddress, ia=address.ia, ja=address.ja)
            else:
                if address.id == -1L:
                    #todo update address
                    m_address = Address(knajpa=m_knajpa.key(), address=address.completeAddress, ia=address.ia, ja=address.ja)
                else:
                    m_address = Address.get_by_id(address.id)
            
            DatastoreService.put(m_address)
            logging.info("Add m_address %s for knajpa %s to datastore", str(m_address.key().id()), str(m_knajpa.key().id()))
        pass
    
    
    """
    Create or Update Knajpa based on KnajpaItem   
    """
    @staticmethod
    def create_new_knajpa(knajpaitem):
        if not isinstance(knajpaitem , KnajpaItem):
            raise TypeError('incorrect type of parameter knajpaitem')
        
        m_knajpa = Knajpa(name=knajpaitem.name, dateOfCreate=knajpaitem.dateOfCreate, dateOfUpdate=knajpaitem.dateOfUpdate)
        DatastoreService.put(m_knajpa)
        
        logging.debug("Add knajpa to datastore %s" , str(m_knajpa.key().id()));
        
        KnajpaService._updateAddresses(knajpaitem, m_knajpa, True)
        
        for group in knajpaitem.get_groups_list():
            m_group = Group(knajpa=m_knajpa.key(), name=group.name)
            DatastoreService.put(m_group)
            logging.debug("Add m_group %s for knajpa %s to datastore", str(m_group.key().id()), str(m_knajpa.key().id()))
            
            for item in group.get_content_item_list():
                m_item = Item(name=item.name, value=item.value, group=m_group.key())
                DatastoreService.put(m_item)
                logging.debug("Add m_item %s to group %s for knajpa %s to datastore", str(m_item.key().id()), m_group.key().name(), str(m_knajpa.key().id()))

        return m_knajpa.key().id()

    @staticmethod
    def _create_map_from_list(list):
        map = {}
        for item in list:
            if(item.id != None and item.id > 0):
                map[item.id] = item
        return map     

    @staticmethod
    def _get_action_map(old_list, new_list):
        map_from_old_item_list = KnajpaService._create_map_from_list(old_list)
        map_from_new_item_list = KnajpaService._create_map_from_list(new_list)
        g_update = [] 
        g_delete = []
        g_add = []
        
        for key in map_from_new_item_list:
            if((key != None and key > 0) and (key in map_from_old_item_list)) :
                g_update.append(map_from_new_item_list[key])
            else :
                g_add.append(map_from_new_item_list[key])
            pass
        
        for key in map_from_old_item_list:
            if(key not in map_from_new_item_list):
                g_delete.append(map_from_old_item_list[key])
                pass
            pass
        pass
        logging.debug('List of items that have to be added: %s', str(g_add))
        logging.debug('List of items that have to be updated: %s', str(g_update))
        logging.debug('List of items that have to be deleted: %s', str(g_delete))
        return {'add': g_add, 'update': g_update , 'delete': g_delete}
    
    @staticmethod
    def _add_items_to_group(group, list_of_item):
        for item in list_of_item:
                m_item = Item(name=item.name, value=item.value, group=group.key())
                DatastoreService.put(m_item)
                logging.debug("Add m_item %s for group %s to datastore", str(m_item.key().id()), group.key().name())
                
    @staticmethod
    def _update_content_item (content):
        m_content = None
        if isinstance(content, GroupContent):
            m_content = Group.get_by_id(content.id)
        elif isinstance(content, ContentItem):
            m_content = Item.get_by_id(content.id)
            m_content.value = content.value
        m_content.name = content.name
        
        DatastoreService.put(m_content)
        return  m_content  
        
    @staticmethod
    def _delete_content_items(list):
        for content in list:
            if isinstance(content, GroupContent):
                group = Group.get_by_id(content.id)
                if group:
                    db.delete(group)
            elif isinstance(content, ContentItem):
                item = Item.get_by_id(content.id)
                if item:
                    db.delete(item)
    
    @staticmethod
    def _update_group(m_knajpa, knajpaitem):
        old_list = GroupContent.get_content_item_list_based_on_models(m_knajpa.contentGroups)
        action_map = KnajpaService._get_action_map(old_list, knajpaitem.get_groups_list())
        
        for group in action_map.get('add'):
            
            m_group = Group(knajpa=m_knajpa.key(), name=group.name)
            DatastoreService.put(m_group)
            logging.debug("Add m_group %s for knajpa %s to datastore", str(m_group.key().id()), str(m_knajpa.key().id()))
            
            KnajpaService._add_items_to_group(m_group, group.get_content_item_list())
        
        for group in action_map.get('update'):
            m_group = KnajpaService._update_content_item(group)
            
            old_list_items = ContentItem.get_content_item_list_based_on_models(m_group.items)
            action_map_for_item = KnajpaService._get_action_map(old_list_items, group.get_content_item_list())
            
            KnajpaService._add_items_to_group(m_group, action_map_for_item.get('add'))
            KnajpaService._delete_content_items(action_map_for_item.get('delete'))    
            for item in action_map_for_item.get('update'):
                KnajpaService._update_content_item(item)

        KnajpaService._delete_content_items(action_map.get('delete'))
    
    @staticmethod
    def update_knajpa(knajpaitem):
        if not isinstance(knajpaitem , KnajpaItem):
            raise TypeError('incorrect type of parameter knajpaitem')
        
        if knajpaitem.id == -1L :
            return KnajpaService.create_new_knajpa(knajpaitem)
         
        m_knajpa = Knajpa.get_by_id(knajpaitem.id)
        if(m_knajpa == None):
            raise EntityNotFoundError('knajpa entity with id {0} was not found'.format(knajpaitem.id))
        
        if(knajpaitem.name != None and knajpaitem.name != ''):
            m_knajpa.name = knajpaitem.name
        m_knajpa.dateOfUpdate = knajpaitem.dateOfUpdate
        DatastoreService.put(m_knajpa)
        logging.info("Update knajpa to datastore %s" , str(m_knajpa.key().id()));
        
        KnajpaService._updateAddresses(knajpaitem, m_knajpa, False)
        KnajpaService._update_group(m_knajpa, knajpaitem)
        
        return m_knajpa.key().id() 
    
    @staticmethod
    def get_knajpa(id):
        return KnajpaItem.create_knajpa_item_based_on_model(Knajpa.get_by_id(id)) 

    @staticmethod
    def get_knajpa_list(limit, offset):
        knajpa_items = []
        for item in Knajpa.all():
            logging.debug('method get_knajpa_list : %s', str(item))
            knajpa_items.append(KnajpaItem.create_knajpa_item_based_on_model(item))

        return knajpa_items
    
    @staticmethod
    def count_knajpa():
        return Knajpa.all().count()


class KnajpaItem(object):
    
    id = -1L
    
    name = '';
    
    dateOfCreate = datetime.datetime.today() ;
    
    dateOfUpdate = datetime.datetime.today() ;
    
    _addresses = [];
    
    _phonenumbers = [];
    
    _groups = []
    
    
    def __init__(self, title, id= -1L):
        self.id = id
        self.name = title
        self._addresses = []
        self._phonenumbers = []
        self._groups = []
        
    
    def add_address(self, address, ia, ja):
        self._addresses.append(AddressItem(address=address, ia=ia, ja=ja))
        return self._addresses
        pass
    
    def add_address_item(self, address_item):
        if(isinstance(address_item, AddressItem)):
            self._addresses.append(address_item)
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
        item.id = model.key().id()
        item.dateOfCreate = model.dateOfCreate
        item.dateOfUpdate = model.dateOfUpdate
        
        item.clear_address_list()
        for address in model.addresses:
            address_item = AddressItem(address.address, ia=address.ia, ja=address.ja)
            address_item.id = address.key().id()
            item.add_address_item(address_item)

#        for phoneNumber in model.phonenumbers:
#            pass
        item.clear_group_list()
        for group in model.contentGroups :
            group_content = GroupContent(name=group.name)
            group_content.id = group.key().id()
            
            for group_item in group.items:
                group_content.add_content_item(group_item.name, group_item.value, group_item.key().id())
                
            
            item.add_group(group_content)

        return item
        

class AddressItem():
    id = -1L
    completeAddress = ''
    ia = 0.0
    ja = 0.0
    
    def __init__(self, address, ia, ja, id= -1L):
        self.completeAddress = address
        self.ia = ia
        self.ja = ja
        self.id = id

class GroupContent():
    id = -1L
    name = ''
    _items = []
    
    def __init__(self, name, id= -1L):
        self._validateParameters(name)
        self.name = name
        self._items = []
        self.id = id
        
    
    def add_content_item(self, name, value, id= -1L):
        self._validateParameters(name)
        contentItem = ContentItem(name, value, id)
        self._items.append(contentItem)
        return contentItem
    


    
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
  
    @staticmethod    
    def get_content_item_list_based_on_models(model_groups):
        list = [];
        for group in model_groups :
            group_content = GroupContent(group.name, group.key().id())
            
            for group_item in group.items:
                group_content.add_content_item(group_item.name, group_item.value, group_item.key().id())
            
            list.append(group_content)
        return list
    
    

class ContentItem():
    id = -1L
    name = ''
    value = ''
    
    
    def __init__(self, name, value, id= -1L):
        self.name = name
        self.value = value
        self.id = id
    
    @staticmethod 
    def get_content_item_list_based_on_models(model_items):
        list = []
        for item in model_items:
            list.append(ContentItem(item.name, item.value, item.key().id()))

        return list
    
class PhoneNumberItem():
    pass




    
     
