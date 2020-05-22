import urwid
import signal
import sys
import threading
from tui.palette.palette import palette
from tui.views.dashboardView import DashboardView
from tui.models.configurationModel import ConfigurationModel
from random import uniform, randint
from common.common import get_project_root

import pickle
import os
import subprocess
import inspect
import numpy as np
from multiprocessing.connection import Client
import time
from common.common import guiRefreshTimer


class DashboardController():
    """
    DashboardController is the primary controller in the diminish TUI. As
    more screens are added later, new controllers should be created.

    This controller kicks off the MainLoop for urwid, handles model updates,
    renders views, and maintains a connection to the underlying diminish CLI
    process for performing the ANC algorithm.
    """

    def __init__(self, parameters, logger, loggingHandler):
        """
        Parameters
        ----------
        parameters : array
            An array of environment variables used to initialize the model.
        logger : Logger
            A python Logger that will render logs to the screen.
        loggingHandler : TuiHandler
            The TuiHandler overrides the standard python logging to stdout/stderr and writes any log
            messages to the Logging view.
        """
        self.logger = logger
        self.loggingHandler = loggingHandler
        self.model = ConfigurationModel(parameters)
        self.loggingHandler.configureModel(self.model)
        self.model.logger = logger

        self.view = DashboardView(self.model)
        self.loop = urwid.MainLoop(
            self.view, palette=palette, unhandled_input=self.handle_input)
        self.model.running = False
        self.proc = None

        # Line has to be last
        self.loop.run()

    def getEnvironmentVars(self):
        """
        Constructs a dictionary of the environment variables to inject into the CLI process that spawns.

        Parameters
        ----------
        None

        Returns
        -------
        None

        Raises
        ------
        None
        """
        my_env = os.environ.copy()
        my_env["MODE"] = self.model.mode
        my_env["ALGORITHM"] = self.model.algorithm
        my_env["INPUT_FILE"] = self.model.inputFile
        my_env["TARGET_FILE"] = self.model.targetFile
        my_env["DEVICE"] = self.model.device
        my_env["SIZE"] = str(self.model.size)
        my_env["ROLE"] = self.model.role
        my_env["WAIT_SIZE"] = str(self.model.waitSize)
        my_env["STEP_SIZE"] = str(self.model.stepSize)
        my_env["TUI_CONNECTION"] = str(True)
        return my_env

    def run(self):
        """
        Spawns the diminish CLI and runs the ANC algorithm based on the selections the user made on screen.

        Parameters
        ----------
        None

        Returns
        -------
        None

        Raises
        ------
        None
        """
        self.stdout = self.loop.watch_pipe(self.read_pipe)
        self.stderr = self.loop.watch_pipe(self.read_pipe)

        my_env = self.getEnvironmentVars()

        self.proc = subprocess.Popen(['python3', '-m', 'cli', ],
                                     cwd=get_project_root(),
                                     stdout=self.stdout,
                                     stderr=self.stderr,
                                     env=my_env
                                     )

        if(self.model.mode == 'live'):
            self.createConnectionToCli()

        self.loop.set_alarm_in(0, self.refresh)

    def refresh(self, _loop, data):
        """
        Refresh runs every {guiRefreshTimer} seconds and will rerender the screen with updated model values.

        Parameters
        ----------
        None

        Returns
        -------
        None

        Raises
        ------
        None
        """
        try:
            if(self.model.mode == 'live'):
                self.updateGraphs()
                self.model.memory = int(self.dataClient.recv())
                self.model.cpu = float(self.dataClient.recv())
        except EOFError:
            pass
        except Exception as e:
            self.logger.error(e)

        self.view.refresh()
        _loop.set_alarm_in(guiRefreshTimer, self.refresh)

    def createConnectionToCli(self):
        """
        Using the python multiprocessing library, this function will create a Pipe to the 
        process that spawned the CLI. All monitoring data will be passed from the Monitor class
        in diminish to the TUI via this connection.

        Parameters
        ----------
        None

        Returns
        -------
        None

        Raises
        ------
        None
        """
        connected = False
        # loop until connected
        while not connected:
            try:
                self.dataClient = Client(
                    ('localhost', 5000), authkey=b'secret password')
                connected = True
            except ConnectionRefusedError:
                pass

        self.logger.debug('Connected to Process!')

    def read_pipe(self, read_data):
        """
        Monitors a stdout or stderr pipe and redirects it to the logger.

        Parameters
        ----------
        None

        Returns
        -------
        None

        Raises
        ------
        None
        """
        self.logger.info(read_data)

    def updateGraphs(self):
        """
        Parses the data based from the diminish Monitor class related to the sound graphs.

        Parameters
        ----------
        None

        Returns
        -------
        None

        Raises
        ------
        None
        """
        # first update all three buffers
        tuiBufferName = self.dataClient.recv()  # receive 'error'
        while tuiBufferName != 'end buffers':
            tuiData = self.dataClient.recv()
            self.logger.debug(f'Appending {tuiData} to buffer {tuiBufferName}')

            if(tuiBufferName == 'error'):
                self.model.errorBuffer.append([float(tuiData.flat[0])])
            if(tuiBufferName == 'output'):
                self.model.outputBuffer.append([float(tuiData.flat[0])])
            if(tuiBufferName == 'reference'):
                self.model.referenceBuffer.append([float(tuiData.flat[0])])
            if(tuiBufferName == 'output-error'):
                self.model.errorPercentage = tuiData.flat[0]

            tuiBufferName = self.dataClient.recv()

    def togglePause(self):
        """
        Toggles whether or not the algorithm is running and passes that message to the CLI process

        Parameters
        ----------
        None

        Returns
        -------
        None

        Raises
        ------
        None
        """
        self.model.paused = not self.model.paused
        self.proc.send_signal(signal.SIGUSR1)

    def handle_input(self, key):
        """
        All keyboard input for the main screen is processed in this function

        Parameters
        ----------
        None

        Returns
        -------
        None

        Raises
        ------
        None
        """
        if key == 'Q' or key == 'q':
            if(self.proc is not None):
                self.proc.send_signal(signal.SIGINT)

            raise urwid.ExitMainLoop()
        if key == 'R' or key == 'r':
            self.model.running = True
            self.run()
        if key == 'P' or key == 'p':
            self.togglePause()
