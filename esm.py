import esmSerial
import esmDCLoad
import esmPrint
import esmGPIO
import esmWebInterface
import esmTrailerBackend
import esmPanelMicro
from multiprocessing import Queue
import queue as Queue2
from threading import Thread
from esmMessages import esmMessage as em
from esmPrint import esmPrintSource as ps
import time
import esmTemp
import datetime


elSer = '/dev/serial/by-id/usb-Prolific_Technology_Inc._USB-Serial_Controller_D-if00-port0'
pmSer = '/dev/serial/by-id/usb-Teensyduino_USB_Serial_1697620-if00'

boxHighTemp = 100
boxHighTempCancel = 95


# Contains a list of warnings
warnings = {
        'battLow' : ['Battery Low' , False],
        'battCrit' : ['Battery Critical' , False],
        'windHigh' : ['High Wind', False],
        'windCrit' : ['Critical Wind', False],
        'tempCrit' : ['Critical Temperature', False],
        }

# Contains a list of messages
messages = {
        'notDeployed' : ['System Not Deployed' , False],
        'boxWarm' : ['Electrical box is warm' , False],
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

# Responsible for all the functions of the educational solar module
class esm:

    # Handles running the panel and shingle measurement
    def dcLoadThread(self,queue):
        while not self.exitAllThreads:
            startTime = time.time()
            # Measure the panels
            self.esmGPIO.output(esmGPIO.dcLoadRelay,False)
            result = self.dc.trackMPPT(self.s,10000)
            #
            # Check to see if the operation succeeded
            if result[0]:
                queue.put((em.dcLoadPanel,result[1]))
            else:
                queue.put((em.dcLoadError,em.dcLoadPanel))

            # Measure the shingles
            self.esmGPIO.output(esmGPIO.dcLoadRelay,True)
            result = self.dc.trackMPPT(self.s,10000)

            # Check to see if the operation succeeded
            if result[0]:
                queue.put((em.dcLoadShingle,result[1]))
            else:
                queue.put((em.dcLoadError,em.dcLoadShingle))

            # Find the time it takes to run the algorithm
            execTime = time.time()-startTime
            startTime = time.time()
            endTime = startTime + (10- execTime)

            # Wait 5 minutes, checking for exit every 2
            # Remove the execution time from the delay to remove drift
            while time.time() < endTime:
                if not self.exitAllThreads:
                    time.sleep(1)
                else:
                    self.dprint(ps.main, 'DC Load thread Exiting')
                    return

    # Handles monitoring of the panel measurement microcontroller
    def panelMicroThread(self, queue):
        while not self.exitAllThreads:
            if self.pm.update:
                queue.put((em.panelUpdate,))

                # Reset the update value
                self.pm.update = False

            else:
                time.sleep(1)
        return

    # Handles monitoring the temperature of the electrical box
    def tempThread(self, queue):
        # Loop until time to exit
        while not self.exitAllThreads:
            temp = esmTemp.read_temp()
            if not self.fanMode and temp > boxHighTemp:
                self.fanMode = True
                messages['boxWarm'] = True
                self.esmGPIO.output(esmGPIO.fanRelay,True)
            elif self.fanMode and temp < boxHighTempCancel:
                self.fanMode = False
                messages['boxWarm'] = False
                self.esmGPIO.output(esmGPIO.fanRelay,False)
            time.sleep(1)

        self.dprint(ps.main, 'Temperature thread Exiting')


    # Send an update when ready
    def sendUpdate(self):
        if self.webInterface.sendUpdate(self.dp).status_code == 200:
            self.webInterface.flushBacklog()
        for a in update.updates:
            update.updates[a] = False


    def mainThread(self,queue):
        self.dprint(ps.main, 'Main Thread Started')
        update  = updateHolder()
        while not self.exitAllThreads:
            try:
                item = queue.get(True,1)
                # Long handler if-else
                if item[0] == em.dcLoadPanel:
                    # Update the panel data
                    self.dp.panelOutput = item[1]
                    update.updates['panelReady'] = True

                elif item[0] == em.dcLoadShingle:
                    # Update the shingle data
                    self.dp.shingleOutput = item[1]
                    update.updates['shingleReady'] = True


                elif item[0] == em.dcLoadError:
                    self.dprint(ps.main, 'DC load issue with: '+item[1].name)

                elif item[0] == em.panelUpdate:
                    # Update the data point
                    self.dp.lat = self.pm.location[0]
                    self.dp.lon = self.pm.location[1]
                    self.dp.timestamp = datetime.datetime.now()
                    self.dp.heading = self.pm.heading
                    self.dp.panelAngle = self.pm.pitch
                    update.updates['panelUpdateReady'] = True

                    # Update the trailer backend
                    if self.dp.panelAngle < 10:
                       messages['notDeployed'][1] = True
                    else:
                       messages['notDeployed'][1] = False
                    esmTrailerBackend.update(
                            panelAngle = self.dp.panelAngle,
                            panelTemp = self.pm.temp
                            )



                if update.ready():
                    # Data point is ready, send
                    self.sendUpdate()

            except Queue2.Empty:
                pass
        self.dprint(ps.main, 'Main thread Exiting')


    # Setup the esm object
    def __init__(self):

        # Global exit value
        self.exitAllThreads = False

        with open('pass') as passFile:
            serverPass = bytes(passFile.read(),'ascii')
        output = (False,200)

        # Setup the debug print interface
        self.p = esmPrint.esmPrint(True)
        self.dprint = self.p.dprint
        self.dprint(ps.main, '')
        self.dprint(ps.main, '********************')
        self.dprint(ps.main, 'ESM Started')
        self.dprint(ps.main, '*********************')
        self.dprint(ps.main, '')

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

        # Setup fan mode
        self.fanMode = True

        # Setup temperature sensor
        esmTemp.setup()

        # Setup the panel micro
        self.pm = esmPanelMicro.esmPanelMicro(self.p)

        # Create threads container
        self.threads = []

        # Create the DC load thread
        self.threads.append(Thread(target=self.dcLoadThread,args=(self.queue,)))

        self.threads.append(Thread(target=self.mainThread,args=(self.queue,)))

        self.threads.append(Thread(target=self.tempThread,args=(self.queue,)))

        self.threads.append(Thread(target=self.panelMicroThread,args=(self.queue,)))

        for th in self.threads:
            th.start()

        # Create the datapoint
        self.dp = esmWebInterface.esmDataPoint()


    def shutdown(self):
        # Shutdown the serial ports
        self.s.close()

        # Shutdown the trailer backend
        esmTrailerBackend.stop()

        # close the panel micro
        self.pm.close()

        self.exitAllThreads = True

        for th in self.threads:
            th.join()

    def __enter__(self):
        return self

    def __exit__(self,exc_type, exc_value, traceback):
        self.shutdown()

def main():
    with esm() as esmObj:
        while not esmObj.exitAllThreads:
            time.sleep(1)

if __name__ == '__main__':
    main()

