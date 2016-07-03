import esmSerial
from esmPrint import esmPrintSource as ps
import time
from multiprocessing import Queue
import queue

class esmPanelMicro:
    def __init__(self):
        self.respQ = Queue()
