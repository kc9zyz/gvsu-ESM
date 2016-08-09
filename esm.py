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
import esmADC
import esmBatteryMonitor
import esmAnemometer
import math
import esmLED


elSer = '/dev/serial/by-id/usb-Prolific_Technology_Inc._USB-Serial_Controller_D-if00-port0'
pmSer = '/dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0'
ledSer = '/dev/serial/by-id/usb-Arduino__www.arduino.cc__0044_752373336363510131A2-if00'

boxHighTemp = 105
boxHighTempCancel = 95
ledBrightness = 255


# Contains a list of warnings
warnings = {
        'battCrit' : ['Battery Critical ' , False],
        'windHigh' : ['High Wind ', False],
        'windCrit' : ['Critical Wind ', False],
        'tempCrit' : ['Critical Temperature ', False],
        }

# Contains a list of messages
messages = {
        'notDeployed' : ['System Not Deployed ' , False],
        'boxWarm' : ['Electrical box is warm ' , False],
        'battLow' : ['Battery Low ' , False],
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

    def clear(self):
        for a in self.updates:
            self.updates[a] = False


# Responsible for all the functions of the educational solar module
class esm:

    # Handles running the panel and shingle measurement
    def dcLoadThread(self,queue):
        while not self.exitAllThreads:
            startTime = time.time()
            # Measure the panels
            self.esmGPIO.output(esmGPIO.dcLoadRelay,False)
            time.sleep(0.5)
            result = self.dc.trackMPPT(self.s,10000)
            #
            # Check to see if the operation succeeded
            if not result[0]:
                queue.put((em.dcLoadPanel,result[1]))
            else:
                queue.put((em.dcLoadError,em.dcLoadPanel))

            # Measure the shingles
            time.sleep(0.5)
            self.esmGPIO.input(esmGPIO.dcLoadRelay)
            time.sleep(0.5)
            result = self.dc.trackMPPT(self.s,10000)

            # Check to see if the operation succeeded
            if not result[0]:
                queue.put((em.dcLoadShingle,result[1]))
            else:
                queue.put((em.dcLoadError,em.dcLoadShingle))

            # Find the time it takes to run the algorithm
            execTime = time.time()-startTime
            startTime = time.time()
            endTime = startTime + (60- execTime)

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
                if self.pm.error:
                    self.dprint(ps.main, 'Panel measurement micro not responding')

                time.sleep(1)
        return

    # Handles monitoring the temperature of the electrical box
    def tempThread(self, queue):
        # Loop until time to exit
        while not self.exitAllThreads:
            temp = esmTemp.read_temp(self.dprint,self.esmGPIO)
            queue.put((em.boxTemp,temp))
            if temp > boxHighTemp:
                self.fanMode = True
                messages['boxWarm'][1] = True
                self.esmGPIO.output(esmGPIO.fanRelay,False)
            elif temp < boxHighTempCancel:
                self.fanMode = False
                messages['boxWarm'][1] = False
                self.esmGPIO.input(esmGPIO.fanRelay)
            time.sleep(5)

        self.dprint(ps.main, 'Temperature thread Exiting')


    def soundAlarm(self):
        # Cycle the alarm on 1 second chirps
        for i in range(0,10):
            self.esmGPIO.output(esmGPIO.buzzerRelay,False)
            time.sleep(1)
            self.esmGPIO.input(esmGPIO.buzzerRelay)
            time.sleep(1)

    # Handles monitoring the wind speed
    def windThread(self, queue):
        while not self.exitAllThreads:
            speed = esmAnemometer.windspeed(self.adc)
            queue.put((em.anemometer,speed))
            if speed > 40:
                warnings['windCrit'][1] = True
                self.esmLed.showRed()
                # Wind overspeed detected!
                # Check to see if system is deployed
                if self.dp.panelAngle > 5:

                    self.dprint(ps.main, 'Wind Speed CRITICAL')
                    # Sound alarm
                    self.soundAlarm()

                    # Retract panels
                    self.esmGPIO.output(esmGPIO.retractRelay,False)
                    timeout = 0
                    while self.dp.panelAngle > 10 or timeout > 120:
                        timeout += 1
                        time.sleep(1)
                    self.esmGPIO.input(esmGPIO.retractRelay)
            # Check if windspeed exceeds high threshold
            elif speed > 25:
                warnings['windHigh'][1] = True
                warnings['windCrit'][1] = False
                self.esmLed.showRed()
            # Wind speed is safe
            else:
                warnings['windHigh'][1] = False
                warnings['windCrit'][1] = False

            time.sleep(1)

        self.dprint(ps.main, 'Wind Thread Exiting')


    # Monitors SOC of batteries
    def batteryThread(self, queue):
        # Loop until time to exit
        while not self.exitAllThreads:
            # Check the battery level
            level = esmBatteryMonitor.batteryLevel(self.adc)
            self.batteryLevel = level[0]
            queue.put((em.battery,level[0]))
            if level[0] == 50:
                messages['battLow'][1] = True
            elif level[0] <25:
                messages['battLow'][1] = False
                warnings['battCrit'][1] = True
                if self.dp.panelOutput < 50:
                    self.esmGPIO.output(esmGPIO.ssr,False)
            else:
                messages['battLow'][1] = False
                warnings['battCrit'][1] = False
                self.esmGPIO.input(esmGPIO.ssr)


            time.sleep(10)

        self.dprint(ps.main, 'Battery Thread Exiting')

    # Send an update when ready
    def sendUpdate(self):
        resp = self.webInterface.sendUpdate(self.dp)
        if resp.status_code == 200:
            self.dprint(ps.main, 'Update successful')
            self.webInterface.flushBacklog()
        else:
            self.dprint(ps.main, 'Update failed: '+ str(resp))

        # Clear the updated parameters
        self.update.clear()

    def ledThread(self,queue):
        time.sleep(5)
        while not self.exitAllThreads:
            if not warnings['windCrit'][1] :
                self.esmLed.showLevel(int(math.ceil(self.batteryLevel / 20)),ledBrightness)
                time.sleep(12)
                self.esmLed.showBoxes(ledBrightness)
                time.sleep(10)
            time.sleep(1)


    def mainThread(self,queue):
        self.dprint(ps.main, 'Main Thread Started')
        self.update  = updateHolder()
        while not self.exitAllThreads:
            try:
                item = queue.get(True,1)
                # Long handler if-else
                if item[0] == em.dcLoadPanel:
                    # Update the panel data
                    self.dp.panelOutput = item[1]
                    self.update.updates['panelReady'] = True

                elif item[0] == em.dcLoadShingle:
                    # Update the shingle data
                    self.dp.shingleOutput = item[1]
                    self.update.updates['shingleReady'] = True


                elif item[0] == em.dcLoadError:
                    self.dprint(ps.main, 'DC load issue with: '+item[1].name)

                elif item[0] == em.panelUpdate:
                    # Update the data point
                    self.dp.lat = self.pm.location[0]
                    self.dp.lon = self.pm.location[1]
                    self.dp.timestamp = datetime.datetime.now()
                    self.dp.heading = self.pm.heading
                    self.dp.panelAngle = self.pm.pitch
                    self.update.updates['panelUpdateReady'] = True

                    # Update the trailer backend
                    if self.dp.panelAngle < 5:
                       messages['notDeployed'][1] = True
                    else:
                       messages['notDeployed'][1] = False
                    esmTrailerBackend.update(
                            panelAngle = self.dp.panelAngle,
                            panelTemp = self.pm.temp,
                            heading = self.pm.heading
                            )

                elif item[0] == em.anemometer:
                    esmTrailerBackend.update(windspeed=item[1])

                elif item[0] == em.battery:
                    esmTrailerBackend.update(battery=item[1])

                elif item[0] == em.boxTemp:
                    esmTrailerBackend.update(boxTemp=math.floor(item[1]))


                if self.update.ready():
                    self.dprint(ps.main, 'Sending Update')
                    # Data point is ready, send
                    self.sendUpdate()

                # Update all messages and warnings
                warningText = ''
                for warn in warnings:
                    if warnings[warn][1]:
                        warningText += warnings[warn][0]

                messageText = ''
                for msg in messages:
                    if messages[msg][1]:
                        messageText += messages[msg][0]
                esmTrailerBackend.update(warning = warningText,message = messageText)


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

        print(serverPass)
        # Setup the web interface
        self.webInterface = esmWebInterface.esmWebInterface('http://cis.gvsu.edu/~neusonw/solar/data/',serverPass)

        # Setup the panel micro
        self.pm = esmPanelMicro.esmPanelMicro(self.p)

        # Setup Serial Ports
        serPorts = [
                (esmSerial.esmSerialPorts.electronicLoad,elSer,self.dc.getCallback(),38400),
                (esmSerial.esmSerialPorts.panelMicro,pmSer,self.pm.respQ,115200),
                (esmSerial.esmSerialPorts.leds,ledSer,None,115200)
                ]
        self.s = esmSerial.esmSerial(self.p,serPorts)

        # Setup LED interface
        self.esmLed = esmLED.esmLeds(self.s)

        # Start the trailer display backend
        esmTrailerBackend.startThread()

        # Create the main message Queue
        self.queue = Queue()

        # Setup fan mode
        self.fanMode = True

        # Setup temperature sensor
        esmTemp.setup()


        # Setup the ADC
        self.adc = esmADC.esmADC()

        # Create the datapoint
        self.dp = esmWebInterface.esmDataPoint()

        # Setup battery level reporting
        self.batteryLevel = 100

        # Create threads container
        self.threads = []

        # Create the DC load thread
        self.threads.append(Thread(target=self.dcLoadThread,args=(self.queue,)))

        self.threads.append(Thread(target=self.mainThread,args=(self.queue,)))

        self.threads.append(Thread(target=self.tempThread,args=(self.queue,)))

        self.threads.append(Thread(target=self.panelMicroThread,args=(self.queue,)))

        self.threads.append(Thread(target=self.batteryThread,args=(self.queue,)))

        self.threads.append(Thread(target=self.windThread,args=(self.queue,)))

        self.threads.append(Thread(target=self.ledThread,args=(self.queue,)))

        for th in self.threads:
            th.start()



    def shutdown(self):

        # Shutdown the trailer backend
        esmTrailerBackend.stop()

        # close the panel micro
        self.pm.close()

        self.exitAllThreads = True

        for th in self.threads:
            th.join()
        self.esmGPIO.__init__()

        # Shutdown the serial ports
        self.s.close()

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

