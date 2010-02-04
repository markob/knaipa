# Auth Request: POST request to url:
#  https://www.google.com/accounts/ClientLogin
# with following params:
# - accountType: GOOGLE (get authorization for Google account only)
# - email: user's full email address
# - passwd: password
# - service: name of Google service (lh2 for picasaweb)
# - source: short string identifying application, in loggin purposes; should
# have a form "companyName-applicationName-versionID"
# - loginToken: optional; token representing the specific CAPTCHA challenge
# - loginCaptcha: optional; string entered by user as an answer to a CAPTCHA
# challenge

import urllib

from google.appengine.api import urlfetch


login_url = 'https://www.google.com/accounts/ClientLogin'

login_form_fields = {'accountType': 'GOOGLE',
                     'Email': 'knaipa.service@gmail.com',
                     'Passwd': 'qaswedfrtghy',
                     'service': 'lh2',
                     'source': 'knaipa-knaipa-dev-6'}

login_form_data = urllib.urlencode(login_form_fields)


def login():
    response = urlfetch.fetch(url=login_url,
                              payload=login_form_data,
                              method=urlfetch.POST,
                              headers={'Content-Type':
                                       'application/x-www-form-urlencoded'})

    auth_shift = response.content.index('Auth=')
    auth_tooken = response.content[auth_shift + 5:]
    
    return auth_tooken


def get_photos_list():
    url = 'http://picasaweb.google.com/data/feed/api/user/knaipa.service/albumid/default'

    response = urlfetch.fetch(url=url,
                              headers={'Authorization':
                                       'GoogleLogin auth=%s' % login()})

    return response.content
