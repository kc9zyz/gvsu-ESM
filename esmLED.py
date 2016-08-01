import colorsys
from neopixel import *

# LED strip configuration:
LED_COUNT      = 60      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

class esmLeds():
    def __init__(self):
        self.leds = [
                [4],
                [3,5],
                [2,6],
                [1,7],
                [0,8],
                ]
        self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
        self.strip.begin()


    def showLevel(self,level,lastBrightness):
        # Neopixels are GRB, not RGB
        ledColors = [
                [0,255,0],
                [179,255,0],
                [251,255,0],
                [255,0,0],
                [255,0,0]
                ]

        # Scale the last pixel by the amount
        levelColor = ledColors[level]
        for i in range(0,len(levelColor)):
            levelColor[i] = int(levelColor[i] * lastBrightness)
        ledColors[level] = levelColor

        # Loop through LEDs
        for i in range(0,level+1):
            ledgroup = self.leds[i]
            color = ledColors[i]
            neoColor = Color(color[0],color[1],color[2])
            for led in ledgroup:
                self.strip.setPixelColor(led,neoColor)

        # Blank the remaining LEDs
        for i in range(level+1,len(self.leds)):
            ledgroup = self.leds[i]
            for led in ledgroup:
                self.strip.setPixelColor(led,Color(0,0,0,))
        self.strip.show()


