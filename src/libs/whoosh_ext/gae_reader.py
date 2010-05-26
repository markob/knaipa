"""Implementation of DocReader interface for Whoosh to read documents from GAE storage."""

import logging

from libs.whoosh.reading import IndexReader as Reader


class GAE_Reader(Reader):
    """"""
    
    # required interface methods
    def __getitem__(self):
        pass
    
    
    def __iter__(self):
        pass

    
    def doc_count_all(self):
        pass
    
    
    def doc_count(self):
        pass
    
    
    def field_length(self, fieldid):
        pass
    
    
    def doc_field_length(self, docnum, fieldid):
        pass
    
    
    def doc_field_lengths(self, docnum):
        pass
    
    
    def vector(self, docnum, fieldid):
        pass
    
    
    def vector_as(self, astype, docnum, fieldid):
        pass
    

    # optional interface methods
    def close(self):
        pass
    