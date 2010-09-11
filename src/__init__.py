import os,logging   ,sys
logging.getLogger().setLevel(logging.DEBUG)

logging.debug(os.path.dirname(__file__))
sys.path.append(os.path.dirname(__file__))
