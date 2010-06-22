# -*- coding: utf-8 -*-

from datetime import datetime
from google.appengine.ext import db
from google.appengine.tools.bulkloader import Loader, Exporter
from libs.models.articles import Article

class ArticleLoader(Loader):
    """ Article Model entities loader. """
    
    def __init__(self):
        str_to_text = lambda x: x.decode('utf-8')
        str_to_date = lambda x: datetime.strptime(x, '%m %d %Y %H:%M')
        
        Loader.__init__(self, 'Article',
                        [('title', str_to_text),
                         ('description', str_to_text),
                         ('cut', str_to_text),
                         ('text', str_to_text),
                         ('modified', str_to_date)
                        ])


class ArticleExporter(Exporter):
    """ Article Model entities exporter. """

    def __init__(self):
        text_to_str = lambda x: x.encode('utf-8')
        date_to_str = lambda x: x.strftime('%m %d %Y %H:%M')

        Exporter.__init__(self, 'Article',
                          [('title', text_to_str, None),
                           ('description', text_to_str, None),
                           ('cut', text_to_str, None),
                           ('text', text_to_str, None),
                           ('modified', date_to_str, None)
                          ])
                                   

loaders = [ArticleLoader]
exporters = [ArticleExporter]
