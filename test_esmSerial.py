import unittest
import esmSerial
import esmPrint

class TestSerialMethods(unittest.TestCase):
    s = None
    def test_init(self):
        self.s = esmSerial.esmSerial()
        self.s.init(esmPrint.esmPrint())

        self.assertEqual(self.s.sendSerial(esmSerial.esmSerialPorts.uiMicro,bytearray([0,1])),2)
        self.assertIsNone(self.s.write(esmSerial.esmSerialPorts.uiMicro,bytearray([0])))
    def tearDown(self):
        if self.s is not None:
            self.s.close()

if __name__ == '__main__':
    unittest.main()
