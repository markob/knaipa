""" Current file contains functionality to handle search requests from user. """

import logging as log

class SearchHandler(object):
    """Handles search request by using full text search functionality"""
    
    def __init__(self):
        log.debug("Search handler initialization")
