from jpcap.packet import Packet
from jdumper.analyzer import JDPacketAnalyzer

class SSHAnalyzer(JDPacketAnalyzer):
    def __init__(self):
        self.layer = self.APPLICATION_LAYER
    
    def is_analyzable(self, p):
        if isinstance(p, TCPPacket) and \
           (p.src_port == 22 or p.dst_port == 22):
            return True
        else:
            return False
    
    def get_protocol_name(self):
        return "SSH"
    
    def get_value_names(self):
        return None
    
    def analyze(self, p):
        pass
    
    def get_value(self, s):
        return None
    
    def get_value_at(self, i):
        return None
    
    def get_values(self):
        return None
