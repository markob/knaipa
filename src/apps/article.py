import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from libs.models.article import Article
from libs.utils import ObjectHandler, InvalidRequestError


class ArticleHandler(ObjectHandler):
    """ Adapts article and stores it to data storage. """

    def __init__(self):
        ObjectHandler.__init__(self, Article)

    
    def _get_cmd_handler(self):
        """ Selects appropriate handler for the requested command. """

        cmd = self.request.get('cmd')
        
        if 'post' == cmd:
            return (self._write, 'article-post.xml')
        elif 'get' == cmd:
            return (self._read, 'article-get.xml')
        elif 'list' == cmd:
            return (self._get_list, 'articles-list.xml')
        else:
            raise(InvalidRequestError('invalid command requested'))

    
        
application = webapp.WSGIApplication(
    [('/article', ArticleHandler)], debug = True)
        
        
def main():
    run_wsgi_app(application)

        
if __name__ == '__main__':
    main()
