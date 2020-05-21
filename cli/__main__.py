from common.common import getEnvironmentVariables
from diminish.diminish import Diminish
import logging
import os
import sys


# the logging for CLI is set at a global level rather than using a logger like TUI
# this could be improved, but not believed to be necessary.
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"),
                    format='%(levelname)s {%(filename)s:%(lineno)d} (%(threadName)-9s) %(message)s',)


if __name__ == '__main__':
    try:
        logging.info('Starting...')
        diminish = Diminish()

        parameters = getEnvironmentVariables()

        # prercorded mode is used to test the algorithm against a predefined input and target
        # live is used to test with the full implmentation (error microphone + reference microphone
        # please see README for documentation of each environment variable parameter
        if parameters['mode'] == 'prerecorded':
            diminish.process_prerecorded(
                parameters['device'], parameters['inputFile'], parameters['targetFile'], parameters['size'], parameters['algorithm'])
        elif parameters['mode'] == 'live':
            diminish.process_anc(
                parameters['device'], parameters['targetFile'], parameters['algorithm'], parameters['role'],
                parameters['waitSize'], parameters['stepSize'], parameters['size'], parameters['tuiConnection'])

        logging.info('Finished!')
    except KeyboardInterrupt:
        exit('\nInterrupted by user')
    except Exception as e:
        exit(type(e).__name__ + ': ' + str(e))
