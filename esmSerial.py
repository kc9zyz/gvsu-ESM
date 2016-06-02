from esmPrint import esmPrintSource as ps
from enum import Enum
import serial
from multiprocessing import Process
from multiprocessing import Queue
import queue as Queue2
from time import sleep

class esmSerialPorts(Enum):
    uiMicro = 0
    panelMicro = 1
    electronicLoad = 2
    stringInverter = 3
class esmSerial():
    uiProc = None
    def read(self,port):
        return None

    def write(self,port,msg):
        return None

    def rxHandler(self,port,callback,queue):
        while True:
            if self.read(port):
                self.dprint(ps.serial,'Value Received')
            try:
                item = queue.get_nowait()
                if item == 'q':
                    break
            except Queue2.Empty:
                pass

            sleep(.1)

    def serialTasksClose(self):
        # TODO Should switch to message queue for termination
        # self.uiProc.join()
        for port in self.ports:
            self.ports[port][2].put('q')
            self.ports[port][1].join()


    def init(self,Dprint,serPorts):
        self.dprint = Dprint.dprint
        dprint = self.dprint

        self.ports = {}
        for port in serPorts:
            # Create the port from the tuple provided
            # 0 - port enum name
            # 1 - port location
            # 2 - port callback
            ser = serial.Serial()
            queue = Queue()
            p = Process(target=self.rxHandler,args=(ser,port[2],queue))
            p.start()
            self.ports[port[0]] = (ser,p,queue)
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




