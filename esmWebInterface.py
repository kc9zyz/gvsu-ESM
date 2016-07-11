import requests
from datetime import datetime
from collections import namedtuple
import json
import os
import base64
import hashlib

class esmDataPoint:
    def __init__(self):
        self.panelOutput = 0
        self.shingleOutput = 0
        self.timestamp = datetime.now()
        self.lat = 0
        self.lon = 0
        self.heading = 0
        self.panel_angle = 0

class esmWebInterface:
    def __init__(self, host, key):
        self.url = host
        self.key = key
        self.backlog = []
    def flushBacklog(self):
        # Empty the backlog of unfinshed requests
        return len(self.backlog)
    def sendUpdate(self, dataPoint):
        # Save the python timestamp, convert to string
        timestamp = dataPoint.timestamp
        dataPoint.timestamp = "'"+str(dataPoint.timestamp)+"'"
        # Add the random data to the data point
        dataPoint.random = base64.b64encode(os.urandom(12)).decode('ascii')
        # Create the json string
        dataBytes = str.encode(json.dumps(dataPoint.__dict__))
        # Restore the python timestamp
        dataPoint.timestamp = timestamp
        # Create a hash of the data and key
        m = hashlib.md5()
        m.update(dataBytes)
        m.update(self.key)
        # Configure the post body payload
        payload = {'json': dataBytes, 'hash': m.hexdigest()}
        # Sen the post request
        r = requests.post(self.url + '?asset=current-data',data = payload)
        # Return the result
        if r.status_code == 401:
            self.backlog.append(dataPoint)
        return r




