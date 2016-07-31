# Handle communication between ADC and Raspberry Pi
try:
    import smbus
except ImportError:
    import esmMocksmbus as smbus
import time

MODECNTRL = 0x00
idle = 0x00
auto_scan = 0xCC
manual_scan = 0xC2
active = 0x80
DATA0_U = 0x02
DATA0_L = 0x03
DATA1_U = 0x04
DATA1_L = 0x05
DATA2_U = 0x06
DATA2_L = 0x07
DATA3_U = 0x08
DATA3_L = 0x09
ADDRESS = 0x48

chan0Scale = 1
chan1Scale = 1
chan2Scale = 1

class esmADC:
    def __init__(self):
        self.bus = smbus.SMBus(1)
        self.address = ADDRESS
        for i in range (0,5):
            try:
                # Send auto scan mode
                self.bus.write_byte_data(self.address,MODECNTRL,active)
                self.bus.write_byte_data(self.address,MODECNTRL,auto_scan)
                return
            except:
                pass

    def read(self):
        for i in range (0,5):
            try:
                time.sleep(0.01)
                self.bus.write_byte_data(self.address,MODECNTRL,idle)
                chan0 = self.bus.read_byte_data(self.address,DATA0_U) << 4
                chan0 = chan0 + (self.bus.read_byte_data(self.address,DATA0_L) >> 4)
                chan0 = chan0 * (5/4096)
                chan0 *= chan0Scale

                chan1 = self.bus.read_byte_data(self.address,DATA1_U) << 4
                chan1 = chan1 + (self.bus.read_byte_data(self.address,DATA1_L) >> 4)
                chan1 = chan1 * (5/4096)
                chan1 *= chan1Scale

                chan2 = self.bus.read_byte_data(self.address,DATA2_U) << 4
                chan2 = chan2 + (self.bus.read_byte_data(self.address,DATA2_L) >> 4)
                chan2 = chan2 * (5/4096)
                chan2 *= chan2Scale

                self.bus.write_byte_data(self.address,MODECNTRL,auto_scan)
                return (chan0,chan1,chan2)
            except:
                pass

        return (0,0,0)
