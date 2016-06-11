from esmPrint import esmPrintSource as ps
from enum import Enum
import serial
from multiprocessing import Process
from multiprocessing import Queue
import multiprocessing
import queue as Queue2
from time import sleep

class esmSerialPorts(Enum):
    uiMicro = 0
    panelMicro = 1
    electronicLoad = 2
    stringInverter = 3
class esmSerial():

    def write(self,port,msg):
        try:
            if port.port != None:
                port.write(msg)
        except AttributeError:
            pass
        return None

    def rxHandler(self,port,callback,queue):
        while True:
            if port.isOpen():
                while port.in_waiting > 0:
                    #self.dprint(ps.serial,'Value Received')
                    if type(callback) is multiprocessing.queues.Queue:
                        callback.put((port.read(1)))
                    else:
                        print(type(callback))
            try:
                item = queue.get_nowait()
                if item == 'q':
                    break
            except Queue2.Empty:
                pass

            sleep(.001)

    def serialTasksClose(self):
        # TODO Should switch to message queue for termination
        # self.uiProc.join()
        for port in self.ports:
            self.ports[port][2].put('q')
            self.ports[port][1].join()


    def __init__(self,Dprint,serPorts):
        self.uiProc = None
        self.dprint = Dprint.dprint
        dprint = self.dprint

        self.ports = {}
        for port in serPorts:
            # Create the port from the tuple provided
            # 0 - port enum name
            # 1 - port location
            # 2 - port callback queue
            if port[1] != None and port[1] != 'test':
                ser = serial.Serial(port[1])
            else:
                ser = serial.Serial()
            if len(port) > 3:
                ser.baudrate = port[3]
            queue = Queue()
            p = Process(target=self.rxHandler,args=(ser,port[2],queue))
            p.start()
            self.ports[port[0]] = (ser,p,queue)

    def close(self):
        self.serialTasksClose()

    def sendSerial(self, port, msg):
        try:
            if not port in self.ports:
                print("Port not defined")
                return True
            serPort = self.ports[port][0]
            self.write(serPort,msg)
            return len(msg)
        except AttributeError:
            raise
            return True




