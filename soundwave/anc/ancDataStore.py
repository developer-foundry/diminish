import numpy as np
from influx.influxService import InfluxService
import time

class AncDataStore():
    def __init__(self):
        self.service = InfluxService()
        self.waveName = str(time.time())

    def sendData(self, wave):
        self.service.addWave(self.waveName, wave)