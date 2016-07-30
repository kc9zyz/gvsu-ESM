import esmSerial
import esmDCLoad
import esmPrint
import esmGPIO
import esmWebInterface
import esmTrailerBackend
from multiprocessing import Queue
import queue as Queue2
from threading import Thread
from esmMessages import esmMessage as em
from esmPrint import esmPrintSource as ps
import time

elSer = '/dev/serial/by-id/usb-Prolific_Technology_Inc._USB-Serial_Controller_D-if00-port0'
pmSer = '/dev/serial/by-id/usb-Teensyduino_USB_Serial_1697620-if00'


# Contains a list of warnings
warnings = {
        'battLow' : ('Battery Low' , False),
        'battCrit' : ('Battery Critical' , False),
        'windHigh' : ('High Wind', False),
        'windCrit' : ('Critical Wind', False),
        }

# Contains a list of messages
messages = {
        'notDeployed' : ('System Not Deployed' , False),
        }

class updateHolder:
    def __init__(self):

        self.updates = {
                'panelReady' : False,
                'shingleReady' : False,
                'panelUpdateReady' : False,
                }
        return

    def ready(self):
        for a in self.updates:
            if not self.updates[a]:
                return False
        return True

class esm:

    def dcLoadThread(self,queue):
        startTime = time.time()
        # Measure the panels
        self.esmGPIO.output(esmGPIO.dcLoadRelay,False)
        result = self.dc.trackMPPT(self.s,10000)
        if result[0]:
            queue.put((em.dcLoadPanel,result[1]))
        else:
            queue.put((em.dcLoadError,em.dcLoadPanel))

        # Measure the shingles
        self.esmGPIO.output(esmGPIO.dcLoadRelay,True)
        result = self.dc.trackMPPT(self.s,10000)
        if result[0]:
            queue.put((em.dcLoadShingle,result[1]))
        else:
            queue.put((em.dcLoadError,em.dcLoadShingle))

        # Find the time it takes to run the algorithm
        execTime = time.time()-startTime
        startTime = time.time()

        # Wait 5 minutes, checking for exit every 2
        # Remove the execution time from the delay to remove drift
        while time.time() < startTime + (300-execTime):
            if not self.exitAllThreads:
                time.sleep(2)
            else:
                self.dprint(ps.main, 'DC Load thread Exiting')
                return
    def panelMicroThread(self, queue):
        return

    def sendUpdate(self):
        self.webInterface.sendUpdate(self.dp)


    def mainThread(self,queue):
        self.dprint(ps.main, 'Main Thread Started')
        update  = updateHolder()
        while not self.exitAllThreads:
            try:
                item = queue.get_nowait()
                # Long handler if-else
                if item[0] == em.dcLoadPanel:
                    # Update the panel data
                    dp.panelOutput = item[1]
                    update.updates['panelReady'] = True

                elif item[0] == em.dcLoadShingle:
                    # Update the shingle data
                    dp.shingleOutput = item[1]
                    update.updates['shingleReady'] = True


                elif item[0] == em.dcLoadError:
                    self.dprint(ps.main, 'DC load issue with: '+item[1].name)

                if update.ready():
                    # Data point is ready, send
                    self.webInterface.sendUpdate(self.dp)
                    for a in update.updates:
                        update.updates[a] = False

            except Queue2.Empty:
                pass
        self.dprint(ps.main, 'Main thread Exiting')




    def __init__(self):

        # Global exit value
        self.exitAllThreads = False

        with open('pass') as passFile:
            serverPass = bytes(passFile.read(),'ascii')
        output = (False,200)

        # Setup the debug print interface
        self.p = esmPrint.esmPrint(False)
        self.dprint = self.p.dprint

        # Setup the DC load object
        self.dc = esmDCLoad.esmDCLoad(self.p)

        # Setup the GPIO driver
        self.esmGPIO = esmGPIO.esmGPIO()

        # Setup the web interface
        self.webInterface = esmWebInterface.esmWebInterface('http://cis.gvsu.edu/~neusonw/solar/data/',serverPass)

        # Setup Serial Ports
        serPorts = [
                (esmSerial.esmSerialPorts.electronicLoad,elSer,self.dc.getCallback(),38400),
                (esmSerial.esmSerialPorts.panelMicro,pmSer,self.dc.getCallback(),115200)
                ]
        self.s = esmSerial.esmSerial(self.p,serPorts)

        # Start the trailer display backend
        esmTrailerBackend.startThread()

        # Create the main message Queue
        self.queue = Queue()

        # Create threads container
        self.threads = []

        # Create the DC load thread
        self.threads.append(Thread(target=self.dcLoadThread,args=(self.queue,)))

        self.threads.append(Thread(target=self.mainThread,args=(self.queue,)))

        for th in self.threads:
            th.start()

        # Create the datapoint
        dp = esmWebInterface.esmDataPoint()


    def shutdown(self):
        # Shutdown the serial ports
        self.s.close()

        # Shutdown the trailer backend
        esmTrailerBackend.stop()

        self.exitAllThreads = True

        for th in self.threads:
            th.join()

    def __enter__(self):
        return self

    def __exit__(self,exc_type, exc_value, traceback):
        self.shutdown()

def main():
    with esm() as esmObj:
        time.sleep(100)

if __name__ == '__main__':
    main()




