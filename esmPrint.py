from enum import Enum

class esmPrintSource(Enum):
    # Serial
    serial = '<Serial> '
    serialNameError = '<Serial: NameError> '
    serialException = '<Serial: SerialException> '
    serialTimeoutException = '<Serial: SerialTimoutException> '



def esmPrint(source, text):
    print('\n'+source.value+text)
