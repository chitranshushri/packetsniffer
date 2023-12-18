from abc import ABC, abstractmethod


class JDStatisticsTaker(ABC):
    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def analyze(self, packets):
        pass

    @abstractmethod
    def add_packet(self, p):
        pass

    @abstractmethod
    def get_labels(self):
        pass

    @abstractmethod
    def get_stat_types(self):
        pass

    @abstractmethod
    def get_values(self, index):
        pass

    @abstractmethod
    def clear(self):
        pass

    def new_instance(self):
        return self.__class__()
