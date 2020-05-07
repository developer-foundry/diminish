import numpy as np

import logging

import soundfile as sf

from soundwave.algorithms.signal_processing import process_signal
import soundwave.playback.playback as player
import soundwave.plotting.plot as plot

from soundwave.anc.ancClientOrchestrator import AncClientOrchestrator
from soundwave.anc.ancServerOrchestrator import AncServerOrchestrator
import soundwave.common.common


def process_prerecorded(device, inputFile, targetFile, truncateSize, algorithm):
    inputSignal, inputFs = sf.read(inputFile, dtype='float32')
    targetSignal, targetFs = sf.read(targetFile, dtype='float32')

    # trucate the input signal for testing purposes as the file is big
    inputSignal = inputSignal[0:truncateSize]
    targetSignal = targetSignal[0:truncateSize]

    outputSignal, errorSignal = process_signal(
        inputSignal, targetSignal, algorithm)

    # player.play_signal(parser, outputSignal, inputFs, device)

    plot.plot_vertical(algorithm, 'prerecorded', inputSignal,
                        targetSignal, outputSignal, errorSignal)

def process_anc(device, targetFile, algorithm, btmode, waitSize, stepSize):
    orchestrator = None
    try:
        if(btmode == 'server'):
            orchestrator = AncServerOrchestrator(device, algorithm, targetFile, waitSize, stepSize)
        elif(btmode == 'client'):
            orchestrator = AncClientOrchestrator(device, waitSize, stepSize)
        
        orchestrator.run()
    except KeyboardInterrupt:
        if(btmode == 'server'):
            orchestrator.ancPlot.plot_buffers(algorithm)
        logging.info('Exiting Program due to keyboard interrupt')
    except Exception as e:
        logging.error(f'Exception thrown: {e}')