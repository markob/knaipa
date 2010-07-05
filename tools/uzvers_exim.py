# -*- coding: utf-8 -*-

from datetime import datetime
from google.appengine.ext import db
from google.appengine.tools.bulkloader import Loader, Exporter
from libs.uzvers import Uzver

class UzverLoader(Loader):
    """ Uzver Model entities loader. """
    
    def __init__(self):
        str_to_text = lambda x: x.decode('utf-8')
        str_to_date = lambda x: datetime.strptime(x, '%m %d %Y %H:%M')
        
        Loader.__init__(self, 'Uzver',
                        [('first_name', str_to_text),
                         ('last_name', str_to_text),
                         ('nick_name', str_to_text),
                         ('email', str_to_text),
                         ('password', str_to_text),
                         ('avatar', str_to_text),
                         ('created', str_to_date)
                        ])


class UzverExporter(Exporter):
    """ Uzver Model entities exporter. """

    def __init__(self):
        text_to_str = lambda x: x.encode('utf-8')
        date_to_str = lambda x: x.strftime('%m %d %Y %H:%M')

        Exporter.__init__(self, 'Uzver',
                          [('first_name', text_to_str, None),
                           ('last_name', text_to_str, None),
                           ('nick_name', text_to_str, None),
                           ('email', text_to_str, None),
                           ('password', text_to_str, None),
                           ('created', date_to_str, None)
                          ])
                                   

loaders = [UzverLoader]
exporters = [UzverExporter]
