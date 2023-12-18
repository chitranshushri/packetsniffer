from abc import ABC, abstractmethod
from jpcap.packet import Packet

class JDPacketAnalyzer(ABC):
    DATALINK_LAYER = 0
    NETWORK_LAYER = 1
    TRANSPORT_LAYER = 2
    APPLICATION_LAYER = 3
    
    def __init__(self):
        self.layer = self.DATALINK_LAYER
    
    @abstractmethod
    def is_analyzable(self, packet: Packet) -> bool:
        pass
    
    @abstractmethod
    def analyze(self, packet: Packet) -> None:
        pass
    
    @abstractmethod
    def get_protocol_name(self) -> str:
        pass
    
    @abstractmethod
    def get_value_names(self) -> list:
        pass
    
    @abstractmethod
    def get_value(self, value_name: str):
        pass
    
    @abstractmethod
    def get_values(self) -> list:
        pass
    
    @abstractmethod
    def get_value_at(self, index: int):
        pass
