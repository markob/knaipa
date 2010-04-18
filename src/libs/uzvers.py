from libs.models.uzvers import Uzver
from google.appengine.ext import db



class BadUserRequest(Exception):
    """ Following exception is used to indicate bad user data """
    pass


def UserProxy(object):
    """ It's wrapper for users implementation which gets some additional functionality """
        

    def __init__(self, user_data, is_new=True):
        """ Creates new user or loads an existing user data from datastore """
        if None == user_data or None == user_data['nick_name']:
            raise(BadUserData, 'user nickname is required')
        
        if is_new:
            # create new user but check for duplicates first
            if not self._is_unique(user_data):
                raise(BadUserRequest, 'user with such nickname or email exists')
            

            user = Uzver(user_data)
            user.put()

        else:
            # try to get and update an existing user or raise exception if it's not exist
            key = db.Key(Uzver, user_data['nick_name'])
            user = db.get(key)

            if None == user:
                raise(BadUserRequest, 'user with the specified nickname does not exist')

            # anonymous user is read-only
            if 'anonymous' == user['nick_name'].to_lower():
                raise(BadUserRequest, 'specified user is read-only')

            # update user data
            self._user_ = user
            self.set_user_info(user_data)

        self._user_ = user


    def _is_unique(self, user_data):
        """ Checks that the specified user nickname or email don't exist in datastore """
        if None == user_data['nick_name'] or None == user_data['email']:
            raise(BadUserRequest, 'invalid request data')
        
        query = db.Query(Uzver)
        query = query.filter('nick_name =', user_data['nick_name'])
        query = query.filter('email =', user_data['email'])

        if None != query.get():
            return False

        return True


    def get_user_info(self):
        """ Simple retrieves user data """
        user_data = {}
        instance_properties = self._user_.instance_properties()
        for prop_name in instance_properties:
            user_data[prop_name] = getattr(user, prop_name)

        return user_data


    def set_user_info(self, user_data):
        """ Updates user instance with the passed data """
        instance_properties = self._user_.instance_properties()

        for prop_name in instance_properties:
            if user_data.has_key(prop_name):
                setattr(self._user_, prop_name, user_data[prop_name])


    def get_user_id(self):
        """ Simple retrieves user id """
        self._user_.key().id_or_name()



def get_anonymous_id():
    """ Retrieves anonymous user object """
    # try to get anonymous user
    key = db.Key(Uzver, 'anonymous')
    user = db.get(key)

    # or create it if it does not exist
    if None == user:
        user = Uzver(nick_name='anonymous',
                     first_name='unknown',
                     last_name='unknown',
                     email='anonymous@knajpa.com.ua',
                     password='qaswedfrtghy')
        user.put()

    return user.key().id_or_name()
