import logging

from google.appengine.ext import webapp
from libs.models.article import Article
from google.appengine.api import db


class ArticleHandler(webapp.RequestHandler):
    """ Adapts article and stores it to data storage. """

    def get(self):
        command = self.request.get('cmd')
        if not cmd:
            
        article = db.get(key)

        self.response.headers['Content-Type'] = 'text/xml'
        return self.response.out.write(self.__getArticleXML())


    def post(self):
        """ Extracts article from DataStore and retrieves it
        in XML format. """

        article = new Article()
        article.text = self.request.get('text')
        article.put()

        self.response.headers['Content-Type'] = 'text/xml'
        return self.response.out.write(self.__getKeyXML());


    def _parse_request(self):
        """ Extracts request params and validate them. """
        self._request['cmd'] = self.request.get('cmd')
        


application = webapp.WSGIApplication(
    [('.*', ArticleHandler)], debug = True)
        
        
def main():
    webapp.util.run_wsgi_app(application)

        
if __name__ == '__main__':
    main()
