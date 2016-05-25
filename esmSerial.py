from esmPrint import esmPrintSource as ps
from enum import Enum
import serial
from multiprocessing import Process
from time import sleep

class esmSerialPorts(Enum):
    uiMicro = 0
    panelMicro = 1
    electronicLoad = 2
    stringInverter = 3
class esmSerial():
    def callback(self):
        return
    def read(self,port):
        return True

    def write(self,port,msg):
        return True

    def uiMicroRxHandler(self,callback):
        while True:
            for port in self.ports:
                if self.read(port):
                    self.dprint(ps.serial,'Checking')
            sleep(1)

    def init(self,Dprint):
        self.dprint = Dprint.dprint
        dprint = self.dprint
        self.ports = {}
        # Define serial ports used by the Educational Solar Module
        self.ports[esmSerialPorts.uiMicro] = uiMicroPort = serial.Serial() #'/dev/serial/by-id/1'
        self.ports[esmSerialPorts.panelMicro] = panelMicroPort = self.panelMicroPort = serial.Serial() #'/dev/serial/by-id/2'
        self.ports[esmSerialPorts.electronicLoad] = electronicLoadPort = self.electronicLoadPort = serial.Serial() # '/dev/serial/by-id/3'
        self.ports[esmSerialPorts.stringInverter] = stringInverterPort = serial.Serial() #'/dev/ttyAMA0'


        # Test the UI Micro Port
        try:
            if uiMicroPort.port == None:
                dprint(ps.serialNameError,'The User interface Micro has not been set up.')
        except NameError:
            dprint(ps.serialNameError,'The User interface Micro has not been set up.')

        # Test the Panel Micro Port
        try:
            if panelMicroPort.port == None:
                dprint(ps.serialNameError,'The Panel Measurement Micro has not been set up.')
        except NameError:
            dprint(ps.serialNameError,'The Panel Measurement Micro has not been set up.')

        # Test the Electronic Load Port
        try:
            if electronicLoadPort.port == None:
                dprint(ps.serialNameError,'The Electronic Load has not been set up.')
        except NameError:
            dprint(ps.serialNameError,'The Electronic Load has not been set up.')

        # Test the String Inverter port
        try:
            if stringInverterPort.port == None:
                dprint(ps.serialNameError,'The String Inverter has not been set up.')
        except NameError:
            dprint(ps.serialNameError,'The String Inverter has not been set up.')

        p = Process(target=self.uiMicroRxHandler, args=(self.callback,))
        p.start()
    def sendSerial(self, port, msg):
        self.write(self.ports[port],msg)




