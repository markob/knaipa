import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from libs.models.article import Article
from libs.utils import ModelProcessor, InvalidRequestError

from xml.dom import minidom
from libs import xml_tools as XMLTools


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
            handler = self._get_cmd_handler()
            resp_data = handler(self.request)

        except InvalidRequestError, err:
            self.error(404)

        self.response.headers['Content-Type'] = 'text/xml'
        return self.response.out.write(resp_data)


    def _get_cmd_handler(self):
        """ Selects appropriate handler for the requested command. """

        cmd = self.request.get('cmd')
        
        if 'post' == cmd:
            return self._store_article
        elif 'get' == cmd:
            return self._read_article
        else:
            raise(InvalidRequestError('invalid command requested'))


    def _store_article(self, request):
        """ Stores an article from request and retieves it id. """

        key = self._write_article(request)

        xmlDoc = XMLTools.createXmlDoc('response')
        root = xmlDoc.documentElement

        node = XMLTools.genStringNode(xmlDoc, key, 'id')
        root.appendChild(node)
        
        return xmlDoc.toxml('utf-8');


    def _write_article(self, request):
        """ Parses request data and store article object. """
    
        key = request.get('id')
        processor = ModelProcessor(Article)
        
        if key:
            # get article from datastore
            article = self._get_article(key)
            
            #update the article
            processor.update_from_request(request, article)
        else:
            # create new article
            article = processor.create_from_request(request)

        # save article
        article.put()
            
        return str(article.key())


    def _read_article(self, request):
        """ Retrieves requested article from datastore. """

        key = request.get('id')

        if not key:
            raise(InvalidRequestError('invalid article id requested'))

        article = self._get_article(key)

        processor = ModelProcessor(Article)
        
        return processor.gen_xml(article)


    def _get_article(self, key):
        """ Retrieves article with the specified key from datastore. """
        
        article = Article.get(key)
        if not article:
            raise(InvalidRequestError('requested article does not exists'))

        return article
    
    
application = webapp.WSGIApplication(
    [('.*', ArticleHandler)], debug = True)
        
        
def main():
    run_wsgi_app(application)

        
if __name__ == '__main__':
    main()
