from enum import Enum

class AutoNumber(Enum):
     def __new__(cls):
         value = len(cls.__members__) + 1
         obj = object.__new__(cls)
         obj._value_ = value
         return obj

class esmMessage(AutoNumber):
    # DC load messages
    dcLoadPanel = ()
    dcLoadShingle = ()
    dcLoadError = ()

    # Anemometer messages
    anemometer = ()
    anemometerError = ()

    # Temperature messages
    boxTemp = ()
    panelTemp = ()
    tempError = ()

    # Panel Micro Messages
    panelUpdate = ()

    # Battery Messages
    batteryLow = ()
    batteryCritical = ()

    # Exit Message
    exitMessage = ()

