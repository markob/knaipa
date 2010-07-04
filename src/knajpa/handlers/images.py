import logging as log

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from google.appengine.ext.webapp import template

# add gdata library to python path
import os, sys

sys.path.append(os.path.abspath(os.curdir) + '/../libs/gdata')

# import gdata images and service API
import gdata.photos.service as GDService

from xml.dom import minidom

# global properties definitions to deal with picasaweb

user_id = 'knaipa.service@gmail.com'
user_passwd = 'qaswedfrtghy'
album_id = 'default'

source_str = 'knaipa-knaipa-service'
image_name = 'Knaipa Service\'s Image'

photos_uri = 'http://picasaweb.google.com/data/feed/api'
album_uri = photos_uri + "/user/%s/albumid/%s" % (user_id, album_id)

template_path = os.path.join(os.path.dirname(__file__),
                             '../templates/image-post.xml')


class ImageHandler(webapp.RequestHandler):
    """ Forwards image to picasaweb service. """

    def post(self):
        try:
            photo_entry = self._post_image()
            photo_info = {'photo_url': photo_entry.GetMediaURL()}
            
            photo_xml = minidom.parseString(str(photo_entry))
            
            node = photo_xml.getElementsByTagName('ns1:albumid')            
            node = node[0].firstChild
            photo_info['album_id'] = node.nodeValue
            
            node = photo_xml.getElementsByTagName('ns1:id')
            node = node[0].firstChild
            photo_info['photo_id'] = node.nodeValue
            
            thumb_prefix = 'thumb_'
            thumbs_list = []
            for thumb in photo_entry.media.thumbnail:
                thumb_name = thumb_prefix + str(thumb.width) + 'x' + str(thumb.height)
                thumbs_list.append({'name': thumb_name, 'url': thumb.url})
                
            photo_info['thumbs_list'] = thumbs_list
            
            self.response.headers['Content-Type'] = 'text/xml'
            return self.response.out.write(
                template.render(template_path, photo_info))
        
        except:
            return self.error(404)
        
        
    def _post_image(self):
        img_handle = self.request.POST.get('image').file
        
        log.debug("Authorization is going")
        
        gd_client = GDService.PhotosService()
        gd_client.email = user_id
        gd_client.password = user_passwd
        gd_client.source = source_str
        gd_client.ProgrammaticLogin()
        
        log.debug("Image is posting")
        
        photo_entry = gd_client.InsertPhotoSimple(album_uri,
                                                  image_name,
                                                  None,
                                                  img_handle)
        
        log.debug("Image was posted with id %d" % photo_entry)
        
        return photo_entry

        
application = webapp.WSGIApplication(
    [('/image', ImageHandler)], debug = True)
        
        
def main():
    run_wsgi_app(application)

        
if __name__ == '__main__':
    main()
