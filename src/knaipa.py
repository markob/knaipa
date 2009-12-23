import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

def loginRequired(func):
    """ Login Decorator - checks current user status and
    redirects to login page if user is not logged in. """
    
    def wrapper(self, *args, **kw):
        user = users.get_current_user()
        
        if not user:
            logging.debug('Anonymous user tried to get access.')
            self.redirect(users.create_login_url(self.request.uri))
        else:
            func(self, *args, **kw)
    
    return wrapper


application = webapp.WSGIApplication(
    [('/cmd/login', MainPage)],
    debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
