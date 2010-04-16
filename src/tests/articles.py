""" Checks base functionality of the articles engine """
import unittest
import urllib
import urllib2

from xml.dom import minidom

# List of test cases
class BaseArticleTest(unittest.TestCase):
    """ Checks common service functionality. """


    def getResponse(self, get_params, post_params=None):
        """ Requests appropriate data and response object. """
        url = 'http://localhost:8080/articles?' + get_params
        
        if post_params:
            data = urllib.urlencode(post_params)
            return urllib2.urlopen(url, data)
        
        return urllib2.urlopen(url)
    
    
    def getResponseContent(self, get_params, post_params=None):
        """ Requests appropriate data and retrieves DOM response object """
        return minidom.parse(self.getResponse(get_params, post_params))


# 1) common service tests
#   a) get service url (get service info page)
class ArticleInfoTest(BaseArticleTest):
    """ Checks common service functionality. """


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
        data = { 'services': 'service#1',
                 'title': 'Knajpa',
                 'description': 'Just a knajpa',
                 'cut': 'Just a knajpa',
                 'text': 'Text about knajpa. Just a text.',
                 'author': 'Guest' }
        
        dom = self.getResponseContent('cmd=add', data)

        root = dom.documentElement
        self.assertEquals('content', root.tagName)
        
        nodes = dom.getElementsByTagName('id')
        self.assertEquals('id', nodes[0].tagName)

        article_id = nodes[0].firstChild.data
        self.assertTrue(article_id)
    

if __name__ == '__main__':
    unittest.main()
