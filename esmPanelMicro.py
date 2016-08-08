import esmSerial
from esmPrint import esmPrintSource as ps
import time
from multiprocessing import Queue
import queue
import datetime
import threading
import json
import sys
import pickle

class panelThread(threading.Thread):

    def __init__(self, panelMicro, respQ,dprint):
        threading.Thread.__init__(self)
        self.respQ = respQ
        self.end = False
        self.dprint = dprint
        self.panelMicro = panelMicro
    def run(self):
        while not self.end:
            message = bytearray()
            byte = b'0'
            i = 0
            while byte != b'\n' and not self.end:
                try:
                    byte = self.respQ.get(True,10)
                    message += byte
                    self.panelMicro.error = False
                except queue.Empty:
                    self.panelMicro.error = True

            if not self.end:
                data = json.loads(str(message,'ascii'))
                # Update the panel variables with the received information 
                try:
                    self.panelMicro.location = (data['lat'] / 1000000, data['long'] / 1000000)
                    self.panelMicro.update = True
                except KeyError:
                    pass

                try:
                    self.panelMicro.heading = data['heading']
                    self.panelMicro.update = True
                except KeyError:
                    pass

                try:
                    self.panelMicro.pitch = data['pitch']
                    self.panelMicro.pitch = -self.panelMicro.pitch 
                    self.panelMicro.update = True
                except KeyError:
                    pass

                try:
                    self.panelMicro.roll = data['roll']
                    self.panelMicro.update = True
                except KeyError:
                    pass

                try:
                    self.panelMicro.temp = data['temp']
                    self.panelMicro.update = True
                except KeyError:
                    pass

                try:
                    date = data['date']
                    time = data['time']
                    day = int(date / 10000)
                    month = int(date / 100) % 100
                    year = (int(date) % 100) + 2000
                    hour = int(time / 1000000)
                    minute = int(time / 10000) % 100
                    second = int(time / 100) % 100

                    self.panelMicro.timestamp = datetime.datetime(year,month,day,hour,minute,second)
                    self.panelMicro.update = True

                except KeyError:
                    pass

                # Save last data for reload
                toPickle = {
                        'location' : self.panelMicro.location,
                        'timestamp' : self.panelMicro.timestamp,
                        'heading' : self.panelMicro.heading,
                        'pitch' : self.panelMicro.pitch,
                        'roll' : self.panelMicro.roll,
                        'temp' : self.panelMicro.temp,
                        }
                with open('lastPoint','wb') as afile:
                    pickle.dump(toPickle,afile)



    def stop(self):
        self.end = True;


class esmPanelMicro:
    def __init__(self, Dprint):
        self.respQ = Queue()
        self.dprint = Dprint.dprint

        # Instantiate position variables
        self.location = (0.0,0.0)
        self.timestamp = datetime.datetime.now()
        self.heading = 0.0
        self.pitch = 0.0
        self.roll = 0.0
        self.temp = 0.0
        self.error = False
        # Save last data for reload
        try:
            with open('lastPoint','rb') as afile:
                try:
                    toPickle = pickle.load(afile)

                    self.location = toPickle['location']
                    self.timestamp = toPickle['timestamp']
                    self.heading = toPickle['heading']
                    self.pitch = toPickle['pitch']
                    self.roll = toPickle['roll']
                    self.temp =  toPickle['temp']
                # Pickle file may be damaged, ignore it if so
                except:
                    pass
        except FileNotFoundError:
            # No previous points were saved
            pass

        self.update = False

        # Spawn thread to handler inter-process communication
        self.panelThread = panelThread(self,self.respQ,self.dprint)
        self.panelThread.start()
    def close(self):
        self.panelThread.stop()
        self.panelThread.join()

    def __exit__(self,exc_type, exc_value, traceback):
        self.close()

