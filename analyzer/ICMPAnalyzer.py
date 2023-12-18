from scapy.all import *

class ICMPAnalyzer:
    def __init__(self):
        self.layer = "TRANSPORT_LAYER"
        self.value_names = [
            "Type", "Code", "ID", "Sequence", "Redirect Address",
            "Address Mask", "Original Timestamp", "Receive Timestamp",
            "Transmission Timestamp"
        ]
        self.type_names = [
            "Echo Reply(0)", "Unknown(1)", "Unknown(2)",
            "Destination Unreachable(3)", "Source Quench(4)",
            "Redirect(5)", "Unknown(6)", "Unknown(7)", "Echo(8)",
            "Unknown(9)", "Unknown(10)", "Time Exceeded(11)",
            "Parameter Problem(12)", "Timestamp(13)",
            "Timestamp Reply(14)", "Unknown(15)", "Unknown(16)",
            "Address Mask Request(17)", "Address Mask Reply(18)"
        ]
        self.values = {}

    def is_analyzable(self, pkt):
        return isinstance(pkt, ICMP)

    def get_protocol_name(self):
        return "ICMP"

    def get_value_names(self):
        return self.value_names

    def analyze(self, pkt):
        if not self.is_analyzable(pkt):
            return
        self.values.clear()

        icmp = pkt.getlayer(ICMP)
        if icmp.type >= len(self.type_names):
            self.values[self.value_names[0]] = str(icmp.type)
        else:
            self.values[self.value_names[0]] = self.type_names[icmp.type]

        self.values[self.value_names[1]] = icmp.code

        if icmp.type in [0, 8] or (13 <= icmp.type <= 18):
            self.values[self.value_names[2]] = icmp.id
            self.values[self.value_names[3]] = icmp.seq

        if icmp.type == 5:
            self.values[self.value_names[4]] = str(icmp.redir_ip)

        if icmp.type in [17, 18]:
            self.values[self.value_names[5]] = (
                f"{icmp.subnetmask >> 12}.{(icmp.subnetmask >> 8) & 0xff}."
                f"{(icmp.subnetmask >> 4) & 0xff}.{icmp.subnetmask & 0xff}"
            )

        if icmp.type in [13, 14]:
            self.values[self.value_names[6]] = icmp.orig_timestamp
            self.values[self.value_names[7]] = icmp.recv_timestamp
            self.values[self.value_names[8]] = icmp.trans_timestamp

    def get_value(self, value_name):
        return self.values.get(value_name)

    def get_value_at(self, index):
        if 0 <= index < len(self.value_names):
            return self.values.get(self.value_names[index])
        return None

    def get_values(self):
        return [self.values.get(name) for name in self.value_names]


# Example usage:
# icmp_pkt = IP()/ICMP(type=8, code=0)
# analyzer = ICMPAnalyzer()
# analyzer.analyze(icmp_pkt)
# print(analyzer.get_value_names())
# print(analyzer.get_values())
