import esmSerial
import esmDCLoad
import esmPrint

def serCallback(byte):
    print(str(byte,'ascii'), end="")
dc = esmDCLoad.esmDCLoad()
serPorts = [(esmSerial.esmSerialPorts.electronicLoad,"/dev/tty.usbserial",dc.getCallback(),38400)]
p = esmPrint.esmPrint(False)
s = esmSerial.esmSerial(p,serPorts)
dc.trackMPPT(s,p,1000)
s.close()

