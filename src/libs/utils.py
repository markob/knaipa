""" Utilities are used in other modules and contain common solutions for them """

import logging


def loginRequired(func):
    """ Login decorator checks if user is logged in. It redirects to create account
        page in case when user isn't logged in. """
    
    def wrapper(self, *args, **kw):
        user = users.get_current_user()
        
        if not user:
            logging.debug('Anonymous user tried to get access.')
            self.redirect(users.create_login_url(self.request.uri))
        else:
            func(self, *args, **kw)
    
    return wrapper


def genLazyClassLoaderProxy(clsName, modName):
    
    class LazyClassLoaderProxy(object):

        __classProperties = (clsName, modName)

        @staticmethod
        def __getClassObject():
            (clsName, modName) = LazyClassLoaderProxy.__classProperties
            
            _tmp = __import__(modName, globals(), locals(), [clsName], -1)
            return _tmp.__dict__[clsName]

        def __new__(cls, *args, **kwds):
            cls = LazyClassLoaderProxy.__getClassObject()
            return object.__new__(cls, *args, **kwds)

    return LazyClassLoaderProxy
