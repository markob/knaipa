import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.api import urlfetch

from xml.dom import minidom


class AddArticleModelTest(webapp.RequestHandler):
    """ Just adds article model description. """

    def get(self):
        
        response = """
        <html>
          <head>
            <title>Add Article</title>
          </head>
          <body>
            <form action=\"/article\" method=\"post\">
              <input type=\"hidden\" name=\"cmd\" value=\"post\" />
              <p/>Knaipa:
              <input type=\"textarea\" name=\"knaipa\" />
              <p/>Title:
              <input type=\"textarea\" name=\"title\" />
              <p/>Description:
              <input type=\"textarea\" name=\"description\" />
              <p/>Cut:
              <input type=\"textarea\" name=\"cut\" />
              <p/>Text:
              <input type=\"textarea\" name=\"text\" />
              <p/>
              <input type=\"submit\" value=\"Post\" />
            </form>
            <p/>
            <form action=\"/article\" method=\"get\">
              <input type=\"hidden\" name=\"cmd\" value=\"get\" />
              <p/>Id:
              <input type=\"textarea\" name=\"id\" />
              <p/>
              <input type=\"submit\" value=\"Get\" />
            </form>
            <form action=\"/image\" enctype=\"multipart/form-data\" method=\"post\">
              <p/>Image:
              <input type=\"file\" name=\"image\" />
              <p/>
              <input type=\"submit\" value=\"Upload\" />
            </form>

          </body>
        </html>
        """
          
        return self.response.out.write(response)


application = webapp.WSGIApplication([('.*', AddArticleModelTest)],
                                     debug=True)

def main():
	run_wsgi_app(application)

if __name__ == '__main__':
	main()
