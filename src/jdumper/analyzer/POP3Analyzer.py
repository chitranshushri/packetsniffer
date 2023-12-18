from jpcap.packet import Packet, TCPPacket
from jdumper.analyzer import JDPacketAnalyzer

class POP3Analyzer(JDPacketAnalyzer):
    def __init__(self):
        self.layer = self.APPLICATION_LAYER
    
    def is_analyzable(self, p: Packet) -> bool:
        return isinstance(p, TCPPacket) and (p.src_port == 110 or p.dst_port == 110)
    
    def get_protocol_name(self) -> str:
        return "POP3"
    
    def get_value_names(self) -> list:
        return None
    
    def analyze(self, p: Packet) -> None:
        pass
    
    def get_value(self, s: str):
        return None
    
    def get_value_at(self, i: int):
        return None
    
    def get_values(self) -> list:
        return None
