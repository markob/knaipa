import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from libs.models.articles import Article
from libs.objhandler import ObjectHandler
from libs.utils import InvalidRequestError


class ArticleHandler(ObjectHandler):
    """ Adapts article and stores it to data storage. """

    def __init__(self):
        ObjectHandler.__init__(self, Article)
    
    
    def _select_cmd_handler(self):
        """ Selects appropriate handler for the requested command. """

        cmd = self.request.get('cmd')

        # get list of all articles (short info and id)
        if 'list' == cmd:
            return (self._get_list, 'articles-list.xml')
        # add new article to storage (for authorized users only)
        elif 'add' == cmd:
            return (self._write, 'articles-add.xml')
        # get article with the specified article id
        elif 'get' == cmd:
            return (self._read, 'articles-get.xml')
        # remove article with the specified id from storage (for authorized users only)
        elif 'del' == cmd:
            return (self._delete, 'articles-del.xml')
        # get static info about articles service
        elif 'info' == cmd:
            return (lambda self: None, 'articles-info.xml')
        # return 404 error in all other cases
        else:
            raise(InvalidRequestError('invalid command requested'))

    
        
application = webapp.WSGIApplication(
    [('/articles', ArticleHandler)], debug = True)
        
        
def main():
    run_wsgi_app(application)

        
if __name__ == '__main__':
    main()
