import unittest
import esmADC


class TestSerialMethods(unittest.TestCase):
    s = None
    def test_init(self):
        adc = esmADC.esmADC()
        self.assertIsNotNone(adc.read())

if __name__ == '__main__':
    unittest.main()
