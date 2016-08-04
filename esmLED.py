import esmSerial
import math
class esmLeds():
    def __init__(self,serial):
        self.serial = serial



    # Run the show level animation, for a given level and brightness
    def showLevel(self, level, brightness):
        if level > 5:
            level = 5

        if brightness > 255:
            brightness = 255
        brightness /=29
        brightness = math.ceil(brightness)
        brightness = str(brightness)
        level = str(level)
        msg=bytearray('l'+level+brightness+'\n','ascii')

        # Send the LED command
        self.serial.sendSerial(esmSerial.esmSerialPorts.leds,msg)

    # Run the show boxes animation, for a given brightness
    def showBoxes(self, brightness):
        if brightness > 255:
            brightness = 255
        brightness /=29
        brightness = math.ceil(brightness)
        brightness = str(brightness)
        msg=bytearray('b'+brightness+'\n','ascii')
        # Send the LED command
        self.serial.sendSerial(esmSerial.esmSerialPorts.leds,msg)
    def showRed(self):
        msg=bytearray('r\n','ascii')
        # Send the LED command
        self.serial.sendSerial(esmSerial.esmSerialPorts.leds,msg)


