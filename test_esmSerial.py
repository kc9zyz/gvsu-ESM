import unittest
import esmSerial
import esmPrint

def serCallback(byte):
    print(byte)

class TestSerialMethods(unittest.TestCase):
    s = None
    def test_init(self):
        p = esmPrint.esmPrint(False)
        serPorts = [
                    (esmSerial.esmSerialPorts.panelMicro,"test", serCallback),
                    ]
        with self.assertRaises(TypeError):
            self.s1 = esmSerial.esmSerial()
        self.s1 = esmSerial.esmSerial(p,serPorts)

        # Test missing port
        self.assertTrue(self.s1.sendSerial(esmSerial.esmSerialPorts.electronicLoad,bytearray([0,1])))
        self.s1.close()

        p = esmPrint.esmPrint(False)
        serPorts = [
                    (esmSerial.esmSerialPorts.panelMicro,"test", serCallback),
                    (esmSerial.esmSerialPorts.electronicLoad,"test", serCallback),
                    ]
        self.s1 = esmSerial.esmSerial(p,serPorts)

        self.assertEqual(self.s1.sendSerial(esmSerial.esmSerialPorts.panelMicro,bytearray([0,1])),2)
        self.assertIsNone(self.s1.write(esmSerial.esmSerialPorts.panelMicro,bytearray([0])))
    def tearDown(self):
        if self.s1 is not None:
            self.s1.close()

if __name__ == '__main__':
    unittest.main()
