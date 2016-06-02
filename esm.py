import esmPrint as esmPrint
from esmPrint import esmPrintSource as ps
import esmSerial
import esmDCLoad

def main():
    dprint = esmPrint.esmPrint()

    serial = esmSerial.esmSerial()
    dprint = esmPrint.esmPrint()
    dprint.init()
    serPorts = #[(esmSerial.esmSerialPorts.uiMicro,"/dev/ptyp1", serCallback)]
#            (esmSerial.esmSerialPorts.panelMicro,"/dev/ptyp2", serCallback),
[            (esmSerial.esmSerialPorts.electronicLoad,"/dev/ptyp3", esmDCLoad.callback)]
#            (esmSerial.esmSerialPorts.stringInverter,"/dev/ptyp4", serCallback)]
    serial.init(dprint,serPorts))
    esmDCLoad.trackMPPT(serial,dprint)


if __name__ == "__main__":
    main()
