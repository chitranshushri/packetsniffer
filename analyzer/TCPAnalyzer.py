from jpcap.packet import TCPPacket, Packet
from jdumper.analyzer import JDPacketAnalyzer

class TCPAnalyzer(JDPacketAnalyzer):
    def __init__(self):
        self.layer = self.TRANSPORT_LAYER
        self.value_names = [
            "Source Port",
            "Destination Port",
            "Sequence Number",
            "Ack Number",
            "URG Flag",
            "ACK Flag",
            "PSH Flag",
            "RST Flag",
            "SYN Flag",
            "FIN Flag",
            "Window Size",
        ]
        self.values = {}

    def is_analyzable(self, p):
        return isinstance(p, TCPPacket)

    def get_protocol_name(self):
        return "TCP"

    def get_value_names(self):
        return self.value_names

    def analyze(self, p):
        self.values.clear()
        if not self.is_analyzable(p):
            return
        tcp = p
        self.values[self.value_names[0]] = tcp.src_port
        self.values[self.value_names[1]] = tcp.dst_port
        self.values[self.value_names[2]] = tcp.sequence
        self.values[self.value_names[3]] = tcp.ack_num
        self.values[self.value_names[4]] = tcp.urg
        self.values[self.value_names[5]] = tcp.ack
        self.values[self.value_names[6]] = tcp.psh
        self.values[self.value_names[7]] = tcp.rst
        self.values[self.value_names[8]] = tcp.syn
        self.values[self.value_names[9]] = tcp.fin
        self.values[self.value_names[10]] = tcp.window

    def get_value(self, value_name):
        return self.values.get(value_name)

    def get_value_at(self, index):
        if 0 <= index < len(self.value_names):
            return self.values.get(self.value_names[index])
        return None

    def get_values(self):
        return [self.values.get(name) for name in self.value_names]
