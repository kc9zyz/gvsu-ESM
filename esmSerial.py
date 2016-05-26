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
    ports = {}
    def callback(self):
        return
    def read(self,port):
        return None

    def write(self,port,msg):
        return None

    def uiMicroRxHandler(self,callback):
        while True:
            for port in self.ports:
                if self.read(port):
                    self.dprint(ps.serial,'Value Received')
            sleep(1)
    def serialTasksInit(self):
        self.uiProc= Process(target=self.uiMicroRxHandler, args=(self.callback,))
        self.uiProc.start()

    def serialTasksClose(self):
        # TODO Should switch to message queue for termination
        # self.uiProc.join()
        self.uiProc.terminate()


    def init(self,Dprint):
        self.dprint = Dprint.dprint
        dprint = self.dprint
        # Define serial ports used by the Educational Solar Module
        self.ports[esmSerialPorts.uiMicro]  = serial.Serial() #'/dev/serial/by-id/1'
        self.ports[esmSerialPorts.panelMicro] = serial.Serial() #'/dev/serial/by-id/2'
        self.ports[esmSerialPorts.electronicLoad] = serial.Serial() # '/dev/serial/by-id/3'
        self.ports[esmSerialPorts.stringInverter] = serial.Serial() #'/dev/ttyAMA0'


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

        self.serialTasksInit()

    def close(self):
        self.serialTasksClose()

    def sendSerial(self, port, msg):
        if not port in self.ports:
            print("Port not defined")
            return True
        self.write(self.ports[port],msg)
        return len(msg)




