from jpcap.packet import UDPPacket, Packet
from jdumper.analyzer import JDPacketAnalyzer

class UDPAnalyzer(JDPacketAnalyzer):
    def __init__(self):
        self.layer = self.TRANSPORT_LAYER
        self.value_names = ["Source Port", "Destination Port", "Packet Length"]
        self.udp = None

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
        for i in range(len(self.value_names)):
            if self.value_names[i] == value_name:
                return self.get_value_at(i)
        return None

    def get_value_at(self, index):
        if 0 <= index < len(self.value_names):
            if index == 0:
                return self.udp.src_port if self.udp else None
            elif index == 1:
                return self.udp.dst_port if self.udp else None
            elif index == 2:
                return self.udp.length if self.udp else None
        return None

    def get_values(self):
        return [self.get_value_at(i) for i in range(len(self.value_names))]
