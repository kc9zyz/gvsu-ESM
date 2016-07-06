import unittest
import esmPanelMicro
import esmPrint
import esmSerial
import time
import datetime

class TestDCLoadMethods(unittest.TestCase):
    def test_gps(self):
        Dprint = esmPrint.esmPrint(False)
        pm = esmPanelMicro.esmPanelMicro(Dprint)
        self.pm = pm
        for c in '{"lat" : 42.0, "long" : -85.0}\n':
            pm.respQ.put(c.encode('ascii'))
        time.sleep(0.02);
        self.assertEqual(pm.location,(42.0,-85.0))


        for c in '{"heading" : 170.0}\n':
            pm.respQ.put(c.encode('ascii'))
        time.sleep(0.02);
        self.assertEqual(pm.heading,170)

        for c in '{"pitch" : 17.0}\n':
            pm.respQ.put(c.encode('ascii'))
        time.sleep(0.02);
        self.assertEqual(pm.pitch,17)

        for c in '{"roll" : 13.0}\n':
            pm.respQ.put(c.encode('ascii'))
        time.sleep(0.02);
        self.assertEqual(pm.roll,13)

        for c in '{"temp" : 73.0}\n':
            pm.respQ.put(c.encode('ascii'))
        time.sleep(0.02);
        self.assertEqual(pm.temp,73)

        for c in '{"date" : 62116, "time": 11200}\n':
            pm.respQ.put(c.encode('ascii'))
        time.sleep(0.02);
        self.assertEqual(pm.timestamp,datetime.datetime(2016,6,21,1,12,00))
    def tearDown(self):
        self.pm.close()

if __name__ == '__main__':
    unittest.main()
