from common.common import getEnvironmentVariables, parseCliParameters
from soundwave import app
import logging
import os
import sys

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"),
                    format='%(levelname)s {%(filename)s:%(lineno)d} (%(threadName)-9s) %(message)s',)


if __name__ == '__main__':
    try:
        if len(sys.argv) == 1:
            parameters = getEnvironmentVariables()
        else:
            parameters = parseCliParameters(sys.argv)

        if parameters['mode'] == 'prerecorded':
            app.process_prerecorded(parameters['device'], parameters['inputFile'],
                                    parameters['targetFile'], parameters['size'], parameters['algorithm'])
        elif parameters['mode'] == 'live':
            app.process_anc(parameters['device'],
                            parameters['targetFile'], parameters['algorithm'], parameters['role'], parameters['waitSize'], parameters['stepSize'], parameters['size'], parameters['tuiConnection'])

    except KeyboardInterrupt:
        exit('\nInterrupted by user')
    except Exception as e:
        exit(type(e).__name__ + ': ' + str(e))
