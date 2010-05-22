""""""
import logging

from libs.whoosh.index import Index
from src.libs.whoosh.writing import IndexWriter


class GAE_IndexWriter(IndexWriter):
    """"""
    
    def add_document(self):
        """Adds a new document to the index."""
        pass
    

    def delete_document(self, docnum):
        """Deletes a document by its number."""
        pass
    
    
    def update_document(self, **fields):
        """"""
        pass
    
    
    def commit(self):
        """Saves the additions/deletions done with this IndexWriter to the main index,
           and release any resources used by the IndexWriter."""
        pass
    
    
    def cancel(self):
        """Throws away any additions/deletions done with this IndexWriter,
           and release any resources used by the IndexWriter."""
        pass
