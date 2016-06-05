import esmSerial
from esmPrint import esmPrintSource as ps
import time
from multiprocessing import Queue
import queue
import csv
import numpy as np


class powerPointTrack:
    voltage = [0]
    current = [0]
    power   = [0]

    def all(self):
        return [self.voltage,self.current,self.power]
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
                # print(str(byte,'ascii'))
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

        # Set the parameters to 0 
        current = 0
        voltage = 0
        power = 0
        currents = [0]
        voltages = [0]
        powers = [0]


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
        currentStepLevel = 100
        for i in range(0,4):
            currentsSession = [0]
            voltagesSession = [0]
            powersSession = [0]

            while current <= maxCurrent :
                print(current)
                if self.setCurrent(serial,current):
                    return (True,0)
                time.sleep(.4)
                try:
                    voltages.append(self.getVoltage(serial))
                    voltagesSession.append(voltages[len(voltages)-1])

                    currents.append(self.getCurrent(serial))
                    currentsSession.append(currents[len(currents)-1])

                    powers.append(self.getPower(serial))
                    powersSession.append(powers[len(powers)-1])
                except queue.Empty:
                    print('No Response from DC Load')
                    return (False,0)

                current += currentStepLevel

            # Find the index of the max power value
            x = np.array(powersSession)
            maxIdx = np.argmax(x)
            maxCurr = int(currentsSession[maxIdx] *1000)
            print('Max: ',maxCurr, ' MaxP: ',powersSession[maxIdx])

            current = maxCurr - currentStepLevel
            maxCurrent = maxCurr + currentStepLevel
            currentStepLevel /=8

            self.deactivateDevice(serial)
            time.sleep(3)
            self.prepareDevice(serial)



        self.deactivateDevice(serial)
        f = open('out.csv','wt')
        try:
            writer = csv.writer(f)
            writer.writerow(('Voltage','Current', 'Power'))
            for i in range(0,len(voltages)):
                writer.writerow((voltages[i],currents[i],powers[i]))
        finally:
            f.close()

        # Increase the current until the computed power begins to decrease

        # Perturb and observe to get MPP
        return (False,0)

