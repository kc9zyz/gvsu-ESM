from enum import Enum

class esmPrintSource(Enum):
    # Serial
    serial = [0,'<Serial> ']
    serialNameError = [1,'<Serial: NameError> ']
    serialException = [2,'<Serial: SerialException> ']
    serialTimeoutException = [3,'<Serial: SerialTimoutException> ']

    # MPPT
    mppt = [4,'<MPPT> ']

class esmPrint():
    moduleInit = None
    def dprint(self,source, text):
        if self.moduleInit == None:
            print('Need to init');
            return True
        else:
            print('\n'+source.value[1]+text)
            return False

    def init(self):
        self.moduleInit = True;
        return False
