import esmSerial
from esmPrint import esmPrintSource as ps
import time
from multiprocessing import Queue
import queue
import datetime
import threading
import json
import sys

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
            while byte != b'\n' and not self.end:
                try:
                    byte = self.respQ.get(True,1)
                    message += byte
                except queue.Empty:
                    pass
            if not self.end:
                data = json.loads(str(message,'ascii'))
                # Update the panel variables with the 
                try:
                    self.panelMicro.location = (data['lat'], data['long'])
                except KeyError:
                    pass

                try:
                    self.panelMicro.heading = data['heading']
                except KeyError:
                    pass

                try:
                    self.panelMicro.pitch = data['pitch']
                except KeyError:
                    pass

                try:
                    self.panelMicro.roll = data['roll']
                except KeyError:
                    pass

                try:
                    self.panelMicro.temp = data['temp']
                except KeyError:
                    pass

                try:
                    date = data['date']
                    time = data['time']
                    month = int(date / 10000)
                    day = int(date / 100) % 100
                    year = (int(date) % 100) + 2000
                    hour = int(time / 10000)
                    minute = int(time / 100) % 100
                    second = (int(time) % 100)

                    self.panelMicro.timestamp = datetime.datetime(year,month,day,hour,minute,second)

                except KeyError:
                    pass



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

        # Spawn thread to handler inter-process communication
        self.panelThread = panelThread(self,self.respQ,self.dprint)
        self.panelThread.start()
    def close(self):
        self.panelThread.stop()
        self.panelThread.join()

