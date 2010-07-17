import logging as log

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import os,sys

#sys.path.append('/data/programming/projects/startup/knajpa/src')
log.info(os.path)

from knajpa.models.articles import Article
from knajpa.handlers.objhandler import ObjectHandler
from knajpa.utils import InvalidRequestError


# Articles service request handler
class ArticleHandler(ObjectHandler):
    """ Adapts article and stores it to data storage. """

    def __init__(self):
        ObjectHandler.__init__(self, Article)

        # add cmd handlers
        self._cmd_handlers = { 'list'  : (self._get_list, 'article/articles-list.xml'),
                               'add'   : (self._write, 'article/articles-add.xml'),
                               'get'   : (self._read, 'article/articles-get.xml'),
                               'del'   : (self._delete, 'article/articles-del.xml'),
                               'info'  : (lambda self: None, 'article/articles-info.xml'),
                               'error' : (lambda self: None, 'article/articles-error.xml') }
        
        log.debug("Article handler was initialized")
    
    
    def _select_cmd_handler(self):
        """ Selects appropriate handler for the requested command. """

        cmd = self.request.get('cmd')

        try:
            return self._cmd_handlers[cmd]
        except KeyError:
            raise(InvalidRequestError('invalid command requested'))

    
        
application = webapp.WSGIApplication(
    [('/articles', ArticleHandler)], debug = True)
        
        
def main():
    run_wsgi_app(application)

        
if __name__ == '__main__':
    main()
