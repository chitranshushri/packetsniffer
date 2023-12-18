from jpcap.packet import Packet
from jdumper.analyzer import JDPacketAnalyzer

class UDPAnalyzer(JDPacketAnalyzer):
    value_names = [
        "Source Port",
        "Destination Port",
        "Packet Length"
    ]
    
    def __init__(self):
        self.udp = None
        self.layer = self.TRANSPORT_LAYER
    
    def is_analyzable(self, p):
        return isinstance(p, UDPPacket)
    
    def get_protocol_name(self):
        return "UDP"
    
    def get_value_names(self):
        return self.value_names
    
    def analyze(self, p):
        if not self.is_analyzable(p):
            return
        self.udp = p
    
    def get_value(self, value_name):
        for i, name in enumerate(self.value_names):
            if name == value_name:
                return self.get_value_at(i)
        return None
    
    def get_value_at(self, index):
        if self.udp is None:
            return None
        if index == 0:
            return self.udp.src_port
        elif index == 1:
            return self.udp.dst_port
        elif index == 2:
            return self.udp.length
        else:
            return None
    
    def get_values(self):
        if self.udp is None:
            return [None, None, None]
        return [self.get_value_at(i) for i in range(3)]
