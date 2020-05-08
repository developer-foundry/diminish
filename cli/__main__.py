from common.common import getEnvironmentVariables
from soundwave import app


if __name__ == '__main__':
    try:
        parameters = getEnvironmentVariables()

        if parameters['mode'] == 'prerecorded':
            app.process_prerecorded(parameters['device'], parameters['inputFile'],
                                    parameters['targetFile'], parameters['size'], parameters['algorithm'])
        elif parameters['mode'] == 'live':
            app.process_anc(parameters['device'],
                            parameters['targetFile'], parameters['algorithm'], parameters['role'], parameters['waitSize'], parameters['stepSize'], parameters['size'])

    except KeyboardInterrupt:
        exit('\nInterrupted by user')
    except Exception as e:
        exit(type(e).__name__ + ': ' + str(e))
