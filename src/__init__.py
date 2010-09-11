import os,sys
import logging as log

# store application root
APP_ROOT_PATH = os.path.abspath(os.path.dirname(__file__) + "/..")

# add application sources to system path
sys.path.append(APP_ROOT_PATH + "/src")
# add libraries to system path
sys.path.append(os.path.abspath(APP_ROOT_PATH + "/libs"))