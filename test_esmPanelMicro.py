import unittest
import esmPanelMicro
import esmPrint
import esmSerial
import time
import datetime
from multiprocessing import Queue

class TestPMMethods(unittest.TestCase):
    def test_gps(self):
        Dprint = esmPrint.esmPrint(False)
        pm = esmPanelMicro.esmPanelMicro(Dprint)
        self.pm = pm
        for c in '{"lat" : 42964055, "long" : -85677421}\n':
            pm.respQ.put(c.encode('ascii'))
        time.sleep(0.02);
        self.assertEqual(pm.location,(42.964055,-85.677421))

        for c in '{"pitch" : 17.0}\n':
            pm.respQ.put(c.encode('ascii'))
        time.sleep(0.02);
        self.assertEqual(pm.pitch,-17)

        for c in '{"roll" : 13.0}\n':
            pm.respQ.put(c.encode('ascii'))
        time.sleep(0.02);
        self.assertEqual(pm.roll,13)

        for c in '{"temp" : 73.0}\n':
            pm.respQ.put(c.encode('ascii'))
        time.sleep(0.02);
        self.assertEqual(pm.temp,73)

        for c in '{"date" : 210616, "time": 1120000}\n':
            pm.respQ.put(c.encode('ascii'))
        time.sleep(0.02);
        self.assertEqual(pm.timestamp,datetime.datetime(2016,6,21,1,12,00))

        for c in '{"mx" : -48, "my" : 2188}\n':
            pm.respQ.put(c.encode('ascii'))
        time.sleep(0.02);
        self.assertEqual(pm.heading,75)
    def tearDown(self):
        self.pm.close()

if __name__ == '__main__':
    unittest.main()
