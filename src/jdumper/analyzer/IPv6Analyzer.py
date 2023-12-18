from jpcap.packet import IPPacket, Packet
from jdumper.analyzer import JDPacketAnalyzer
from socket import gethostbyaddr

class IPv6Analyzer(JDPacketAnalyzer):
    value_names = [
        "Version",
        "Class",
        "Flow Label",
        "Length",
        "Protocol",
        "Hop Limit",
        "Source IP",
        "Destination IP",
        "Source Host Name",
        "Destination Host Name"
    ]
    
    def __init__(self):
        self.values = {}
        self.layer = self.NETWORK_LAYER
    
    def is_analyzable(self, p):
        return isinstance(p, IPPacket) and p.version == 6
    
    def get_protocol_name(self):
        return "IPv6"
    
    def get_value_names(self):
        return self.value_names
    
    def analyze(self, packet):
        self.values.clear()
        if not self.is_analyzable(packet):
            return
        
        ip = packet
        self.values[self.value_names[0]] = 6
        self.values[self.value_names[1]] = ip.priority
        self.values[self.value_names[2]] = ip.flow_label
        self.values[self.value_names[3]] = ip.length
        self.values[self.value_names[4]] = ip.protocol
        self.values[self.value_names[5]] = ip.hop_limit
        self.values[self.value_names[6]] = ip.src_ip.getHostAddress()
        self.values[self.value_names[7]] = ip.dst_ip.getHostAddress()
        self.values[self.value_names[8]] = gethostbyaddr(ip.src_ip.getHostAddress())[0]
        self.values[self.value_names[9]] = gethostbyaddr(ip.dst_ip.getHostAddress())[0]
    
    def get_value(self, value_name):
        return self.values.get(value_name)
    
    def get_value_at(self, index):
        if 0 <= index < len(self.value_names):
            return self.values.get(self.value_names[index])
        return None
    
    def get_values(self):
        return [self.get_value_at(i) for i in range(len(self.value_names))]
