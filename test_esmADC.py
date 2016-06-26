import unittest
import esmADC


class TestSerialMethods(unittest.TestCase):
    s = None
    def test_init(self):
        adc = esmADC.esmADC()
        a = adc.read()
        self.assertIsNotNone(a)
        print(a)

if __name__ == '__main__':
    unittest.main()
