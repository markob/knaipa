import logging

from google.appengine.ext import webapp
from libs.models.article import Article
from google.appengine.api import db


class ArticleAdder(webapp.RequestHandler):
    """ Adapts article and stores it to data storage. """

    def post(self):
        """ Extracts article from DataStore and retrieves it
        in XML format. """

        article = new Article()
        article.text = self.request.get('text')
        article.put()

        return self.response.write



class ArticleGetter(webapp.RequestHandler):
    """ Retrieves approptiate article by its key. """

    def get(self):
        key = self.request.get('id')
        article = db.get(key)
        return self.response.write()


application = webapp.WSGIApplication(
    [('/add/', AddArticle),
     ('/get/', GetArticle)],
    debug = True)
        
        
def main():
    webapp.util.run_wsgi_app(application)

        
if __name__ == '__main__':
    main()
