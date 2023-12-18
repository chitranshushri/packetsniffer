from scapy.all import *

class IPv6Analyzer:
    def __init__(self):
        self.layer = "NETWORK_LAYER"
        self.value_names = [
            "Version", "Class", "Flow Label", "Length", "Protocol",
            "Hop Limit", "Source IP", "Destination IP", "Source Host Name",
            "Destination Host Name"
        ]
        self.values = {}

    def is_analyzable(self, pkt):
        return isinstance(pkt, IPv6)

    def get_protocol_name(self):
        return "IPv6"

    def get_value_names(self):
        return self.value_names

    def analyze(self, pkt):
        self.values.clear()
        if not self.is_analyzable(pkt):
            return

        self.values[self.value_names[0]] = 6
        self.values[self.value_names[1]] = pkt.tc
        self.values[self.value_names[2]] = pkt.fl
        self.values[self.value_names[3]] = pkt.plen
        self.values[self.value_names[4]] = pkt.nh
        self.values[self.value_names[5]] = pkt.hlim
        self.values[self.value_names[6]] = pkt.src
        self.values[self.value_names[7]] = pkt.dst
        self.values[self.value_names[8]] = socket.gethostbyaddr(pkt.src)[0] if pkt.src else "Unknown"
        self.values[self.value_names[9]] = socket.gethostbyaddr(pkt.dst)[0] if pkt.dst else "Unknown"

    def get_value(self, value_name):
        return self.values.get(value_name)

    def get_value_at(self, index):
        if 0 <= index < len(self.value_names):
            return self.get_value(self.value_names[index])
        return None

    def get_values(self):
        return [self.get_value(name) for name in self.value_names]


# Example usage:
# ipv6_pkt = IPv6(src="2001:db8::1", dst="2001:db8::2")
# analyzer = IPv6Analyzer()
# analyzer.analyze(ipv6_pkt)
# print(analyzer.get_value_names())
# print(analyzer.get_values())
