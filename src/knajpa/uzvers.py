from knajpa.models.uzvers import Uzver
from google.appengine.ext import db



class BadUserRequest(Exception):
    """ Following exception is used to indicate bad user data """
    pass


def UserProxy(object):
    """ It's wrapper for users implementation which gets some additional functionality """
        

    def __init__(self, user_data, is_new=True, user_id=None):
        """ Creates new user or loads an existing user data from datastore """
        if (None == user_id) and (None == user_data or None == user_data['nick_name']):
            raise(BadUserData, 'user nickname or id is required')

        if None != user_id:
            # existing user requested, try to get it
            user = db.get(user_id)
            if None == user:
                raise(BadUserData, 'user with the specified nickname does not exist')
        
        elif is_new:
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

        # password should be updated in other way
        if user_data.has_key('password'):
            self._user_.set_password(user_data['password'])


    def get_user_id(self):
        """ Simple retrieves user id """
        self._user_.key().id_or_name()


    def is_password(self, password):
        """ Checks user password and retrieves True or False """
        return self._user_.is_password(password)



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
