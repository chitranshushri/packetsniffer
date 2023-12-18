from scapy.all import *

class HTTPAnalyzer:
    def __init__(self):
        self.layer = "APPLICATION_LAYER"
        self.value_names = ["Method", "Header"]
        self.method = ""
        self.headers = []

    def is_analyzable(self, pkt):
        return (
            isinstance(pkt, TCP)
            and (pkt.sport == 80 or pkt.dport == 80)
        )

    def get_protocol_name(self):
        return "HTTP"

    def get_value_names(self):
        return self.value_names

    def analyze(self, pkt):
        self.method = ""
        self.headers = []
        if not self.is_analyzable(pkt):
            return

        try:
            data_str = pkt.load.decode("utf-8")
            data_lines = data_str.splitlines()

            self.method = data_lines[0]

            if "HTTP" not in self.method:
                # This packet doesn't contain an HTTP header
                self.method = "Not HTTP Header"
                return

            # Read headers
            header_lines = data_lines[1:]
            self.headers = header_lines

        except UnicodeDecodeError:
            # Handle UnicodeDecodeError if the data cannot be decoded
            pass

    def get_value(self, value_name):
        if value_name == self.value_names[0]:
            return self.method
        elif value_name == self.value_names[1]:
            return self.headers
        return None

    def get_value_at(self, index):
        if index == 0:
            return self.method
        elif index == 1:
            return self.headers
        return None

    def get_values(self):
        return [self.method, self.headers]


# Example usage:
# http_pkt = IP()/TCP(sport=12345, dport=80)/b'GET / HTTP/1.1\r\nHost: example.com\r\n\r\n'
# analyzer = HTTPAnalyzer()
# analyzer.analyze(http_pkt)
# print(analyzer.get_value_names())
# print(analyzer.get_values())
