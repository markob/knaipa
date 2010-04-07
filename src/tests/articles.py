""" Checks base functionality of the articles engine """
import unittest
import urllib2

from xml.dom import minidom

# List of test cases

# 1) valid add/update/remove cases:
#   a) add a new article
#   b) update an existing article
#   c) remove an existing article

# 2) invalid cases:
#   a) add a new article with bad data
#   b) update an existing article with bad data
#   d) try to remove an nonexisting article

# 3) get list of articles
#   a) get list of articles
class GetListTest(unittest.TestCase):
    """ Checks getting a list of articles """
    
    def getResponse(self, params):
        """ Requests appropriate data and retrieves DOM response object. """
        return urllib2.urlopen('http://localhost:8080/articles?' + params)
    
    
    def getResponseContent(self, params):
        """ Requests appropriate data and retrieves DOM response object """
        return minidom.parse(self.getResponse(params))
    
    
    def testBaseURL(self):
        """ <site url>/articles request should retrieve 2xx response """
        response = self.getResponse('cmd=info')
        self.assertTrue(200 <= response.code < 299)
    
    
    def testResponseObject(self):
        """ articles?cmd=list response should have root tag named 'content' """
        dom = self.getResponseContent('cmd=list')
        
        root = dom.documentElement
        self.assertEquals(root.tagName, 'content')


if __name__ == '__main__':
    unittest.main()
