import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

from libs.models.article import Article
from libs.utils import ModelProcessor, InvalidRequestError

from xml.dom import minidom
from libs import xml_tools as XMLTools

import os


templates_path = os.path.join(os.path.dirname(__file__), '../templates')


class ArticleHandler(webapp.RequestHandler):
    """ Adapts article and stores it to data storage. """

    def get(self):
        """ Just hooks all GET requests and passes it to processor. """
        
        return self._handle_request()


    def post(self):
        """ Just hooks all POST requests and passes it to processor. """

        return self._handle_request()


    def _handle_request(self):
        """ Processes input request and creates appropriate reqponse. """

        try:
            handler, template_name = self._get_cmd_handler()
            resp_data = handler(self.request)

            template_path = os.path.join(templates_path, template_name)
            
            self.response.headers['Content-Type'] = 'text/xml'
            return self.response.out.write(
                template.render(template_path, resp_data))

        except InvalidRequestError, err:
            return self.error(404)


    def _get_cmd_handler(self):
        """ Selects appropriate handler for the requested command. """

        cmd = self.request.get('cmd')
        
        if 'post' == cmd:
            return (self._write_article, 'article-post.xml')
        elif 'get' == cmd:
            return (self._read_article, 'article-get.xml')
        elif 'list' == cmd:
            return (self._get_articles_list, 'articles-list.xml')
        else:
            raise(InvalidRequestError('invalid command requested'))


    def _write_article(self, request):
        """ Parses request data and store article object. """
    
        article_id = request.get('id')
        processor = ModelProcessor(Article)
        
        if article_id:
            # get article from datastore
            article = self._get_article(article_id)
            
            #update the article
            processor.update_from_request(request, article)
        else:
            # create new article
            article = processor.create_from_request(request)

        # save article
        article.put()
            
        return {'article_id': article.key().id()}


    def _read_article(self, request):
        """ Retrieves requested article from datastore. """

        article_id = request.get('id')

        if not article_id:
            raise(InvalidRequestError('invalid article id requested'))

        article = self._get_article(article_id)
        
        return {'article':
                ModelProcessor(Article).gen_model_data(article)}


    def _get_article(self, id):
        """ Retrieves article with the specified key from datastore. """
        
        article = Article.get_by_id(int(id))
        if not article:
            raise(InvalidRequestError('requested article does not exists'))

        return article


    def _get_articles_list(self, request):
        """ Retieves a list of all articles. """

        articles = Article.all()
        articles_list = []

        model_processor = ModelProcessor(Article)
        
        for article in articles:
            articles_list.append(model_processor.gen_model_data(article))
                    
        return {'articles_list': articles_list}
    
    
application = webapp.WSGIApplication(
    [('/article', ArticleHandler)], debug = True)
        
        
def main():
    run_wsgi_app(application)

        
if __name__ == '__main__':
    main()
