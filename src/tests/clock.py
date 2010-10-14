from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import datetime
import tests.models as models

class ClockTest(webapp.RequestHandler):

    def get(self):
        time = datetime.datetime.now()
        user = users.get_current_user()

        if not user:
            navbar = ("<p>Welcome! <a href=\"%s\">Sign in or register</a> to customize.</p>" % (users.create_login_url(self.request.path)))

            tzForm = ''
        else:
            navbar = ("Welcome %s! You can <a href=\"%s\">sign out</a>.</p>" % (user.email(), users.create_logout_url(self.request.path)))

            userPrefs = models.GetUserPrefs()
            
            tzForm = """
            <form method=\"post\">
              <label for=\"tz_offset\">
                Timezone offset from UTC (can be negative):
              </label>
              <input name=\"tz_offset\" id=\"tz_offset\" type=\"text\"
                size=\"4\" value=\"%d\" />
              <input type=\"submit\" value=\"Set\" />
            </form>
            """ % userPrefs.tzOffset

            time += datetime.timedelta(0, 0, 0, 0, 0, userPrefs.tzOffset)

        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write("""
        <html>
          <head>
            <title>The Time Is...</title>
          </head>
          <body>
            %s
            <p>The time is: %s</p>
            %s
          </body>
        </html>""" % (navbar, str(time), tzForm))


    def post(self):
        userPrefs = models.GetUserPrefs()

        try:
            tzOffset = int(self.request.get('tz_offset'))
            userPrefs.tzOffset = tzOffset
            userPrefs.put()
        except ValueError:
            pass

        self.redirect('/tests/clock')


application = webapp.WSGIApplication([('/tests/clock', ClockTest)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
