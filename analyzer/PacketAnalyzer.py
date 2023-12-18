from datetime import datetime
from jpcap.packet import Packet
from jdumper.analyzer import JDPacketAnalyzer

class PacketAnalyzer(JDPacketAnalyzer):
    def __init__(self):
        self.value_names = ["Captured Time", "Captured Length"]
        self.packet = None

    def is_analyzable(self, packet):
        return True

    def get_protocol_name(self):
        return "Packet Information"

    def get_value_names(self):
        return self.value_names

    def analyze(self, p):
        self.packet = p

    def get_value(self, name):
        if name == self.value_names[0]:
            return datetime.fromtimestamp(self.packet.sec + self.packet.usec / 1e6).strftime('%Y-%m-%d %H:%M:%S.%f')
        elif name == self.value_names[1]:
            return self.packet.caplen
        else:
            return None

    def get_value_at(self, index):
        if index == 0:
            return datetime.fromtimestamp(self.packet.sec + self.packet.usec / 1e6).strftime('%Y-%m-%d %H:%M:%S.%f')
        elif index == 1:
            return self.packet.caplen
        else:
            return None

    def get_values(self):
        return [datetime.fromtimestamp(self.packet.sec + self.packet.usec / 1e6).strftime('%Y-%m-%d %H:%M:%S.%f'),
                self.packet.caplen]
