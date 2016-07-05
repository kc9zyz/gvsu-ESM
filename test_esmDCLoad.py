import unittest
import esmDCLoad
import esmPrint
import esmSerial
from time import sleep

def serCallback(byte):
    print(byte)


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
        self.assertEqual(pp.all(),([0,1],[0,1],[0,1]))

        pp.voltage.append(2)
        pp.current.append(2)
        pp.power.append(4)

        # Test all
        self.assertEqual(pp.all(),([0,1,2],[0,1,2],[0,1,4]))


        pp2 = esmDCLoad.powerPointTrack()
        #print(pp2.all())
        pp2.add(pp)
        self.assertEqual(pp2.all(),([0,0,1,2],[0,0,1,2],[0,0,1,4]))
        self.assertEqual(pp2.last(),(2,2,4))


    def test_trackMPPT(self):
        with self.assertRaises(AttributeError):
            dc = esmDCLoad.esmDCLoad(None)

        p = esmPrint.esmPrint(False)
        dc = esmDCLoad.esmDCLoad(p)
        serPorts = [(esmSerial.esmSerialPorts.electronicLoad,"test", dc.getCallback(),38400)]
        self.s = esmSerial.esmSerial(p,serPorts)

        self.assertTrue(dc.trackMPPT(None,500)[0])
        self.assertFalse(dc.trackMPPT(self.s,500)[0])
    def tearDown(self):
        if self.s is not None:
            self.s.close()




if __name__ == '__main__':
    unittest.main()

