# Attempt to import the raspberry pi specific GPIO module
try:
    import RPi.GPIO as gpio
except ImportError:
    # Fallback to the mocked module for testing
    import esmGPIOMock as gpio
from enum import Enum

retractRelay = 17  #P0 Shield
leds = 18 #P1 Shield
buzzerRelay = 27  #P2 Shield
dcLoadRelay = 22  #P3 Shield
fanRelay = 23  #P4 Shield
ssr = 24  #P5 Shield
tempSensor = 25 #P6 Shield



class esmGPIO:
    def __init__(self):
        # Set board mode to BOARD (raspberry pi header numbering)
        gpio.setmode(gpio.BCM)

        gpio.setwarnings(False)

        # Setup relay outputs
        gpio.setup(retractRelay,gpio.IN)
        gpio.setup(buzzerRelay,gpio.IN)
        gpio.setup(dcLoadRelay,gpio.IN)
        gpio.setup(fanRelay,gpio.IN)
        gpio.setup(ssr,gpio.IN)
        gpio.setup(tempSensor,gpio.OUT, initial=gpio.HIGH)
    def output(self, pin, level):
        # Change to output pin
        gpio.setup(pin,gpio.OUT)
        if level:
            gpio.output(pin,gpio.HIGH)
        else:
            gpio.output(pin,gpio.LOW)
    def input(self, pin):
        gpio.setup(pin,gpio.IN)
        return gpio.input(pin)

