from __future__ import print_function
import sys
import os
import logging
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"),
                    format='%(levelname)s (%(threadName)-9s) %(message)s',)

def log_error(errorMsg):
    logging.error(errorMsg)