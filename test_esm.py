import unittest
import esm
from esmMessages import esmMessage as em
import time

class TestSerialMethods(unittest.TestCase):
    s = None
    def test_init(self):
        with esm.esm() as e:
            e.pm.location = (42,85)
            e.pm.heading = 180
            e.pm.pitch = 23

            e.queue.put((em.dcLoadPanel,100))
            e.queue.put((em.dcLoadShingle,100))
            e.queue.put((em.panelUpdate,))
            time.sleep(2)

if __name__ == '__main__':
    unittest.main()
