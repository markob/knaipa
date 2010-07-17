from knajpa.handlers.objhandler import ObjectHandler
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from knajpa.models.knajpamodel import Knajpa

class KnajpaHandler(ObjectHandler):
    def __init__(self):
        ObjectHandler.__init__(self, Knajpa)


application = webapp.WSGIApplication(
                [('/knajpa', KnajpaHandler)], debug=True)


def main():
    run_wsgi_app(application)


if __name__ == '__main__':
    main()
