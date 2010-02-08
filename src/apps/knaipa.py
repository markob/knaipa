import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

from libs.models.knaipa import Knaipa
from libs.utils import ModelProcessor, InvalidRequestError

from xml.dom import minidom
from libs import xml_tools as XMLTools

import os


templates_path = os.path.join(os.path.dirname(__file__), '../templates')


class KnaipaHandler(webapp.RequestHandler):
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


    def _put(self, request):
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


    def _get(self, request):
        """ Retrieves requested knaipa from datastore. """

        _id = request.get('id')

        if not _id:
            raise(InvalidRequestError('invalid article id requested'))

        entity = self._check_and_get(article_id)
        
        return {'knaipa':
                ModelProcessor(Knaipa).gen_model_data(entity)}


    def _check_and_get(self, id):
        """ Retrieves article with the specified key from datastore. """
        
        article = Article.get_by_id(int(id))
        if not article:
            raise(InvalidRequestError('requested article does not exists'))

        return article


    def _get_list(self, request):
        """ Retieves a list of all knaipas. """

        knaipas = Knaipa.all()
        knaipas_list = []

        model_processor = ModelProcessor(Knaipa)
        
        for knaipa in knaipas:
            knaipas_list.append(model_processor.gen_model_data(knaipa))
                    
        return {'knaipas_list': knaipas_list}
    
    
application = webapp.WSGIApplication(
    [('/knaipa', KnaipaHandler)], debug = True)
        
        
def main():
    run_wsgi_app(application)

        
if __name__ == '__main__':
    main()
