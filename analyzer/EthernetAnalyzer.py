from scapy.all import Ether

class EthernetAnalyzer:
    def __init__(self):
        self.value_names = [
            "Frame Type",
            "Source MAC",
            "Destination MAC"
        ]
        self.eth = None

    def is_analyzable(self, pkt):
        return Ether in pkt

    def get_protocol_name(self):
        return "Ethernet Frame"

    def get_value_names(self):
        return self.value_names

    def analyze(self, pkt):
        if not self.is_analyzable(pkt):
            return
        self.eth = pkt[Ether]

    def get_value(self, value_name):
        for i, name in enumerate(self.value_names):
            if name == value_name:
                return self.get_value_at(i)

        return None

    def get_value_at(self, index):
        if index == 0:
            return self.eth.type
        elif index == 1:
            return self.eth.src
        elif index == 2:
            return self.eth.dst
        else:
            return None

    def get_values(self):
        return [self.get_value_at(i) for i in range(len(self.value_names)]


# Example usage:
# ether_pkt = Ether(src="00:11:22:33:44:55", dst="66:77:88:99:aa:bb", type=0x0800)
# analyzer = EthernetAnalyzer()
# analyzer.analyze(ether_pkt)
# print(analyzer.get_values())
