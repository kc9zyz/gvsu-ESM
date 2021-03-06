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
        return (self.voltage[-1],self.current[-1],self.power[-1])


class esmDCLoad:

    def __init__(self, Dprint):
        self.respQ = Queue()
        #Verify that print is setup
        if Dprint == None:
            raise AttributeError('Dprint not specified.')
        self.dprint = Dprint.dprint

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
                self.dprint(ps.mppt,'Nothing in the serial queue, DC load did not respond')
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

        # Ensure that the process happens before the relay switches
        time.sleep(1)


    def trackMPPT(self,serial, maxCurrent):
        # Make it easier to reference dprint
        dprint = self.dprint


        if serial == None:
            dprint(ps.mppt,'Serial port not specified.')
            return (True,0)
        pp = powerPointTrack()
        self.prepareDevice(serial)

        #
        # Set the current to 0
        current = 0
        currentStepLevel = 100
        maxP = 0
        sessionPoint = powerPointTrack()

        while current <= maxCurrent :
            if self.setCurrent(serial,current):
                return (True,0)
            time.sleep(.5)
            try:
                # Get the operating voltage
                sessionPoint.voltage.append(self.getVoltage(serial))

                # Get the operating current
                sessionPoint.current.append(self.getCurrent(serial))

                # Get the operating power
                sessionPoint.power.append(self.getPower(serial))

                # Stop the tracking algorithm once the voltage and power drop
                if sessionPoint.voltage[-1] == 0 and sessionPoint.power[-1] == 0:
                    break


            except queue.Empty:
                dprint(ps.mppt,'No Response from DC Load')
                self.deactivateDevice(serial)
                return (True,0)

            current += currentStepLevel

        # Find the index of the max power value
        maxIdx = sessionPoint.power.index(max(sessionPoint.power))
        maxCurr = int(sessionPoint.current[maxIdx] *1000)
        dprint(ps.mppt, 'Max: '+str(maxCurr)+ 'mA, MaxP: '+str(sessionPoint.power[maxIdx])+'W')
        maxP = sessionPoint.power[maxIdx]


        self.deactivateDevice(serial)

        # Return the computer maximum power point
        return (False,maxP)

