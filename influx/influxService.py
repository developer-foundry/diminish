from influxdb import InfluxDBClient
import numpy as np
import logging

class InfluxService():
    def __init__(self):
        self.client = InfluxDBClient(database='soundwave')
    
    def addWave(self, waveName, bufferName, waveArray):
        series = []
        for waveDetail in waveArray:
            series.append(f"waves,buffer={bufferName},wave={waveName} channelOne={waveDetail[0]},channelTwo={waveDetail[1]}")

        #write it all in one group. the influx library will handle batching
        self.client.write_points(series, batch_size=5000, protocol='line')