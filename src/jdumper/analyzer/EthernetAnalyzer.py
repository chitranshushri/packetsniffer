from jpcap.packet import Packet
from jdumper.analyzer import JDPacketAnalyzer

class EthernetAnalyzer(JDPacketAnalyzer):
    value_names = [
        "Frame Type",
        "Source MAC",
        "Destination MAC"
    ]
    
    def __init__(self):
        self.eth = None
        self.layer = self.DATALINK_LAYER
    
    def is_analyzable(self, p):
        return p.datalink is not None and isinstance(p.datalink, EthernetPacket)
    
    def get_protocol_name(self):
        return "Ethernet Frame"
    
    def get_value_names(self):
        return self.value_names
    
    def analyze(self, p):
        if not self.is_analyzable(p):
            return
        self.eth = p.datalink
    
    def get_value(self, value_name):
        for i, name in enumerate(self.value_names):
            if name == value_name:
                return self.get_value_at(i)
        return None
    
    def get_value_at(self, index):
        if self.eth is None:
            return None
        
        if index == 0:
            return self.eth.frametype
        elif index == 1:
            return self.eth.getSourceAddress()
        elif index == 2:
            return self.eth.getDestinationAddress()
        else:
            return None
    
    def get_values(self):
        if self.eth is None:
            return [None] * len(self.value_names)
        return [self.get_value_at(i) for i in range(len(self.value_names))]
