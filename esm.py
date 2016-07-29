import esmSerial
import esmDCLoad
import esmPrint
import esmWebInterface

elSer = '/dev/serial/by-id/usb-Prolific_Technology_Inc._USB-Serial_Controller_D-if00-port0'
pmSer = '/dev/serial/by-id/usb-Teensyduino_USB_Serial_1697620-if00'

class esm:
    def __init__(self):
        return

    def dcLoadThread(self,queue):
        #output = dc.trackMPPT(s,10000)
        return

    def setup(self):
        with open('pass') as passFile:
            serverPass = bytes(passFile.read(),'ascii')
        output = (False,200)

        # Setup the debug print interface
        self.p = esmPrint.esmPrint(False)

        # Setup the DC load object
        self.dc = esmDCLoad.esmDCLoad(self.p)

        # Setup the web interface
        self.webInterface = esmWebInterface.esmWebInterface('http://cis.gvsu.edu/~neusonw/solar/data/',serverPass)

        # Setup Serial Ports
        serPorts = [
                (esmSerial.esmSerialPorts.electronicLoad,elSer,self.dc.getCallback(),38400),
                (esmSerial.esmSerialPorts.panelMicro,pmSer,self.dc.getCallback(),115200)
                ]
        self.s = esmSerial.esmSerial(self.p,serPorts)

    def shutdown(self):
        self.s.close()

def main():
    esmObj = esm()
    esmObj.setup()
    esmObj.shutdown()

if __name__ == '__main__':
    main()




# Start a new thread to watch for the output of the panels and shingles

#print('OUTPUT '+str(int(output[1])))
#output = (False,1)
#
#dataPoint = esmWebInterface.esmDataPoint()
#dataPoint.output = int(output[1])


#webInterface.sendUpdate(dataPoint)



