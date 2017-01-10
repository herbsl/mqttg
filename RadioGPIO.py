from RadioBase import RadioBase

import encryption

import RFM69
from RFM69registers import *

import time

class RadioGPIO(RadioBase):
    def __init__(self, freqBand = RF69_868MHZ, nodeID = 1, networkID = 100, isRFM69HW = True, intPin = 18, rstPin = 29):
        self.rfm69 = RFM69.RFM69(freqBand, nodeID, networkID, isRFM69HW, intPin, rstPin)
        self.NETWORKID = networkID
        self.rfm69.setHighPower(True)
        self.rfm69.encrypt("sampleEncryptKey")

    def __del__(self):
        self.rfm69.shutdown()

    def readmsg(self):
        rfm69 = self.rfm69
        rfm69.receiveBegin()

        while not rfm69.receiveDone():
            time.sleep(.1)

        return "".join([chr(char) for char in self.rfm69.DATA])

    def networkid(self):
        return self.NETWORKID

    def senderid(self):
        return self.rfm69.SENDERID

    def rssi(self):
        return self.rfm69.RSSI
