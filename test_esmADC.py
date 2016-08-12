import unittest
import esmADC
import time


class TestSerialMethods(unittest.TestCase):
    s = None
    def test_init(self):
        adc = esmADC.esmADC()
        time.sleep(0.1)
        a = adc.read()
        self.assertIsNotNone(a)
        print(a)

if __name__ == '__main__':
    unittest.main()
