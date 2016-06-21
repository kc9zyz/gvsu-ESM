import unittest
import esmADC


class TestSerialMethods(unittest.TestCase):
    s = None
    def test_init(self):
        adc = esmADC.esmADC()
        self.assertEqual(adc.read(),(0x202,0x202,0x202))

if __name__ == '__main__':
    unittest.main()
