class FreeMemStat:
    def __init__(self):
        self.labels = ["Free Memory"]
        self.types = ["Bytes"]

    def get_name(self):
        return "Free Memory"

    def analyze(self, packets):
        pass  # No implementation as it's not used in the Java code

    def add_packet(self, p):
        pass  # No implementation as it's not used in the Java code

    def get_labels(self):
        return self.labels

    def get_stat_types(self):
        return self.types

    def get_values(self, index):
        if index == 0:
            return [get_free_memory()]  # Simulated Java Runtime.getRuntime().freeMemory()
        else:
            return []

    def clear(self):
        pass  # No implementation as it's not used in the Java code


def get_free_memory():
    import psutil  # Python library for system and process utilities
    return psutil.virtual_memory().available
