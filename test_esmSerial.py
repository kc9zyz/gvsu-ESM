import unittest
import esmSerial
import esmPrint

class TestSerialMethods(unittest.TestCase):
    s = None
    def test_init(self):
        self.s1 = esmSerial.esmSerial()
        p = esmPrint.esmPrint()
        p.init()
        self.assertTrue(self.s1.init(p))
        self.s1.initPorts(esmSerial.esmSerialPorts.uiMicro,"/dev/ptyp1")
        self.s1.initPorts(esmSerial.esmSerialPorts.panelMicro,"/dev/ptyp2")
        self.s1.initPorts(esmSerial.esmSerialPorts.electronicLoad,"/dev/ptyp3")

        # Test missing port
        self.assertTrue(self.s1.sendSerial(esmSerial.esmSerialPorts.stringInverter,bytearray([0,1])))
        self.s1.initPorts(esmSerial.esmSerialPorts.stringInverter,"/dev/ptyp4")
        self.assertFalse(self.s1.init(esmPrint.esmPrint()))

        self.assertEqual(self.s1.sendSerial(esmSerial.esmSerialPorts.uiMicro,bytearray([0,1])),2)
        self.assertIsNone(self.s1.write(esmSerial.esmSerialPorts.uiMicro,bytearray([0])))
    def tearDown(self):
        if self.s1 is not None:
            self.s1.close()

if __name__ == '__main__':
    unittest.main()
