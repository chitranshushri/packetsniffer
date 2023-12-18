from typing import List
from jdumper.stat import (
    ApplicationProtocolStat,
    FreeMemStat,
    JDStatisticsTaker,
    NetworkProtocolStat,
    PacketStat,
    TransportProtocolStat,
)

class JDStatisticsTakerLoader:
    stakers = []

    @staticmethod
    def load_statistics_taker():
        JDStatisticsTakerLoader.stakers.append(PacketStat())
        JDStatisticsTakerLoader.stakers.append(NetworkProtocolStat())
        JDStatisticsTakerLoader.stakers.append(TransportProtocolStat())
        JDStatisticsTakerLoader.stakers.append(ApplicationProtocolStat())
        JDStatisticsTakerLoader.stakers.append(FreeMemStat())

    @staticmethod
    def get_statistics_takers() -> List:
        return JDStatisticsTakerLoader.stakers

    @staticmethod
    def get_statistics_taker_at(index: int) -> JDStatisticsTaker:
        return JDStatisticsTakerLoader.stakers[index]

# Example usage
JDStatisticsTakerLoader.load_statistics_taker()
statistics_takers = JDStatisticsTakerLoader.get_statistics_takers()
statistics_taker_at_index_0 = JDStatisticsTakerLoader.get_statistics_taker_at(0)
