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
        self.strinp = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)


    def showLevel(self,level,lastBrightness):
        ledColors = [
                [255,0,0],
                [255,179,0],
                [255,251,0],
                [0,255,0],
                [0,255,0]
                ]

        levelColor = ledColors[level]
        levelHsv = list(colorsys.rgb_to_hsv(levelColor[0],levelColor[1],levelColor[2]))
        levelHsv[2] *= lastBrightness
        levelHsv[2] = int(levelHsv)
        levelColor = list(colorsys.hsv_to_rgb(levelHsv[0],levelHsv[1],levelHsv[2]))

        # Loop through LEDs
        for i in range(0,level+1):
            ledGroup = self.leds[i]
            color = ledColors[i]
            neoColor = Color(color[0],color[1],color[2])
            for led in ledgroup:
                self.strip.setPIxelColor(led,neoColor)

        # Blank the remaining LEDs
        for i in range(level+1,len(self.leds)):
            ledGroup = self.leds[i]
            for led in ledgroup:
                self.strip.setPIxelColor(led,Color(0,0,0,))


