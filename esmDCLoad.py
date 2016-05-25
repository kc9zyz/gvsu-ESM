import esmSerial
from esmPrint import esmPrintSource as ps


class powerPointTrack:
    voltage = [0]
    current = [0]
    power   = [0]

    def all(self):
        return [self.voltage,self.current,self.power]

def setCurrent(serial, current):
    # Send the command to set the current of the load
    serial.print

def trackMPPT(serial, Dprint):
    current = 0
    voltage = 0
    power = 0
    if Dprint == None:
        print('ERR: DPrint not given, falling back')
        return -1
    dprint = Dprint.dprint
    if serial == None:
        dprint(ps.mppt,'Serial port not specified.')
        return -1
    pp = powerPointTrack()
    # Set the current to 0
    current = 0


    # Increase the current until the computed power begins to decrease

    # Perturb and observe to get MPP

