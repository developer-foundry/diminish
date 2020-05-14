import urwid
import sys
import threading
from tui.palette.palette import palette
from tui.views.dashboardView import DashboardView
from tui.models.configurationModel import ConfigurationModel
from random import uniform, randint
from common.common import get_project_root
from soundwave import app

import pickle
import os
import subprocess
import inspect
import numpy as np
from multiprocessing.connection import Client
import time
from common.common import guiRefreshTimer


class DashboardController():
    def __init__(self, parameters, logger, loggingHandler):
        self.logger = logger
        self.loggingHandler = loggingHandler
        self.model = ConfigurationModel(parameters)
        self.loggingHandler.configureModel(self.model)
        self.model.logger = logger

        self.view = DashboardView(self.model)
        self.loop = urwid.MainLoop(self.view, palette=palette, unhandled_input=self.handle_input)
        self.loop.run()
    
    def run(self):
        self.logger.info('Running...')
        self.stdout = self.loop.watch_pipe(self.read_pipe)
        self.stderr = self.loop.watch_pipe(self.read_pipe)
        cwd = get_project_root()
        connected = False
        self.proc = subprocess.Popen(['python3', '-m', 'cli', self.model.mode,self.model.algorithm,self.model.inputFile,
                                                                self.model.targetFile,self.model.device,str(self.model.size),
                                                                self.model.role,str(self.model.waitSize),str(self.model.stepSize),
                                                                str(self.model.tuiConnection)],
                        cwd=cwd,
                        stdout=self.stdout,
                        stderr=self.stderr
                        )
        
        #loop until connected
        while not connected:
            try:
                self.dataClient = Client(('localhost', 5000), authkey=b'secret password')
                connected = True
            except ConnectionRefusedError:
                pass

        self.logger.debug('Connected to Process!')
        self.loop.set_alarm_in(0, self.refresh)
    
    def read_pipe(self, read_data):
        self.logger.info(read_data)

    def refresh(self, _loop, data):
        try:
            #first update all three buffers
            tuiBufferName = self.dataClient.recv() #receive 'error'
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
        except EOFError:
            pass
        except Exception as e:
            self.logger.error(e)
        
        self.view.refresh()
        _loop.set_alarm_in(guiRefreshTimer, self.refresh)

    # Handle key presses
    def handle_input(self, key):
        if key == 'Q' or key == 'q':
            self.proc.kill() 
            raise urwid.ExitMainLoop()
        if key == 'R' or key == 'r':
            self.run()
            