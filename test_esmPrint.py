import unittest
import esmPrint

class TestPrint(unittest.TestCase):
    def test_initPrint(self):
        p = esmPrint.esmPrint(False)
        self.assertFalse(p.dprint(esmPrint.esmPrintSource.serial,"Test"))

    def test_initFile(self):
        p = esmPrint.esmPrint(True)
        self.assertFalse(p.dprint(esmPrint.esmPrintSource.serial,"Test"))

    def test_noInit(self):
        with self.assertRaises(TypeError):
            q = esmPrint.esmPrint()
        #self.assertRaises(q.dprint(esmPrint.esmPrintSource.serial,"Test"))

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
