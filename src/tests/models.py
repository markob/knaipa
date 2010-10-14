from google.appengine.api import memcache
from google.appengine.api import users
from google.appengine.ext import db


class UserPrefs(db.Model):
    tzOffset = db.IntegerProperty(default=0)
    user = db.UserProperty(auto_current_user_add=True)

    def CacheSet(self):
        memcache.set(self.key().name(), self, namespace=self.key().kind())

    def put(self):
        self.CacheSet()
        db.Model.put(self)


def GetUserPrefs(userId=None):
    if not userId:
        user = users.get_current_user()
        if not user:
            return None
        userId = user.user_id()

    userPrefs = memcache.get(userId, namespace='UserPrefs')
    if not userPrefs:
        key = db.Key.from_path('UserPrefs', userId)
        userPrefs = db.get(key)

        if userPrefs:
            userPrefs.CacheSet()
        else:
            userPrefs = UserPrefs(key_name=userId)

    return userPrefs
        
                                  

