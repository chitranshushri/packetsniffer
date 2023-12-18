class NetworkProtocolStat:
    def __init__(self):
        self.analyzers = []  # To be initialized using JDPacketAnalyzerLoader in Java
        self.num_of_ps = []
        self.total_ps = 0
        self.size_of_ps = []
        self.total_size = 0
        self.labels = []
        self.types = ["# of packets", "% of packets", "total packet size", "% of size"]

    def get_name(self):
        return "Network Layer Protocol Ratio"

    def analyze(self, packets):
        for p in packets:
            self.total_ps += 1
            self.total_size += p.len

            flag = False
            for analyzer in self.analyzers:
                if analyzer.is_analyzable(p):
                    index = self.analyzers.index(analyzer)
                    self.num_of_ps[index] += 1
                    self.total_ps += 1
                    self.size_of_ps[index] += p.len
                    flag = True
                    break

            if not flag:
                self.num_of_ps[-1] += 1
                self.size_of_ps[-1] += p.len

    def add_packet(self, p):
        flag = False
        self.total_ps += 1
        self.total_size += p.len
        for analyzer in self.analyzers:
            if analyzer.is_analyzable(p):
                index = self.analyzers.index(analyzer)
                self.num_of_ps[index] += 1
                self.size_of_ps[index] += p.len
                flag = True
                break

        if not flag:
            self.num_of_ps[-1] += 1
            self.size_of_ps[-1] += p.len

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
            percents = []
            if self.total_ps == 0:
                return percents
            for num in self.num_of_ps:
                percents.append(num * 100 // self.total_ps)
            return percents
        elif index == 2:  # total packet size
            if not self.size_of_ps:
                return []
            return self.size_of_ps
        elif index == 3:  # % of size
            percents = []
            if self.total_size == 0:
                return percents
            for size in self.size_of_ps:
                percents.append(size * 100 // self.total_size)
            return percents
        else:
            return None

    def clear(self):
        self.num_of_ps = [0] * (len(self.analyzers) + 1)
        self.size_of_ps = [0] * (len(self.analyzers) + 1)
        self.total_ps = 0
        self.total_size = 0
