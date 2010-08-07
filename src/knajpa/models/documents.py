from knajpa.models.articles import Article

class IndexableDocument(Article):
    """ It's common descendant for all indexable documents.
        It is used as workaround for appengine polymodel poor functionality. """
    pass
