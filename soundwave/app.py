import numpy as np

import logging

import soundfile as sf

from soundwave.algorithms.signal_processing import process_signal
import soundwave.plotting.plot as plot

from soundwave.orchestrators.clientOrchestrator import ClientOrchestrator
from soundwave.orchestrators.serverOrchestrator import ServerOrchestrator
import common.common


def process_prerecorded(device, inputFile, targetFile, truncateSize, algorithm):
    inputSignal, inputFs = sf.read(inputFile, dtype='float32')
    targetSignal, targetFs = sf.read(targetFile, dtype='float32')

    # trucate the input signal for testing purposes as the file is big
    inputSignal = inputSignal[0:truncateSize]
    targetSignal = targetSignal[0:truncateSize]

    outputSignal, errorSignal = process_signal(
        inputSignal, targetSignal, algorithm)

    plot.plot_vertical(algorithm, 'prerecorded', inputSignal,
                       targetSignal, outputSignal, errorSignal)


def process_anc(device, targetFile, algorithm, btmode, waitSize, stepSize, size, tuiConnection):
    orchestrator = None
    try:
        if(btmode == 'server'):
            orchestrator = ServerOrchestrator(
                device, algorithm, targetFile, waitSize, stepSize, size, tuiConnection)
        elif(btmode == 'client'):
            orchestrator = ClientOrchestrator(device, waitSize, stepSize)

        orchestrator.run()
    except KeyboardInterrupt:
        if(btmode == 'server'):
            orchestrator.stop()
        logging.info('Exiting Program due to keyboard interrupt')
    except Exception as e:
        logging.exception(f'Exception thrown: {e}')
