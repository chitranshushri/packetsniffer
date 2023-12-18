from scapy.all import *

class FTPAnalyzer:
    def __init__(self):
        self.layer = "APPLICATION_LAYER"

    def is_analyzable(self, pkt):
        return (
            isinstance(pkt, TCP)
            and (
                pkt.sport == 20
                or pkt.dport == 20
                or pkt.sport == 21
                or pkt.dport == 21
            )
        )

    def get_protocol_name(self):
        return "FTP"

    def get_value_names(self):
        return None

    def analyze(self, pkt):
        pass

    def get_value(self, s):
        return None

    def get_value_at(self, i):
        return None

    def get_values(self):
        return None


# Example usage:
# ftp_pkt = IP()/TCP(sport=21, dport=12345)
# analyzer = FTPAnalyzer()
# print(analyzer.is_analyzable(ftp_pkt))
# print(analyzer.get_protocol_name())
