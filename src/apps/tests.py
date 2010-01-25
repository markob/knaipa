import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.api import urlfetch

from xml.dom import minidom


class AddArticleModelTest(webapp.RequestHandler):
    """ Just adds article model description. """

    def get(self):

        index = self.request.url.index(self.request.path)
        upload_url = self.request.url[0:index] + '/images/upload-url'
        result = urlfetch.fetch(upload_url)

        xmlDoc = minidom.parseString(result.content)

        nodeList = xmlDoc.getElementsByTagName('upload-url')
        upload_url = nodeList[0].firstChild.data

        nodeList = xmlDoc.getElementsByTagName('enctype')
        enctype = nodeList[0].firstChild.data
        
        response = """
        <html>
          <head>
            <title>Add Article</title>
          </head>
          <body>
            <form action=\"/article/\" method=\"post\">
              <input type=\"hidden\" name=\"cmd\" value=\"post\" />
              <p/>Knaipa:
              <input type=\"textarea\" name=\"knaipa\" />
              <p/>Title:
              <input type=\"textarea\" name=\"title\" />
              <p/>Description:
              <input type=\"textarea\" name=\"description\" />
              <p/>Text:
              <input type=\"textarea\" name=\"text\" />
              <p/>
              <input type=\"submit\" value=\"Post\" />
            </form>
            <p/>
            <form action=\"/article/\" method=\"get\">
              <input type=\"hidden\" name=\"cmd\" value=\"get\" />
              <p/>Id:
              <input type=\"textarea\" name=\"id\" />
              <p/>
              <input type=\"submit\" value=\"Get\" />
            </form>
            <p/>
            <form action=\"%s\" method=\"post\" enctype=\"%s\" />
              <p/>Image:
              <input type=\"file\" name=\"file\" />
              <p/>
              <input type=\"submit\" value=\"Upload\" />
            </form>            
          </body>
        </html>
        """ % (upload_url, enctype)
          
        return self.response.out.write(response)


application = webapp.WSGIApplication([('.*', AddArticleModelTest)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
