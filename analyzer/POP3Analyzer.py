from jpcap.packet import TCPPacket, Packet
from jdumper.analyzer import JDPacketAnalyzer

class POP3Analyzer(JDPacketAnalyzer):
    def __init__(self):
        self.layer = self.APPLICATION_LAYER

    def is_analyzable(self, p):
        return isinstance(p, TCPPacket) and ((p.src_port == 110) or (p.dst_port == 110))

    def get_protocol_name(self):
        return "POP3"

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
