import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from libs.models.comment import Comment
from libs.objhandler import ObjectHandler
from libs.utils import InvalidRequestError


class CommentHandler(ObjectHandler):
    """ Adapts comment and stores it to data storage. """


    def _select_cmd_handler(self):
        """ Selects appropriate handler for the requested command. """

        cmd = self.request.get('cmd')
        
        if 'post' == cmd:
            return (self._write, 'comment-post.xml')
        elif 'get' == cmd:
            return (self._read, 'comment-get.xml')
        elif 'list' == cmd:
            return (self._get_list, 'comment-list.xml')
        else:
            raise(InvalidRequestError('invalid command requested'))

    
    
application = webapp.WSGIApplication(
    [('/comment', CommentHandler)], debug = True)
        
        
def main():
    run_wsgi_app(application)

        
if __name__ == '__main__':
    main()
