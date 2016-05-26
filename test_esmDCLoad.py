import unittest
import esmDCLoad
import esmPrint
import esmSerial
from time import sleep

class TestDCLoadMethods(unittest.TestCase):
    s = None
    def test_powerPointTrack(self):
        # Instantiate a powerPointTrack
        pp = esmDCLoad.powerPointTrack()
        # Test init values
        self.assertEqual(pp.voltage,[0])
        self.assertEqual(pp.current,[0])
        self.assertEqual(pp.power,[0])

        # Add a voltage point
        pp.voltage.append(1)
        # Test voltage point placement
        self.assertEqual(pp.voltage,[0,1])
        pp.current.append(1)
        # Test current point placement
        self.assertEqual(pp.current,[0,1])
        pp.power.append(1)
        # Test power point placement
        self.assertEqual(pp.power,[0,1])

        # Test all
        self.assertEqual(pp.all(),[[0,1],[0,1],[0,1]])

        pp.voltage.append(2)
        pp.current.append(2)
        pp.power.append(4)

        # Test all
        self.assertEqual(pp.all(),[[0,1,2],[0,1,2],[0,1,4]])

    def test_trackMPPT(self):
        self.assertTrue(esmDCLoad.trackMPPT(None,None)[0])
        self.assertTrue(esmDCLoad.trackMPPT(None,esmPrint.esmPrint())[0])
        self.assertTrue(esmDCLoad.trackMPPT(esmSerial.esmSerial(),esmPrint.esmPrint())[0])
        self.s = esmSerial.esmSerial()
        self.s.initPorts(esmSerial.esmSerialPorts.uiMicro,"/dev/ptyp1")
        self.s.initPorts(esmSerial.esmSerialPorts.panelMicro,"/dev/ptyp2")
        self.s.initPorts(esmSerial.esmSerialPorts.electronicLoad,"/dev/ptyp3")
        self.s.initPorts(esmSerial.esmSerialPorts.stringInverter,"/dev/ptyp4")
        self.s.init(esmPrint.esmPrint())
        p = esmPrint.esmPrint()
        p.init()
        self.assertFalse(esmDCLoad.trackMPPT(self.s,p)[0])
    def tearDown(self):
        if self.s is not None:
            self.s.close()




if __name__ == '__main__':
    unittest.main()

