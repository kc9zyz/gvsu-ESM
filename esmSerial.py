from esmPrint import esmPrint as dprint
from esmPrint import esmPrintSource as ps
# Define serial ports used by the Educational Solar Module
uiMicroPort = None #'/dev/serial/by-id/1'
panelMicroPort = None #'/dev/serial/by-id/2'
electronicLoadPort = None # '/dev/serial/by-id/3'
stringInverterPort = None #'/dev/ttyAMA0'

def init():
    try:
        if uiMicroPort == None:
            dprint(ps.serialNameError,'The User interface Micro has not been set up.')
    except NameError:
        dprint(ps.serialNameError,'The User interface Micro has not been set up.')
    try:
        if panelMicroPort == None:
            dprint(ps.serialNameError,'The Panel Measurement Micro has not been set up.')
    except NameError:
        dprint(ps.serialNameError,'The Panel Measurement Micro has not been set up.')
    try:
        if electronicLoadPort == None:
            dprint(ps.serialNameError,'The Electronic Load has not been set up.')
    except NameError:
        dprint(ps.serialNameError,'The Electronic Load has not been set up.')
    try:
        if stringInverterPort == None:
            dprint(ps.serialNameError,'The String inverter has not been set up.')
    except NameError:
        dprint(ps.serialNameError,'The String inverter has not been set up.')

def main():
    # my code here
    init()

if __name__ == "__main__":
    main()
