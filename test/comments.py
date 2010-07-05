""" Checks base functionality of the comments engine """
import unittest
import base_service as baseServiceTests


class CommentsInfoTest(baseServiceTests.ServiceTest):
    """ Checks common service functionality. """

    def setUp(self):
        """ Initializes test with service specific data """
        self._url_ = 'http://localhost:8080/comments'
        self._data_ = { 'services': 'Test Service',
                        'title': 'Test Restaurant',
                        'description': 'It is just a test content.',
                        'cut': 'It may be same as description or may be not.',
                        'text': 'This is text about the restaurant. But it is also a mock.',
                        'author': 'Anonymous' }

        
if __name__ == '__main__':
    unittest.main()
