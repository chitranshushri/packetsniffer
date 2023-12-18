class TransportProtocolStat:
    types = ["# of packets", "% of packets", "total packet size", "% of size"]
    
    def __init__(self):
        self.analyzers = []  # Placeholder for analyzer list
        self.num_of_ps = []
        self.size_of_ps = []
        self.total_ps = 0
        self.total_size = 0
        self.labels = []

    def get_name(self):
        return "Transport Layer Protocol Ratio"

    def analyze(self, packets):
        self.analyzers = []  # Placeholder for analyzer list
        for packet in packets:
            self.total_ps += 1
            # Placeholder for isAnalyzable method
            flag = False
            for analyzer in self.analyzers:
                if analyzer.isAnalyzable(packet):  # Implement isAnalyzable method accordingly
                    index = self.analyzers.index(analyzer)
                    self.num_of_ps[index] += 1
                    self.size_of_ps[index] += packet.length  # Assuming length is available in the packet
                    self.total_size += packet.length
                    flag = True
                    break
            if not flag:
                self.num_of_ps[-1] += 1
                self.size_of_ps[-1] += packet.len - 12
                self.total_size += packet.len - 12

    def add_packet(self, p):
        self.total_ps += 1
        flag = False
        for analyzer in self.analyzers:
            if analyzer.isAnalyzable(p):  # Implement isAnalyzable method accordingly
                index = self.analyzers.index(analyzer)
                self.num_of_ps[index] += 1
                self.size_of_ps[index] += p.length  # Assuming length is available in the packet
                self.total_size += p.length
                flag = True
                break
        if not flag:
            self.num_of_ps[-1] += 1
            self.size_of_ps[-1] += p.len - 12
            self.total_size += p.len - 12

    def get_labels(self):
        return self.labels

    def get_stat_types(self):
        return self.types

    def get_values(self, index):
        if index == 0:  # # of packets
            if not self.num_of_ps:
                return []
            return self.num_of_ps
        elif index == 1:  # % of packets
            percents = [(num * 100 // self.total_ps) if self.total_ps != 0 else 0 for num in self.num_of_ps]
            return percents
        elif index == 2:  # total packet size
            if not self.size_of_ps:
                return []
            return self.size_of_ps
        elif index == 3:  # % of size
            percents = [(size * 100 // self.total_size) if self.total_size != 0 else 0 for size in self.size_of_ps]
            return percents
        else:
            return None

    def clear(self):
        self.num_of_ps = []
        self.size_of_ps = []
        self.total_ps = 0
        self.total_size = 0
