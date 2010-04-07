from google.appengine.ext import db
from google.appengine.ext.db.polymodel import PolyModel

import hashlib

class Uzver(PolyModel):
    """ It's base user class. All system users should be its descendants. """
    
    first_name = db.StringProperty(default='Anonymous')
    last_name = db.StringProperty(default='Anonymous')
    email = db.EmailProperty(default='anonymous@mvmz-lv.appspot.com')
    nick_name = db.StringProperty(required=True)
    avatar = db.LinkProperty(default=None)
    password = db.StringProperty(default='qaswedfrtghy')
    
    _password_is_hashed = False
    
    
    def put(self):
        """ Updates password hash if it's needed. """
        self.password = self._gen_password_hash(self.password)
        
        PolyModel.put(self)
    
    
    def _gen_password_hash(self, password):
        """ Generates SHA1 hash for the password. """
        hash = self.password
        
        if not self._password_is_hashed:
            hash = hashlib.sha1(password).hexdigest()
            self._password_is_hashed = True
        
        return hash
    
    
    def set_password(self, password):
        """ Sets user password to the specified value. """
        self.password = password
        self._password_is_hashed = False
    
    
    def is_password(self, password):
        """ Checks that provided password is equal to user password. """
        if not self._password_is_hashed:
            self.password = self._gen_password_hash(self.password)
        
        hash = hashlib.sha1(password).hexdigest()
        
        if hash == self.password:
            return True
        else:
            return False
    
    
    def get_id(self):
        """ Returns user ID. """
        return self.key().id()
