import esmPrint as esmPrint
from esmPrint import esmPrintSource as ps
import esmSerial

def main():
    dprint = esmPrint.esmPrint()
    serial = esmSerial.esmSerial()
    serial.init(dprint)
if __name__ == "__main__":
    main()
