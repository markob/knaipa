""" Checks base functionality of the services engine """
import unittest
import urllib

from xml.dom import minidom

# List of test cases

# 1) valid add/update/remove cases:
#   a) add a new base service
#   b) add a new extended service
#   c) update an existing service data
#   d) remove an existing service

# 2) invalid cases:
#   a) add a new base service with bad data
#   b) add a new extended service with bad data
#   c) update an existing service with bad data
#   d) remove nonexisting service

# 3) get list of services
#   a) get list of services
class GetListTest(unittest.TestCase):
    """ Checks getting a list of services """
    
    def testListSyntax(self):
        """ services?cmd=list should return a list of services or empty list """
        http = urllib.urlopen('http://localhost:8080/services?cmd=list')
        dom = minidom.parse(http)
        
        print(dom)


if __name__ == '__main__':
    unittest.main()
