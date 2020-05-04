import numpy as np

from functools import partial
from profilehooks import profile

import sys
import os
import pickle
import threading
import logging

import sounddevice as sd
import soundfile as sf

from soundwave.algorithms.signal_processing import process_signal
import soundwave.playback.playback as player
import soundwave.microphone.microphone as mic
import soundwave.plotting.plot as plot

from soundwave.anc.ancClientOrchestrator import AncClientOrchestrator
from soundwave.anc.ancServerOrchestrator import AncServerOrchestrator
import soundwave.common.common


targetLocation = 0
liveInputSignal = None
liveTargetSignal = None
liveOutputSignal = None
liveErrorSignal = None
processing = True

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


# call back for the sounddevice Stream to perform live processing
def live_algorithm(algorithm, targetSignal, numChannels, indata, outdata, frames, time, status):
    global targetLocation
    global liveInputSignal
    global liveTargetSignal
    global liveOutputSignal
    global liveErrorSignal

    if status:
        logging.info(status)

    # keep a running counter of where we are in the target signal
    # making a global variable for now
    inputSignal = np.array(indata)
    targetSignalMaxLength = len(targetSignal)
    truncateSize = len(inputSignal)
    targetEnd = (targetLocation + truncateSize)

    # start the target signal file over if we've reached the end
    if targetSignalMaxLength < targetEnd:
        targetLocation = 0

    # splice the target signal to line it up with the current input signal
    targetSignal = targetSignal[targetLocation:targetEnd]

    # process the signal and create pink noise
    if processing:
        outputSignal, errorSignal = process_signal(
        inputSignal, targetSignal, algorithm)
    else:
        outputSignal = np.add(inputSignal, targetSignal)
        errorSignal = np.zeros((len(targetSignal), 2))

    targetLocation += truncateSize
    outdata[:] = outputSignal

    #update global arrays for plotting
    if(liveInputSignal is None):
        liveInputSignal = inputSignal
        liveTargetSignal = targetSignal
        liveOutputSignal = outputSignal
        liveErrorSignal = errorSignal
    else:
        liveInputSignal = np.concatenate((liveInputSignal, inputSignal), axis=0)
        liveTargetSignal = np.concatenate((liveTargetSignal, targetSignal), axis=0)
        liveOutputSignal = np.concatenate((liveOutputSignal, outputSignal), axis=0)
        liveErrorSignal = np.concatenate((liveErrorSignal, errorSignal), axis=0)


def process_live(parser, device, targetFile, algorithm):
    global processing
    nextAction = ''

    try:
        numChannels = 2
        targetSignal, targetFs = sf.read(targetFile, dtype='float32')
        algo_partial = partial(
            live_algorithm, algorithm, targetSignal, numChannels)
        with sd.Stream(device=(device, device),
                    channels=numChannels, callback=algo_partial):
            while nextAction.upper() != 'EXIT':
                nextAction = input()
                if(nextAction.upper() == 'PAUSE' or nextAction.upper() == 'RESUME'):
                    processing = not processing
                
        
        # plot the results on exit
        plot.plot_vertical(algorithm, 'live', liveInputSignal,
                        liveTargetSignal, liveOutputSignal, liveErrorSignal)

    except KeyboardInterrupt:
        parser.exit('\nInterrupted by user')
    except Exception as e:
        parser.exit(type(e).__name__ + ': ' + str(e))


def process_anc(device, targetFile, algorithm, btmode, waitSize, stepSize):
    orchestrator = None
    try:
        if(btmode == 'server'):
            orchestrator = AncServerOrchestrator(device, algorithm, targetFile, waitSize, stepSize)
        elif(btmode == 'client'):
            orchestrator = AncClientOrchestrator(device, waitSize, stepSize)
        
        orchestrator.run()
    except KeyboardInterrupt:
        logging.info('Exiting Program due to keyboard interrupt')
    except Exception as e:
        logging.error(f'Exception thrown: {e}')