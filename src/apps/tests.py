import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from libs.models.object import ObjectScheme


class AddArticleModelTest(webapp.RequestHandler):
    """ Just adds article model description. """

    def get(self):
        # try to get stored object scheme for 'article'
        query = db.Query(ObjectScheme)

        if 0 == query.count():
            msg = "Article object description doesn't exist."

            query = ObjectScheme(name='article')
            query.objects.append('author')
            query.objects.append('description')
            query.objects.append('text')

            query.put()
        else:
            query = query.get()
            
            msg = "Article object type description already exists."
            msg = "%s</p>Name: %s" % (msg, query.name)

            for attr in query.objects:
                msg = "%s</p>Attribute: %s" % (msg, attr)

        return self.response.out.write(msg);


application = webapp.WSGIApplication([('.*', AddArticleModelTest)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
