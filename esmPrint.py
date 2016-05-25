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
    def dprint(self,source, text):
        if self.init == False:
            print('Need to init');
        else:
            print('\n'+source.value[1]+text)

    def init(self):
        self.init = True;
