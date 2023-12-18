from jpcap.packet import TCPPacket, Packet
from jdumper.analyzer import JDPacketAnalyzer

class TelnetAnalyzer(JDPacketAnalyzer):
    def __init__(self):
        self.layer = self.APPLICATION_LAYER

    def is_analyzable(self, p):
        return (
            isinstance(p, TCPPacket)
            and ((p.src_port == 23) or (p.dst_port == 23))
        )

    def get_protocol_name(self):
        return "Telnet"

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

