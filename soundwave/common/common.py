from __future__ import print_function
import sys
import os
import logging
from dotenv import load_dotenv
load_dotenv()

mu = 0.00001

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"),
                    format='%(levelname)s {%(filename)s:%(lineno)d} (%(threadName)-9s) %(message)s',)