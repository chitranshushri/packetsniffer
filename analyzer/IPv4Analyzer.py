from scapy.all import *

class IPv4Analyzer:
    def __init__(self):
        self.layer = "NETWORK_LAYER"
        self.value_names = [
            "Version", "TOS: Priority", "TOS: Throughput", "TOS: Reliability",
            "Length", "Identification", "Fragment: Don't Fragment",
            "Fragment: More Fragment", "Fragment Offset", "Time To Live",
            "Protocol", "Source IP", "Destination IP", "Source Host Name",
            "Destination Host Name"
        ]
        self.values = {}

    def is_analyzable(self, pkt):
        return isinstance(pkt, IP) and pkt.version == 4

    def get_protocol_name(self):
        return "IPv4"

    def get_value_names(self):
        return self.value_names

    def analyze(self, pkt):
        self.values.clear()
        if not self.is_analyzable(pkt):
            return

        self.values[self.value_names[0]] = 4
        self.values[self.value_names[1]] = pkt.tos >> 5
        self.values[self.value_names[2]] = (pkt.tos >> 4) & 1
        self.values[self.value_names[3]] = (pkt.tos >> 3) & 1
        self.values[self.value_names[4]] = pkt.len
        self.values[self.value_names[5]] = pkt.id
        self.values[self.value_names[6]] = pkt.flags.DF
        self.values[self.value_names[7]] = pkt.flags.MF
        self.values[self.value_names[8]] = pkt.frag
        self.values[self.value_names[9]] = pkt.ttl
        self.values[self.value_names[10]] = pkt.proto
        self.values[self.value_names[11]] = pkt.src
        self.values[self.value_names[12]] = pkt.dst
        self.values[self.value_names[13]] = pkt[IP].src
        self.values[self.value_names[14]] = pkt[IP].dst

    def get_value(self, value_name):
        if (self.value_names[13] == value_name and isinstance(self.values.get(value_name), IPv4Address)) or \
           (self.value_names[14] == value_name and isinstance(self.values.get(value_name), IPv4Address)):
            addr = self.values.get(value_name)
            # You may want to implement hostname caching here
            self.values[value_name] = socket.gethostbyaddr(addr)[0] if addr else "Unknown"
        
        return self.values.get(value_name)

    def get_value_at(self, index):
        if 0 <= index < len(self.value_names):
            return self.get_value(self.value_names[index])
        return None

    def get_values(self):
        return [self.get_value(name) for name in self.value_names]


# Example usage:
# ipv4_pkt = IP(src="192.168.1.1", dst="192.168.1.2")
# analyzer = IPv4Analyzer()
# analyzer.analyze(ipv4_pkt)
# print(analyzer.get_value_names())
# print(analyzer.get_values())
