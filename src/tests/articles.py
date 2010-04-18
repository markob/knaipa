""" Checks base functionality of the articles engine """
import unittest
from base_test import ServiceTest


base_url = 'http://localhost:8080/articles'


# 1) common service tests
#   a) get service url (get service info page)
class ArticleInfoTest(ServiceTest):
    """ Checks common service functionality. """

    def setUp(self):
        """ Initializes test with service specific data """
        self._url_ = base_url
        self._data_ = { 'services': 'Test Service',
                        'title': 'Test Restaurant',
                        'description': 'It is just a test content.',
                        'cut': 'It may be same as description or may be not.',
                        'text': 'This is text about the restaurant. But it is also a mock.',
                        'author': 'Anonymous' }

        
if __name__ == '__main__':
    unittest.main()
