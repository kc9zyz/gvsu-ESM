import requests
from datetime import datetime
from collections import namedtuple
import json
import os
import pickle
import glob
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
        self.panelAngle = 0

class esmWebInterface:
    def __init__(self, host, key):
        self.url = host
        self.key = key

    def backlog(self,data,name):
        # Create the filename of the backlog entry
        filename = 'backlog/'+name

        # Make the backlog entry file if it isn't already there
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        # Open the backlog entry file for writing
        with open(filename,'wb') as afile:

            # Dump the backlog entry into the file
            pickle.dump(data,afile)


    # Empty the backlog of unfinished requests
    def flushBacklog(self):
        # Create res variable for return
        res = None

        # Get all files that are in the backlog
        files = glob.glob('backlog/*')

        # Track the number of files
        numFiles = 0

        # Iterate through the backlog files
        for filename in files:
            numFiles += 1

        for filename in files:

            # Open the backlog entry file
            with open(filename,'rb') as afile:

                # Load the backlog entry
                point = pickle.load(afile)

                # Try to send data to server
                res = self.sendUpdate(point, True)

                # Check to see if request succeeded
                if res.status_code == 200:

                    # Remove the backlog entry that was just sent
                    os.remove(filename)
                else:
                    # If an error occurred, return it
                    return (numFiles,res)

        return (numFiles,res)

    def sendUpdate(self, dataPoint, fromBack=False):
        # Save the python timestamp, convert to string
        timestamp = dataPoint.timestamp
        dataPoint.timestamp = "'"+dataPoint.timestamp.strftime('%Y-%m-%d %H:%M:%S')+"'"
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
        # Send the post request
        try:
            r = requests.post(self.url + '?asset=current-data',data = payload,timeout=5)
        except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
            self.backlog(dataPoint, m.hexdigest())
            return None
        if not fromBack:
            try:
                r2 = requests.post('http://localhost/data' + '?asset=current-data',data = payload,timeout=2)
            except:
                pass

        # Return the result
        if r.status_code == 401:
            if not fromBack:
                self.backlog(dataPoint, m.hexdigest())
        return r

    def connected(self):
        try:
            r = requests.get(self.url + '?asset=current-data',timeout=5)
        except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
            return False
        return True





