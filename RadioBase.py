from abc import ABCMeta, abstractmethod

class RadioBase:
    __metaclass__ = ABCMeta

    @abstractmethod
    def readmsg(self):
        raise NotImplementedError()

    @abstractmethod
    def networkid(self):
        raise NotImplementedError()

    @abstractmethod
    def senderid(self):
        raise NotImplementedError()

    @abstractmethod
    def rssi(self):
        raise NotImplementedError()
