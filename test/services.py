'''
Created on Aug 7, 2010

@author: apetrenko
'''
import unittest
from knajpa.models.articles import Article
from knajpa.models.restaurant import Knajpa, Address
import logging


class TestServiceKnajpa(unittest.TestCase):


    def testAddNewKnajpa(self):
        
        knajpa = Knajpa(name= 'TestKnajpa')
        knajpa.put()
        
        Address(knajpa,ja=0.098,ia=0.13 ,address='123 First Ave., Seattle, WA, 98101').put()
        
        
        for item in Knajpa.all():
            logging.info('Knajpa name'+item.name);
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testAddNewKnajpa']
    unittest.main()