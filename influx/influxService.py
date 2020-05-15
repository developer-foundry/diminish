from influxdb import InfluxDBClient
import numpy as np

class InfluxService():
    def __init__(self):
        self.client = InfluxDBClient(database='soundwave')
    
    def addWaveDetail(self, waveName, channelOne, channelTwo):
        json_body = [
            {
                "measurement": "wave_detail",
                "tags": {
                    "wave": waveName
                },
                "fields": {
                    "channelOne": channelOne,
                    "channelTwo": channelTwo
                }
            }
        ]

        self.client.write_points(json_body)

    def addWave(self, waveName, waveArray):
        for waveDetail in np.nditer(waveArray):
            self.addWaveDetail(waveName, waveDetail[0], waveDetail[1])