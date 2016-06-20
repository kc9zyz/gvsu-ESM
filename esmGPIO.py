# Attempt to import the raspberry pi specific GPIO module
try:
    import RPi.GPIO as gpio
except ImportError:
    try:
        # Fallback to the mocked module for testing
        import esmGPIOMock as gpio
    except ImportError:
        print('RPi.GPIO Library not installed, Mock library not found either.')
        raise
from enum import Enum

class gpioPins(Enum):
    retractRelay = 0
    buzzerRelay = 1



class esmGPIO:
    def __init__(self):
        # Set board mode to BOARD (raspberry pi header numbering)
        gpio.setmode(gpio.BOARD)

        # Setup relay outputs
        gpio.setup(gpioPins.retractRelay,gpio.OUT, initial=gpio.LOW)
        gpio.setup(gpioPins.buzzerRelay,gpio.OUT, initial=gpio.LOW)
    def output(self, pin, level):
        if level:
            gpio.output(pin,gpio.HIGH)
        else:
            gpio.output(pin,gpio.LOW)
    def input(self, pin):
        return gpio.input(pin)

