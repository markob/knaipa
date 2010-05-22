"""It's the wrapper for 'whoosh storage'. It imlements functionality to store
    indices to appengine storage."""

import logging

from libs.whoosh.store import Storage


########################################################################
class GAE_Storage(Storage):
    """Implementation of 'whoosh.store.Storage' to store index into GAE db."""

    #----------------------------------------------------------------------
    def create_index(self):
        """Creates and returns an object implementing 'whoosh.index.Index'
           interface."""
        
        return index
    
    
    #----------------------------------------------------------------------
    def open_index(self):
        """Returns an object implementing 'whoosh.index.Index' interface."""
        
        return index