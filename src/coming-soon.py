from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from datetime import datetime, timedelta, time
from xml.dom import minidom

# Starting date for service in format (year, month, day)
startTime = datetime(year=2009, month=8, day=15, hour=12)


class ComingSoon(webapp.RequestHandler):
    """ Temporary stub retrieves time reminding to service start. """

    def get(self):
        """ Get request handler. Sends XML response with time reminding to
            service start. """
            
        self.response.headers["Content-Type"] = "text/xml"
        self.response.out.write(self.__createResponseXML())
        
            
    def __createResponseXML(self):
        """ Creates XML DOM object and fills it in with appropriate data.
            Retrieves completed XML string as a result.
        """
        
        doc = minidom.Document()
        
        root = doc.createElement('coming-soon')
        doc.appendChild(root)
        
        timeToStart = self.__getTimeToStart()
        
        node = doc.createElement('days')
        node.setAttribute('value', str(timeToStart.days))
        root.appendChild(node)
        
        node = doc.createElement('hours')
        node.setAttribute('value', str(timeToStart.seconds/3600))
        root.appendChild(node)
        
        node = doc.createElement('minutes')
        node.setAttribute('value', str((timeToStart.seconds%3600)/60))
        root.appendChild(node)
        
        node = doc.createElement('seconds')
        node.setAttribute('value', str(timeToStart.seconds%60))
        root.appendChild(node)
        
        return doc.toxml('utf-8')
        
        
    def __getTimeToStart(self):
        """ Calculates and retrieves time reminding to service start. """
        
        nowTime = datetime.today()
        return startTime - nowTime



# Declaration of WSGI application. Currently only one request handler
# works with all requests.
application = webapp.WSGIApplication([('/.*', ComingSoon)], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
