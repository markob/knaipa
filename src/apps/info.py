from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from datetime import date

from libs.models.info import Knaipa
from libs.models.person import PersonInfo
from libs.models.article import Article

from libs.utils import DataMapperUtils

class GetFullInfo(webapp.RequestHandler):
    """ This handler is responsible for insertion of a new item to the store. """
    
    def get(self):
        allPersons = PersonInfo.all()

        personExists = False
        for person in allPersons:
            if person.firstName == 'Marko' and person.secondName == 'Black':
                existsExists = True
                break

        if not personExists:
            person = PersonInfo(
                firstName="Marko",
                secondName="Black",
                nickName="tanatos",
                bornDate=date(1982, 8, 19),
                sex="male")

            person.put()

        allArticles = Article.all()

        article = None

        if allArticles.count() == 0:
            article = Article(
                text = "Bla-bla-bla, bla-bla, bla-bla, bla-bla-blaaaaa!",
                author = person)
            article.put()
        else:
            article = allArticles.get()
            article.delete()
    
        self.response.headers["Content-Type"] = "text/xml"
        
        return self.response.out.write(DataMapperUtils.genXML(article))
    

application = webapp.WSGIApplication([('.*', GetFullInfo)], debug=True)

def main():
    run_wsgi_app(application)
    

if __name__ == '__main__':
    main()
