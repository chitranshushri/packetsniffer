from jpcap.packet import IPPacket, Packet
from jdumper.JDCaptor import hostnameCache
from jdumper.analyzer import JDPacketAnalyzer
from socket import gethostbyaddr

class IPv4Analyzer(JDPacketAnalyzer):
    value_names = [
        "Version",
        "TOS: Priority",
        "TOS: Throughput",
        "TOS: Reliability",
        "Length",
        "Identification",
        "Fragment: Don't Fragment",
        "Fragment: More Fragment",
        "Fragment Offset",
        "Time To Live",
        "Protocol",
        "Source IP",
        "Destination IP",
        "Source Host Name",
        "Destination Host Name"
    ]
    
    def __init__(self):
        self.values = {}
        self.layer = self.NETWORK_LAYER
    
    def is_analyzable(self, p):
        return isinstance(p, IPPacket) and p.version == 4
    
    def get_protocol_name(self):
        return "IPv4"
    
    def get_value_names(self):
        return self.value_names
    
    def analyze(self, packet):
        self.values.clear()
        if not self.is_analyzable(packet):
            return
        
        ip = packet
        self.values[self.value_names[0]] = 4
        self.values[self.value_names[1]] = ip.priority
        self.values[self.value_names[2]] = ip.t_flag
        self.values[self.value_names[3]] = ip.r_flag
        self.values[self.value_names[4]] = ip.length
        self.values[self.value_names[5]] = ip.ident
        self.values[self.value_names[6]] = ip.dont_frag
        self.values[self.value_names[7]] = ip.more_frag
        self.values[self.value_names[8]] = ip.offset
        self.values[self.value_names[9]] = ip.hop_limit
        self.values[self.value_names[10]] = ip.protocol
        self.values[self.value_names[11]] = ip.src_ip.getHostAddress()
        self.values[self.value_names[12]] = ip.dst_ip.getHostAddress()
        self.values[self.value_names[13]] = ip.src_ip
        self.values[self.value_names[14]] = ip.dst_ip
    
    def get_value(self, value_name):
        if value_name in [self.value_names[13], self.value_names[14]]:
            addr = self.values.get(value_name)
            if isinstance(addr, str):
                addr = gethostbyaddr(addr)[0] if addr else ""
                self.values[value_name] = addr
            else:
                addr = addr.getHostAddress()
                if addr in hostnameCache:
                    self.values[value_name] = hostnameCache[addr]
                else:
                    hostname = gethostbyaddr(addr)[0]
                    self.values[value_name] = hostname
                    hostnameCache[addr] = hostname
                    print("miss")
        
        return self.values.get(value_name)
    
    def get_value_at(self, index):
        if 0 <= index < len(self.value_names):
            return self.get_value(self.value_names[index])
        return None
    
    def get_values(self):
        return [self.get_value_at(i) for i in range(len(self.value_names))]
