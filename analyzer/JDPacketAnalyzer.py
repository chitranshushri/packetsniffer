from abc import ABC, abstractmethod

class JDPacketAnalyzer(ABC):
    DATALINK_LAYER = 0
    NETWORK_LAYER = 1
    TRANSPORT_LAYER = 2
    APPLICATION_LAYER = 3

    def __init__(self):
        self.layer = self.DATALINK_LAYER

    @abstractmethod
    def is_analyzable(self, packet):
        pass

    @abstractmethod
    def analyze(self, packet):
        pass

    @abstractmethod
    def get_protocol_name(self):
        pass

    @abstractmethod
    def get_value_names(self):
        pass

    @abstractmethod
    def get_value(self, value_name):
        pass

    @abstractmethod
    def get_value_at(self, index):
        pass

    @abstractmethod
    def get_values(self):
        pass
