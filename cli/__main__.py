from common.common import getEnvironmentVariables
from soundwave.soundwave import Soundwave
import logging
import os
import sys

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"),
                    format='%(levelname)s {%(filename)s:%(lineno)d} (%(threadName)-9s) %(message)s',)


if __name__ == '__main__':
    try:
        logging.info('Starting...')
        soundwave = Soundwave()

        parameters = getEnvironmentVariables()

        if parameters['mode'] == 'prerecorded':
            soundwave.process_prerecorded(parameters['device'], parameters['inputFile'],
                                          parameters['targetFile'], parameters['size'], parameters['algorithm'])
        elif parameters['mode'] == 'live':
            soundwave.process_anc(parameters['device'],
                                  parameters['targetFile'], parameters['algorithm'], parameters['role'], parameters['waitSize'], parameters['stepSize'], parameters['size'], parameters['tuiConnection'])

        logging.info('Finished!')
    except KeyboardInterrupt:
        exit('\nInterrupted by user')
    except Exception as e:
        exit(type(e).__name__ + ': ' + str(e))
