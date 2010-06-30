import logging as log

from common import main, set_system_path
set_system_path()

from google.appengine.ext import webapp

from models.articles import Article
from objhandler import ObjectHandler
from utils import InvalidRequestError

# Articles service request handler
class ArticleHandler(ObjectHandler):
    """ Adapts article and stores it to data storage. """

    def __init__(self):
        ObjectHandler.__init__(self, Article)

        # add cmd handlers
        self._cmd_handlers = { 'list'  : (self._get_list, 'articles-list.xml'),
                               'add'   : (self._write, 'articles-add.xml'),
                               'get'   : (self._read, 'articles-get.xml'),
                               'del'   : (self._delete, 'articles-del.xml'),
                               'info'  : (lambda self: None, 'articles-info.xml'),
                               'error' : (lambda self: None, 'articles-error.xml') }
        
        log.debug("Article handler was initialized")
    
    
    def _select_cmd_handler(self):
        """ Selects appropriate handler for the requested command. """

        cmd = self.request.get('cmd')

        try:
            return self._cmd_handlers[cmd]
        except KeyError:
            raise(InvalidRequestError('invalid command requested'))

    
        
application = webapp.WSGIApplication([('/articles', ArticleHandler)], debug = True)

        
if __name__ == '__main__':
    main(application)
