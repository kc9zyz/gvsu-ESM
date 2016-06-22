import unittest
import esmPrint
import esmGPIO

class TestPrint(unittest.TestCase):
    def test_init(self):
        g = esmGPIO.esmGPIO()
        g.output(esmGPIO.retractRelay,True)
        g.output(esmGPIO.retractRelay,False)
        g.input(esmGPIO.retractRelay)


    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
