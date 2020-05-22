import numpy as np

import logging

import soundfile as sf

from diminish.algorithms.signal_processing import process_signal
import diminish.plotting.plot as plot

from diminish.orchestrators.clientOrchestrator import ClientOrchestrator
from diminish.orchestrators.serverOrchestrator import ServerOrchestrator
import common.common


class Diminish():
    """
    Main entry point for CLI and TUI to start ANC algorithm
    Provides two primary mechanisms for ANC - prerecorded
    and live (ANC)

    Attributes
    ----------
    None
    """
    def process_prerecorded(self, device, inputFile, targetFile, truncateSize, algorithm):
        """
        Process prerecorded WAV files

        Parameters
        ----------
        device: String
            A string representation of the sound device being used. 'default' is usually all that is needed
        inputFile: String
            The name of the input signal data file. This represents the reference microphone
        targetFile: String
            The name of the target signal data file. This is the desired signal the user should hear
        truncateSize: int
            The number of frames to read from the WAV files
        algorithm: str
            The name of the algorithm used to perform ANC. Currently, only 'crls' is available.

        Returns
        -------
        None

        Raises
        ------
        None
        """
        inputSignal, _ = sf.read(inputFile, dtype='float32')
        targetSignal, _ = sf.read(targetFile, dtype='float32')

        # trucate the input signal for testing purposes as the file is big
        inputSignal = inputSignal[0:truncateSize]
        targetSignal = targetSignal[0:truncateSize]

        outputSignal, errorSignal = process_signal(
            inputSignal, targetSignal, algorithm)

        plot.plot_vertical(algorithm, 'prerecorded', inputSignal,
                           targetSignal, outputSignal, errorSignal)

    def process_anc(self, device, targetFile, algorithm, btmode, waitSize, stepSize, size, tuiConnection):
        """
        Process live signal streams from the server and client

        Parameters
        ----------
        device: String
            A string representation of the sound device being used. 'default' is usually all that is needed
        targetFile: String
            The name of the target signal data file. This is the desired signal the user should hear
        algorithm: str
            The name of the algorithm used to perform ANC. Currently, only 'crls' is available.
        btmode: String
            The role of the current process. Can be 'server' or 'client' and is set via ENV
        waitSize: int
            The number of signal frames that should be received before the algorithm is ready
        stepSize: int
            The number of signal frames or matrix rows used in the transfer of data to the server
        size: int
            The number of frames to read from the target signal file
        tuiConnection: Boolean
            A flag indicating if the server is running under the TUI interface or the CLIN interface

        Returns
        -------
        None

        Raises
        ------
        None
        """
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
        except Exception as e:
            logging.exception(f'Exception thrown: {e}')
