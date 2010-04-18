from libs.models.uzvers import Uzver as UserModel
from google.appengine.ext import db


class Uzver(object):
    """ It's helper class to manipulate user instances. """

    def __init__(self, user_data, is_new=True):
        """ Creates new user or loads an existing user data from datastore """
        if is_new:
            # Create new user but check for duplicates first
            query = UserModel.get
