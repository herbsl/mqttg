from RadioBase import RadioBase
import serial

class RadioSerial(RadioBase):
    def __init__(self, dev, baud):
        self.serial = serial.Serial(dev, baud, timeout=None)

    def readmsg(self):
        return self.serial.readline()[:-1]
