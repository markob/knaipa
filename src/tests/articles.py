""" Checks base functionality of the articles engine """
import unittest
import urllib2

from xml.dom import minidom

# List of test cases

# 1) common service tests
#   a) get service url (get service info page)
class BaseArticleTest(unittest.TestCase):
    """ Checks common service functionality. """

    def getResponse(self, params):
        """ Requests appropriate data and retrieves DOM response object. """
        return urllib2.urlopen('http://localhost:8080/articles?' + params)
    
    
    def getResponseContent(self, params):
        """ Requests appropriate data and retrieves DOM response object """
        return minidom.parse(self.getResponse(params))


    def testInfoURL(self):
        """ 'articles?cmd=info' should return service info """
        response = self.getResponse('cmd=info')
        return self.assertTrue(200 <= response.code < 300)

        
# 2) 'get list of articles' service test
#   a) get a list of articles
class ArticlesGetListTest(BaseArticleTest):
    """ Checks 'get an articles list' functionality. """

    def testGetArticlesList(self):
        """ 'articles?cmd=list' should return the list of articles """
        dom = self.getResponseContent('cmd=list')

        root = dom.documentElement
        self.assertEquals('content', root.tagName)


# 3) article manipulation tests:
#   a) add a new article with bad data
#   b) update an existing article with bad data
#   d) try to remove an nonexisting article

# 3) get list of articles
#   a) get list of articles
class ArticleManipulationTest(BaseArticleTest):
    """ Checks articles manipualtion commands (get, add, del) """    
    
    def testGetArticle(self):
        """ 'cmd=get&id=<article_id> should return article or empty xml """
        dom = self.getResponseContent('cmd=get&id=0001')

        root = dom.documentElement
        self.assertEquals('content', root.tagName)


    def testDeleteArticle(self):
        """ 'cmd=del&id=<article_id>' should return deleted article id or empty xml """
        dom = self.getResponseContent('cmd=del&id=0001')

        root = dom.documentElement
        self.assertEquals('content', root.tagName)


    def testAddArticle(self):
        """ 'cmd=add' should return a created article id """
        dom = self.getResponseContent('cmd=add')

        root = dom.documentElement
        self.assertEquals('content', root.tagName)
        
        node = root.firstChild
        self.assertEquals('id', node.tagName)

        article_id = node.firstChild.data
        self.assertTrue(article_id)
    

if __name__ == '__main__':
    unittest.main()
