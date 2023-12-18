from datetime import datetime

class PacketStat:
    types = [
        "Total packet #",
        "Total packet size",
        "Average packet size",
        "bits/s",
        "pkts/s"
    ]
    label = ["Value"]

    def __init__(self):
        self.num_of_ps = 0
        self.size_of_ps = 0
        self.first = None
        self.last = None

    def get_name(self):
        return "Overall information"

    def analyze(self, packets):
        if len(packets) > 0:
            self.first = datetime.fromtimestamp(packets[0].sec + packets[0].usec / 1000)
            self.last = datetime.fromtimestamp(packets[-1].sec + packets[-1].usec / 1000)

        for packet in packets:
            self.num_of_ps += 1
            self.size_of_ps += packet.len

    def add_packet(self, p):
        if self.first is None:
            self.first = datetime.fromtimestamp(p.sec + p.usec / 1000)
        self.last = datetime.fromtimestamp(p.sec + p.usec / 1000)

        self.num_of_ps += 1
        self.size_of_ps += p.len

    def get_labels(self):
        return self.label

    def get_stat_types(self):
        return self.types

    def get_values(self, index):
        ret = [0]
        if index == 0:  # Total packet #
            ret[0] = self.num_of_ps
        elif index == 1:  # Total packet size
            ret[0] = self.size_of_ps
        elif index == 2:  # Average packet size
            ret[0] = self.size_of_ps // self.num_of_ps if self.num_of_ps != 0 else 0
        elif index == 3 or index == 4:  # bits/s or pkts/s
            if self.first is not None:
                sec = (self.last - self.first).total_seconds() * 1000
                if sec != 0:
                    ret[0] = (self.size_of_ps * 8 // sec) if index == 3 else (self.num_of_ps // sec)
        return ret

    def clear(self):
        self.num_of_ps = 0
        self.size_of_ps = 0
        self.first = None
        self.last = None
