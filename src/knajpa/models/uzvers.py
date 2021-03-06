from google.appengine.ext import db

import hashlib

class Uzver(db.Model):
    """ It's base user class. All system users should be its descendants. """
    
    first_name = db.StringProperty(required=True)
    last_name = db.StringProperty(required=True)
    email = db.EmailProperty(required=True)
    nick_name = db.StringProperty(required=True)
    password = db.StringProperty(required=True)
    password_is_hashed = db.BooleanProperty(default=False)
    avatar = db.LinkProperty(default=None)
    created = db.DateTimeProperty(required=True, auto_now_add=True)
    
    
    def put(self):
        """ Updates password hash if it's needed. """
        self.password = self._gen_password_hash(self.password)
        
        db.Model.put(self)
    
    
    def _gen_password_hash(self, password):
        """ Generates SHA1 hash for the password. """
        hash = self.password
        
        if not self.password_is_hashed:
            hash = hashlib.sha1(password).hexdigest()
            self.password_is_hashed = True
        
        return hash
    
    
    def set_password(self, password):
        """ Sets user password to the specified value. """
        self.password = password
        self.password_is_hashed = False
    
    
    def is_password(self, password):
        """ Checks that provided password is equal to user password. """
        if not self.password_is_hashed:
            self.password = self._gen_password_hash(self.password)
        
        hash = hashlib.sha1(password).hexdigest()
        
        if hash == self.password:
            return True
        else:
            return False
    
    
    def get_id(self):
        """ Returns user ID. """
        return self.key().id()

