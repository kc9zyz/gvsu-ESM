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

    def uiMicroRxHandler(self,callback):
        while True:
            if self.read(self.uiMicroPort):
                self.dprint(ps.serial,'Checking')
            sleep(1)

    def init(self,Dprint):
        self.dprint = Dprint.dprint
        dprint = self.dprint
        # Define serial ports used by the Educational Solar Module
        uiMicroPort = self.uiMicroPort = serial.Serial() #'/dev/serial/by-id/1'
        panelMicroPort = self.panelMicroPort = serial.Serial() #'/dev/serial/by-id/2'
        electronicLoadPort = self.electronicLoadPort = serial.Serial() # '/dev/serial/by-id/3'
        stringInverterPort = self.stringInverterPort = serial.Serial() #'/dev/ttyAMA0'

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




