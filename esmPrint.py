from enum import Enum

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

class esmPrint():
    moduleInit = None
    def dprint(self,source, text):
        if self.toFile == True:
            #write to file
            pass
        else:
            print('\n'+source.value[1]+text)
        return False

    def __init__(self, toFile):
        if toFile == True:
            self.toFile = True
        else:
            self.toFile = False
        self.moduleInit = True;
