import logging

import urllib

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

from libs import xml_tools as XMLTools


class UploadURLHandler(webapp.RequestHandler):
    def get(self):
        upload_url = blobstore.create_upload_url('/images/post')

        xmlDoc = XMLTools.createXmlDoc('response')
        root = xmlDoc.documentElement

        node = XMLTools.genStringNode(xmlDoc, upload_url, 'upload-url')
        root.appendChild(node)

        node = XMLTools.genStringNode(xmlDoc,
                                      'multipart/form-data',
                                      'enctype')
        root.appendChild(node)

        resp_data = xmlDoc.toxml('utf-8')

        self.response.headers['Content-Type'] = 'text/xml'
        return self.response.out.write(resp_data)



class ImageUploadHandler(blobstore_handlers.BlobstoreUploadHandler):

    def post(self):
        upload_files = self.get_uploads('file')
        blob_info = upload_files[0]
        self.redirect('/images/get/%s' % blob_info.key())


class ImageDownloadHandler(blobstore_handlers.BlobstoreDownloadHandler):
    """ Stores and retrieves images. """

    def get(self, resource):
        resource = str(urllib.unquote(resource))
        blob_info = blobstore.BlobInfo.get(resource)
        self.send_blob(blob_info)
        
    
application = webapp.WSGIApplication(
    [('/images/get/([^/]+)?', ImageDownloadHandler),
     ('/images/post', ImageUploadHandler),
     ('/images/upload-url', UploadURLHandler)],
    debug = True)
        
        
def main():
    run_wsgi_app(application)

        
if __name__ == '__main__':
    main()

