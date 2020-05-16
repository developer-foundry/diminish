from influxdb import InfluxDBClient
import numpy as np
import logging

class InfluxService():
    def __init__(self):
        self.client = InfluxDBClient(database='soundwave')
    
    def addWave(self, waveName, bufferName, waveArray):
        series = []
        for waveDetail in waveArray:
            point_values = {
                "measurement": "waves",
                "tags": {
                    "buffer": bufferName, #best to write these in lexiographic order
                    "wave": waveName,
                },
                "fields": {
                    "channelOne": waveDetail[0],
                    "channelTwo": waveDetail[1]
                }
            }
            series.append(point_values)

        #write it all in one group. the influx library will handle batching
        self.client.write_points(series, batch_size=5000)