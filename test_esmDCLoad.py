import unittest
import esmDCLoad
import esmPrint
import esmSerial

class TestDCLoadMethods(unittest.TestCase):
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
        self.assertEqual(esmDCLoad.trackMPPT(None,None),-1)
        self.assertEqual(esmDCLoad.trackMPPT(None,esmPrint.esmPrint()),-1)
        self.assertNotEqual(esmDCLoad.trackMPPT(esmSerial.esmSerial(),esmPrint.esmPrint()),-1)



if __name__ == '__main__':
    unittest.main()

