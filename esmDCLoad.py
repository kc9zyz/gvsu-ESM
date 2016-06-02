import esmSerial
from esmPrint import esmPrintSource as ps


class powerPointTrack:
    voltage = [0]
    current = [0]
    power   = [0]

    def all(self):
        return [self.voltage,self.current,self.power]
def callback(byte):
    # Store message until newline
    message +=byte

def setCurrent(serial, current):
    # Send the command to set the current of the load
    msg = "CURR" + str(current) + "mA\n"
    if serial.sendSerial(esmSerial.esmSerialPorts.electronicLoad,msg) == len(msg):
        return False
    else:
        return True
def getPower(serial):
    # Send the command to get the power
    msg = "MEAS:POW?\n"
    serial.sendSerial(esmSerial.esmSerialPorts.electronicLoad,msg)

def prepareDevice(serial):
    # Disable Input
    msg = "INP OFF"
    serial.sendSerial(esmSerial.esmSerialPorts.electronicLoad,msg)
    # Set to CCH mode
    msg = "MODE CCH"
    serial.sendSerial(esmSerial.esmSerialPorts.electronicLoad,msg)
    # Enable input
    msg = "INP ON"
    serial.sendSerial(esmSerial.esmSerialPorts.electronicLoad,msg)

def trackMPPT(serial, Dprint):

    # Set the parameters to 0 
    current = 0
    voltage = 0
    power = 0

    #Verify that print is setup
    if Dprint == None:
        print('ERR: DPrint not given, falling back')
        return (True,0)
    dprint = Dprint.dprint
    if serial == None:
        dprint(ps.mppt,'Serial port not specified.')
        return (True,0)
    pp = powerPointTrack()
    prepareDevice(serial)

    #
    # Set the current to 0
    current = 0
    while current < 9000 :
        if setCurrent(serial,current):
            return (True,0)
        getPower(serial)
        current += 1


    # Increase the current until the computed power begins to decrease

    # Perturb and observe to get MPP
    return (False,0)

