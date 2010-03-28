from google.appengine.ext import db
import hashlib


class Uzver(db.Expando):
    """ It's a base data for a user. It contains required data for all users.
    Other properties can be extended with groups and crosslink object.
    Currently most of user properties isn't needed. Only login is required.
    It allows to leave comments under one anonymous user. """
    
    first_name = db.StringProperty(default='Anonymous')
    last_name = db.StringProperty(default='Anonymous')
    nick_name = db.StringProperty(required=True)
    email = db.EmailProperty(default='anonymous@knajpa.com.ua')
    avatar = db.LinkProperty(default=None)
    password = db.StringProperty(default="password")
    
    
    def put(self):
        """ Converts 'clear text' password to hash and stores entity in
        datastore. """
        self.password = hashlib.sha1(self.password).hexdigest()
        
        db.Expando.put(self)
    
    
    def is_password(self, password):
        """ Get SHA1 hash of provided password and compares it to stored. """
        hash = hashlib.sha1(password).hexdigest()
        
        if hash == self.password:
            return True
        else:
            return False
    
    
    def set_password(self, password):
        """ Generates SHA1 hash from provided password string and stores it. """
        self.password = hashlib.sha1(password).hexdigest()
    
    
    def get_id(self):
        """ Retrieves unique id for the user. """
        return self.get_id()
