# Handle communication between ADC and Raspberry Pi
try:
    import smbus
except ImportError:
    import esmMocksmbus as smbus

MODECNTRL = 0x00
idle = 0x00
auto_scan = 0xCC
DATA0_U = 0x02
DATA0_L = 0x03
DATA1_U = 0x04
DATA1_L = 0x05
DATA2_U = 0x06
DATA2_L = 0x07
ADDRESS = 0x92

class esmADC:
    def __init__(self):
        self.bus = smbus.SMBus(0)
        self.address = ADDRESS
        # Send auto scan mode
        self.bus.write_byte(self.address,MODECNTRL,auto_scan)

    def read(self):
        self.bus.write_byte(self.address,MODECNTRL,idle)
        chan0 = self.bus.read_byte(self.address,DATA0_U) << 4
        chan0 = chan0 + (self.bus.read_byte(self.address,DATA0_L) >> 4)

        chan1 = self.bus.read_byte(self.address,DATA1_U) << 4
        chan1 = chan1 + (self.bus.read_byte(self.address,DATA1_L) >> 4)

        chan2 = self.bus.read_byte(self.address,DATA2_U) << 4
        chan2 = chan2 + (self.bus.read_byte(self.address,DATA2_L) >> 4)

        self.bus.write_byte(self.address,MODECNTRL,auto_scan)
        return (chan0,chan1,chan2)
