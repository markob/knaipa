import logging

import os, sys

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app


def AddLibsToPath():
    """ Appends lib content to Python system path. """

    # get project root first
    projRoot = os.curdir
    # append library path to system path
    sys.path.apend(projRoot + '/libs')


class CommandRounter(webapp.RequestHandler):
    """ General command preprocessor(router) which gets command
    and passes it to appropriate router. """

    __handlers = {'article': ArticleController}

    def getHandler(self, cmd):
        """ Selects appropriate handler and pass request to it. """
        try:
            handler = self.__handlers[self.request.get('cmd')]
        except:
            handler = self.__handlers['invalid']

        # load appropriate handler and launch it
        __import__(handler)


    def get(self):

        return handler.get(self.request)
    

    def post(self):
        pass
    

application = webapp.WSGIApplication(
    [('/cmd/', CommandRouter)], debug=True)

def main():
    AddLibsToPath()
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
