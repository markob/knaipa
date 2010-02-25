import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from libs.utils import InvalidRequestError

# add gdata library to python path
import os, sys

sys.path.append(os.path.abspath(os.curdir) + '/../libs/gdata')

# import gdata images and service API
from gdata.photos import service as GDService
from gdata import media as GDMedia

user_id = 'knaipa.service@gmail.com'
user_passwd = 'qaswedfrtghy'
album_id = 'default'

source_str = 'knaipa-knaipa-dev_7'
image_name = 'Knaipa Service\'s Image'

photos_uri = 'http://picasaweb.google.com/data/feed/api'
album_uri = photos_uri + "/user/%s/albumid/%s" % (user_id, album_id)


class ImageHandler(webapp.RequestHandler):
    """ Forwards image to webpicasa service. """

    def post(self):
        img_handle = self.request.POST.get('image').file
        
        #content_type = img_handle.
        
        gd_client = GDService.PhotosService()
        gd_client.email = user_id
        gd_client.password = user_passwd
        gd_client.source = source_str
        gd_client.ProgrammaticLogin()
        
        #logging.info("Image content type is %s.\n" % content_type)
        
        photo_entry = gd_client.InsertPhotoSimple(album_uri,
                                                  image_name,
                                                  None,
                                                  img_handle)
        
        return self.response.out.write(photo_entry.GetMediaURL())

        
application = webapp.WSGIApplication(
    [('/image', ImageHandler)], debug = True)
        
        
def main():
    run_wsgi_app(application)

        
if __name__ == '__main__':
    main()
