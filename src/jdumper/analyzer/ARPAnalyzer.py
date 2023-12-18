from jpcap.packet import Packet
from jdumper.analyzer import JDPacketAnalyzer

class ARPAnalyzer(JDPacketAnalyzer):
    value_names = [
        "Hardware Type",
        "Protocol Type",
        "Hardware Address Length",
        "Protocol Address Length",
        "Operation",
        "Sender Hardware Address",
        "Sender Protocol Address",
        "Target Hardware Address",
        "Target Protocol Address"
    ]
    
    def __init__(self):
        self.arp = None
        self.layer = self.NETWORK_LAYER
    
    def is_analyzable(self, p):
        return isinstance(p, ARPPacket)
    
    def get_protocol_name(self):
        return "ARP/RARP"
    
    def get_value_names(self):
        return self.value_names
    
    def analyze(self, p):
        if not self.is_analyzable(p):
            return
        self.arp = p
    
    def get_value(self, value_name):
        for i, name in enumerate(self.value_names):
            if name == value_name:
                return self.get_value_at(i)
        return None
    
    def get_value_at(self, index):
        if self.arp is None:
            return None
        
        if index == 0:
            return self.get_hardware_type_string(self.arp.hardtype)
        elif index == 1:
            return self.get_protocol_type_string(self.arp.prototype)
        elif index == 2:
            return self.arp.hlen
        elif index == 3:
            return self.arp.plen
        elif index == 4:
            return self.get_operation_string(self.arp.operation)
        elif index == 5:
            return self.arp.getSenderHardwareAddress()
        elif index == 6:
            return self.arp.getSenderProtocolAddress()
        elif index == 7:
            return self.arp.getTargetHardwareAddress()
        elif index == 8:
            return self.arp.getTargetProtocolAddress()
        else:
            return None
    
    def get_values(self):
        if self.arp is None:
            return [None] * len(self.value_names)
        return [self.get_value_at(i) for i in range(len(self.value_names))]
    
    def get_hardware_type_string(self, type_val):
        if type_val == ARPPacket.HARDTYPE_ETHER:
            return f"Ethernet ({type_val})"
        elif type_val == ARPPacket.HARDTYPE_IEEE802:
            return f"Token ring ({type_val})"
        elif type_val == ARPPacket.HARDTYPE_FRAMERELAY:
            return f"Frame relay ({type_val})"
        else:
            return type_val
    
    def get_protocol_type_string(self, type_val):
        if type_val == ARPPacket.PROTOTYPE_IP:
            return f"IP ({type_val})"
        else:
            return type_val
    
    def get_operation_string(self, operation_val):
        if operation_val == ARPPacket.ARP_REQUEST:
            return "ARP Request"
        elif operation_val == ARPPacket.ARP_REPLY:
            return "ARP Reply"
        elif operation_val == ARPPacket.RARP_REQUEST:
            return "Reverse ARP Request"
        elif operation_val == ARPPacket.RARP_REPLY:
            return "Reverse ARP Reply"
        elif operation_val == ARPPacket.INV_REQUEST:
            return "Identify peer Request"
        elif operation_val == ARPPacket.INV_REPLY:
            return "Identify peer Reply"
        else:
            return operation_val
