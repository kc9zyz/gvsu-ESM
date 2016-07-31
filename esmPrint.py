from enum import Enum
import logging
import logging.handlers
import threading
import os

class esmPrintSource(Enum):
    # Serial
    serial = [0,'<Serial> ']
    serialNameError = [1,'<Serial: NameError> ']
    serialException = [2,'<Serial: SerialException> ']
    serialTimeoutException = [3,'<Serial: SerialTimoutException> ']

    # MPPT
    mppt = [4,'<MPPT> ']

    # Panel Micro
    panelMicro = [5,'<Panel Micro> ']

    # Main
    main = [6,'<Main> ']

    # Temperature
    temp = [6,'<Temperature> ']

class esmPrint():
    moduleInit = None
    def dprint(self,source, text):
        if self.toFile == True:
            #write to log
            self.logger.info(source.value[1]+text)

            pass
        else:
            print(source.value[1]+text)
        return False

    def __init__(self, toFile=False):
        if toFile == True:
            self.toFile = True
        else:
            self.toFile = False
        self.moduleInit = True;

        # Setup logger
        if not os.path.exists('/tmp/log/'):
            os.makedirs('/tmp/log/')
        self.logger = logging.getLogger('esm')
        hdlr = logging.handlers.RotatingFileHandler('/tmp/log/esm.log',maxBytes=100000, backupCount=1000)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        self.logger.addHandler(hdlr)
        self.logger.setLevel(logging.INFO)
