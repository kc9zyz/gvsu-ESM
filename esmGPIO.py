# Attempt to import the raspberry pi specific GPIO module
try:
    import RPi.GPIO as gpio
except ImportError:
    # Fallback to the mocked module for testing
    import esmGPIOMock as gpio
from enum import Enum

retractRelay = 17
buzzerRelay = 19
dcLoadRelay = 20
fanRelay = 21
ssr = 22
tempSensor = 25



class esmGPIO:
    def __init__(self):
        # Set board mode to BOARD (raspberry pi header numbering)
        gpio.setmode(gpio.BCM)

        # Setup relay outputs
        gpio.setup(retractRelay,gpio.OUT, initial=gpio.LOW)
        gpio.setup(buzzerRelay,gpio.OUT, initial=gpio.LOW)
        gpio.setup(dcLoadRelay,gpio.OUT, initial=gpio.LOW)
        gpio.setup(fanRelay,gpio.OUT, initial=gpio.LOW)
        gpio.setup(ssr,gpio.OUT, initial=gpio.LOW)
        gpio.setup(tempSensor,gpio.OUT, initial=gpio.HIGH)
    def output(self, pin, level):
        if level:
            gpio.output(pin,gpio.HIGH)
        else:
            gpio.output(pin,gpio.LOW)
    def input(self, pin):
        return gpio.input(pin)

