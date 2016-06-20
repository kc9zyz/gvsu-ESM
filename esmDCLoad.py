import esmSerial
from esmPrint import esmPrintSource as ps
import time
from multiprocessing import Queue
import queue
import csv


# Defines a power tracking point
class powerPointTrack:
    def __init__(self):
        self.voltage = [0]
        self.current = [0]
        self.power   = [0]

    def all(self):
        return (self.voltage,self.current,self.power)
    def add(self,pp):
        for i in pp.voltage:
            self.voltage.append(i)
        for i in pp.current:
            self.current.append(i)
        for i in pp.power:
            self.power.append(i)
    def last(self):
        return (self.voltage[-1],self.current[-1],self.current[-1])


class esmDCLoad:

    def __init__(self):
        self.respQ = Queue()

    def getCallback(self):
        return self.respQ

    def processCallback(self):
        # Store message until newline
        message = bytearray()
        byte = b'0'
        while byte != b'\n':
            try:
                byte = self.respQ.get(True,1)
                message += byte
            except queue.Empty:
                print('Nothing in the queue')
                raise
        return message


    def setCurrent(self,serial, current):
        # Send the command to set the current of the load
        msg = bytearray("CURR " + str(current) + "mA\n",'ascii')
        if serial.sendSerial(esmSerial.esmSerialPorts.electronicLoad,msg) == len(msg):
            return False
        else:
            return True
    def getPower(self,serial):
        # Send the command to get the power
        msg = bytearray('MEAS:POW?\n','ascii')
        serial.sendSerial(esmSerial.esmSerialPorts.electronicLoad,msg)

        # Wait for response
        try:
            res = self.processCallback()
            return float(str(res,'ascii'))
        except queue.Empty:
            raise

    def getVoltage(self,serial):
        # Send the command to get the power
        msg = bytearray('MEAS:VOLT?\n','ascii')
        serial.sendSerial(esmSerial.esmSerialPorts.electronicLoad,msg)

        # Wait for response
        try:
            res = self.processCallback()
            return float(str(res,'ascii'))
        except queue.Empty:
            raise

    def getCurrent(self,serial):
        # Send the command to get the power
        msg = bytearray('MEAS:CURR?\n','ascii')
        serial.sendSerial(esmSerial.esmSerialPorts.electronicLoad,msg)

        # Wait for response
        try:
            res = self.processCallback()
            return float(str(res,'ascii'))
        except queue.Empty:
            raise


    def prepareDevice(self,serial):
        # Disable Input
        msg = bytearray('INP OFF\n','ascii')
        serial.sendSerial(esmSerial.esmSerialPorts.electronicLoad,msg)
        # Set to CCH mode
        msg = bytearray('MODE CCH\n','ascii')
        serial.sendSerial(esmSerial.esmSerialPorts.electronicLoad,msg)
        # Enable input
        msg = bytearray('INP ON\n','ascii')
        serial.sendSerial(esmSerial.esmSerialPorts.electronicLoad,msg)

    def deactivateDevice(self,serial):
        # Disable Input
        msg = bytearray('INP OFF\n','ascii')
        serial.sendSerial(esmSerial.esmSerialPorts.electronicLoad,msg)
        # Turn off Current 
        msg = bytearray('CURR 0A\n','ascii')
        serial.sendSerial(esmSerial.esmSerialPorts.electronicLoad,msg)


    def trackMPPT(self,serial, Dprint, maxCurrent):

        #Verify that print is setup
        if Dprint == None:
            print('ERR: DPrint not given, falling back')
            return (True,0)
        dprint = Dprint.dprint
        if serial == None:
            dprint(ps.mppt,'Serial port not specified.')
            return (True,0)
        pp = powerPointTrack()
        self.prepareDevice(serial)

        #
        # Set the current to 0
        current = 0
        currentStepLevel = 500
        maxP = 0
        powerPoint = powerPointTrack()
        for i in range(0,2):
            sessionPoint = powerPointTrack()

            while current <= maxCurrent :
                if self.setCurrent(serial,current):
                    return (True,0)
                time.sleep(1)
                try:
                    # Get the operating voltage
                    sessionPoint.voltage.append(self.getVoltage(serial))

                    # Get the operating current
                    sessionPoint.current.append(self.getCurrent(serial))

                    # Get the operating power
                    sessionPoint.power.append(self.getPower(serial))
                    print(sessionPoint.last())
                except queue.Empty:
                    print('No Response from DC Load')
                    return (False,0)

                current += currentStepLevel
            powerPoint.add(sessionPoint)

            # Find the index of the max power value
            maxIdx = max(x)
            maxCurr = int(powerPoint.current[maxIdx] *1000)
            print('Max: ',maxCurr, ' MaxP: ',powerPoint.power[maxIdx])
            maxP = powerPoint.power[maxIdx]

            current = maxCurr - currentStepLevel
            if current < 0:
                current = 0
            maxCurrent = maxCurr + currentStepLevel
            currentStepLevel /=8

            self.deactivateDevice(serial)
            time.sleep(1)
            self.prepareDevice(serial)



        self.deactivateDevice(serial)
        #f = open('out.csv','wt')
#        try:
#            writer = csv.writer(f)
#            writer.writerow(('Voltage','Current', 'Power'))
#            for i in range(0,len()):
#                writer.writerow((voltages[i],currents[i],powers[i]))
#        finally:
#            f.close()

        # Increase the current until the computed power begins to decrease

        # Perturb and observe to get MPP
        return (False,maxP)

