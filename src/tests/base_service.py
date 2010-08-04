""" Checks base functionality of the service engine """
import unittest
import urllib
import urllib2

from xml.dom import minidom


# List of test cases
class ServiceTest(unittest.TestCase):
    """ Checks common service functionality. """
    _url_ = None
    _data_ = None


    def getResponse(self, get_params, post_params=None):
        """ Requests appropriate data and response object. """
        url = self._url_ + '?' + get_params
        
        if post_params:
            data = urllib.urlencode(post_params)
            return urllib2.urlopen(url, data)
        
        return urllib2.urlopen(url)
    
    
    def getResponseContent(self, get_params, post_params=None):
        """ Requests appropriate data and retrieves DOM response object """
        return minidom.parse(self.getResponse(get_params, post_params))


    def testInfoURL(self):
        """ '?cmd=info' should return service info """
        response = self.getResponse('cmd=info')
        return self.assertTrue(200 <= response.code < 300)


    def testGetItemsList(self):
        """ '?cmd=list' should return the list of the service items """
        dom = self.getResponseContent('cmd=list')

        root = dom.documentElement
        self.assertEquals('content', root.tagName)


    def testGetItem(self):
        """ 'cmd=get&id=<item_id> should return an item or empty xml """
        dom = self.getResponseContent('cmd=get&id=0001')

        root = dom.documentElement
        self.assertEquals('content', root.tagName)


    def testDeleteItem(self):
        """ 'cmd=del&id=<item_id>' should return deleted item id or empty xml """
        dom = self.getResponseContent('cmd=del&id=0001')

        root = dom.documentElement
        self.assertEquals('content', root.tagName)


    def testAddItem(self):
        """ 'cmd=add' should return a created item id """        
        dom = self.getResponseContent('cmd=add', self._data_)

        root = dom.documentElement
        self.assertEquals('content', root.tagName)
        
        nodes = dom.getElementsByTagName('id')
        self.assertEquals('id', nodes[0].tagName)

        item_id = nodes[0].firstChild.data
        self.assertTrue(item_id)


    # this test doesn't look as enough simple and currently it's skipped
    ##def testUpdateArticle(self):
        """ 'cmd=add&id=<article_id>' with specified id should update the article """
        # fisrst we should add an article to the service and extract it id
        ##dom = self.getResponseContent('cmd=add', self._getTestArticleData())

        ##root = dom.documentElement
        ##nodes = dom.getElementsByTagName('id')
        ##article_id = nodes[0].firstChild.data

        # end now get the article data
        ##dom = self.getResponseContent('cmd=get&id=%s' % article_id)
