import unittest
import esmWebInterface as wi

class testWeb(unittest.TestCase):
    def test_init(self):
        d = wi.esmDataPoint()
        w = wi.esmWebInterface('http://cis.gvsu.edu/~neusonw/solar/data/',b'TEST')
    def test_send(self):
        # Create the web interface and data point
        w = wi.esmWebInterface('http://cis.gvsu.edu/~neusonw/solar/data/',b'TEST')
        d = wi.esmDataPoint()
        d.output = 100
        self.assertEqual(w.flushBacklog(),0)
        # Send an update
        r = w.sendUpdate(d)

        # Ensure that the operation is unauthorized, but not malformed
        self.assertEqual(r.status_code, 401)
        self.assertEqual(w.flushBacklog(),1)



if __name__ == '__main__':
    unittest.main()
