from scapy.all import ARP

class ARPAnalyzer:
    def __init__(self):
        self.value_names = [
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
        self.arp = None

    def is_analyzable(self, pkt):
        return ARP in pkt

    def get_protocol_name(self):
        return "ARP"

    def get_value_names(self):
        return self.value_names

    def analyze(self, pkt):
        if not self.is_analyzable(pkt):
            return
        self.arp = pkt[ARP]

    def get_value(self, value_name):
        for i, name in enumerate(self.value_names):
            if name == value_name:
                return self.get_value_at(i)

        return None

    def get_value_at(self, index):
        if index == 0:
            return f"Ethernet ({self.arp.hwtype})"
        elif index == 1:
            return f"IP ({self.arp.ptype})"
        elif index == 2:
            return self.arp.hwlen
        elif index == 3:
            return self.arp.plen
        elif index == 4:
            return self.get_operation_name()
        elif index == 5:
            return self.arp.hwsrc
        elif index == 6:
            return self.arp.psrc
        elif index == 7:
            return self.arp.hwdst
        elif index == 8:
            return self.arp.pdst
        else:
            return None

    def get_values(self):
        return [self.get_value_at(i) for i in range(len(self.value_names))]

    def get_operation_name(self):
        op = self.arp.op
        if op == 1:
            return "ARP Request"
        elif op == 2:
            return "ARP Reply"
        elif op == 3:
            return "Reverse ARP Request"
        elif op == 4:
            return "Reverse ARP Reply"
        elif op == 8:
            return "Identify peer Request"
        elif op == 9:
            return "Identify peer Reply"
        else:
            return str(op)


# Example usage:
# arp_pkt = ARP(op=ARP.who_has, pdst="192.168.1.1")
# analyzer = ARPAnalyzer()
# analyzer.analyze(arp_pkt)
# print(analyzer.get_values())
