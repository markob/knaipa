import logging

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

import os
from google.appengine.ext.webapp import template

# Login decorator
def loginRequired(func):
    def wrapper(self, *args, **kw):
        user = users.get_current_user()
        
        if not user:
            logging.debug('Anonymous user tried to get access.')
            self.redirect(users.create_login_url(self.request.uri))
        else:
            func(self, *args, **kw)
    
    return wrapper


class Greeting(db.Model):
    author = db.UserProperty()
    content = db.TextProperty()
    date = db.DateTimeProperty(auto_now_add=True)

    
class MainPage(webapp.RequestHandler):
    @loginRequired
    def get(self):
        greetingsQuery = Greeting.all().order('-date')
        greetings = greetingsQuery.fetch(16)
        user = users.get_current_user()

        for greeting in greetings:
            if greeting.author == user:
                greeting.editTextLink = self.request.uri + 'edit/' + str(greeting.key())
                greeting.deleteTextLink = self.request.uri + 'delete/' + str(greeting.key())
            else:
                greeting.editTextLink = None
                greeting.deleteTextLink = None
        
        url = users.create_logout_url(self.request.uri)
        userNickname = users.get_current_user().nickname()
        urlLinkText = 'logout'
            
        templateValues = {
            'greetings'   : greetings,
            'url'         : url,
            'urlLinkText' : urlLinkText,
            'userNickname': userNickname}
        
        path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
        self.response.out.write(template.render(path, templateValues))

        
class GuestBook(webapp.RequestHandler):
    def post(self):
        greeting = Greeting()
        
        if users.get_current_user():
            greeting.author = users.get_current_user()
        
        greeting.content = self.request.get('content')
        greeting.put()
        self.redirect('/')


class EditPost(webapp.RequestHandler):
    def get(self, postKey):
        post = Greeting.get(postKey)
        
        user = users.get_current_user()
        index = self.request.uri.find('//')
        index = self.request.uri.find('/', index + 2)
        url = users.create_logout_url(self.request.uri[:index + 1])
        userNickname = users.get_current_user().nickname()
        urlLinkText = 'logout'
        
        updateTextLink = self.request.uri
        
        templateValues = {
            'greeting'      : post,
            'url'           : url,
            'urlLinkText'   : urlLinkText,
            'userNickname'  : userNickname,
            'messageText'   : post.content,
            'updateTextLink': updateTextLink}
        
        path = os.path.join(os.path.dirname(__file__), 'templates/edit.html')
        self.response.out.write(template.render(path, templateValues))

        
    def post(self, postKey):
        post = Greeting.get(postKey)
        
        post.content = self.request.get('content')
        post.put()
        self.redirect('/')
        

class DeletePost(webapp.RequestHandler):
    def get(self, postKey):
        post = Greeting.get(postKey)
        post.delete()
        self.redirect('/')


application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/sign', GuestBook),
                                      ('/edit/(.*)', EditPost),
                                      ('/delete/(.*)', DeletePost)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
