import unittest
import esmPrint

class TestPrint(unittest.TestCase):
    def test_init(self):
        p = esmPrint.esmPrint()
        self.assertFalse(p.init())
        self.assertFalse(p.dprint(esmPrint.esmPrintSource.serial,"Test"))
    def test_noInit(self):
        q = esmPrint.esmPrint()
        self.assertTrue(q.dprint(esmPrint.esmPrintSource.serial,"Test"))

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
