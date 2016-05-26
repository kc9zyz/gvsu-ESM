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
    uiProc = None
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
        if self.uiProc is not None:
            self.uiProc.terminate()
    def initPorts(self,port,location):
        try:
            self.ports[port] = serial.Serial()
        except AttributeError:
            self.ports = {}
            self.ports[port] = serial.Serial()



    def init(self,Dprint):
        self.dprint = Dprint.dprint
        dprint = self.dprint
        try:
            self.ports
        except AttributeError:
            self.ports = {}

        # Test the UI Micro Port
        for port in esmSerialPorts:
            try:
                if self.ports[port].port == None:
                    dprint(ps.serialNameError,'The User interface Micro has not been set up.')
            except (NameError,KeyError):
                dprint(ps.serialNameError,'The User interface Micro has not been set up.')
                return True


        self.serialTasksInit()
        return False

    def close(self):
        self.serialTasksClose()

    def sendSerial(self, port, msg):
        try:
            if not port in self.ports:
                print("Port not defined")
                return True
            self.write(self.ports[port],msg)
            return len(msg)
        except AttributeError:
            return True




