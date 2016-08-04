import esmSerial
class esmLeds():
    def __init__(self,serial):
        self.serial = serial



    # Run the show level animation, for a given level and brightness
    def showLevel(self, level, brightness):
        msg=bytearray('l','ascii')
        if level > 255:
            level = 255

        if brightness > 255:
            brightness = 255

        msg.append(level)
        msg.append(brightness)
        # Send the LED command
        self.serial.sendSerial(esmSerial.esmSerialPorts.leds,msg)

    # Run the show boxes animation, for a given brightness
    def showBoxes(self, brightness):
        msg=bytearray('b','ascii')
        if brightness > 255:
            brightness = 255
        msg.append(brightness)
        # Send the LED command
        self.serial.sendSerial(esmSerial.esmSerialPorts.leds,msg)
    def showRed(self):
        msg=bytearray('r','ascii')
        # Send the LED command
        self.serial.sendSerial(esmSerial.esmSerialPorts.leds,msg)


