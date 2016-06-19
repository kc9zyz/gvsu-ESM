import requests
import time
from collections import namedtuple
import json
import os
import base64
import hashlib

class esmDataPoint:
    def __init__(self):
        self.output = 0
        self.timestamp = int(time.time())
        self.loc = (0,0)

class esmWebInterface:
    def __init__(self, host, key):
        self.url = host
        self.key = key
    def flushBacklog(self):
        # Empty the backlog of unfinshed requests
        pass
    def sendUpdate(self, dataPoint):
        # Add the random data to the data point
        dataPoint.random = base64.b64encode(os.urandom(12)).decode('ascii')
        # Create the json string
        dataBytes = str.encode(json.dumps(dataPoint.__dict__))
        # Create a hash of the data and key
        m = hashlib.md5()
        m.update(dataBytes)
        m.update(self.key)
        # Configure the post body payload
        payload = {'json': dataBytes, 'hash': m.hexdigest()}
        # Sen the post request
        r = requests.post(self.url + '?asset=current-data',data = payload)
        #Print the result
        print(r.status_code)
        print(r.text)




