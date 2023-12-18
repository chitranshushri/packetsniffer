from jpcap.packet import Packet
from jdumper.analyzer import JDPacketAnalyzer
from datetime import datetime

class PacketAnalyzer(JDPacketAnalyzer):
    value_names = ["Captured Time", "Captured Length"]
    
    def __init__(self):
        self.packet = None
    
    def is_analyzable(self, packet: Packet) -> bool:
        return True
    
    def get_protocol_name(self) -> str:
        return "Packet Information"
    
    def get_value_names(self) -> list:
        return self.value_names
    
    def analyze(self, p: Packet) -> None:
        self.packet = p
    
    def get_value(self, name: str):
        if name == self.value_names[0]:
            return datetime.fromtimestamp(self.packet.sec + self.packet.usec / 1000000).strftime('%Y-%m-%d %H:%M:%S')
        elif name == self.value_names[1]:
            return self.packet.caplen
        else:
            return None
    
    def get_value_at(self, index: int):
        if index == 0:
            return datetime.fromtimestamp(self.packet.sec + self.packet.usec / 1000000).strftime('%Y-%m-%d %H:%M:%S')
        elif index == 1:
            return self.packet.caplen
        else:
            return None
    
    def get_values(self) -> list:
        return [
            datetime.fromtimestamp(self.packet.sec + self.packet.usec / 1000000).strftime('%Y-%m-%d %H:%M:%S'),
            self.packet.caplen
        ]
