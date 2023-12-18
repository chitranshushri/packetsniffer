from typing import List
from jdumper.analyzer import (
    PacketAnalyzer,
    EthernetAnalyzer,
    IPv4Analyzer,
    IPv6Analyzer,
    TCPAnalyzer,
    UDPAnalyzer,
    ICMPAnalyzer,
    HTTPAnalyzer,
    FTPAnalyzer,
    TelnetAnalyzer,
    SSHAnalyzer,
    SMTPAnalyzer,
    POP3Analyzer,
    ARPAnalyzer,
)

class JDPacketAnalyzerLoader:
    analyzers = []
    layer_analyzers = [[] for _ in range(10)]

    @staticmethod
    def load_default_analyzer():
        JDPacketAnalyzerLoader.analyzers.append(PacketAnalyzer())
        JDPacketAnalyzerLoader.analyzers.append(EthernetAnalyzer())
        JDPacketAnalyzerLoader.analyzers.append(IPv4Analyzer())
        JDPacketAnalyzerLoader.analyzers.append(IPv6Analyzer())
        JDPacketAnalyzerLoader.analyzers.append(TCPAnalyzer())
        JDPacketAnalyzerLoader.analyzers.append(UDPAnalyzer())
        JDPacketAnalyzerLoader.analyzers.append(ICMPAnalyzer())
        JDPacketAnalyzerLoader.analyzers.append(HTTPAnalyzer())
        JDPacketAnalyzerLoader.analyzers.append(FTPAnalyzer())
        JDPacketAnalyzerLoader.analyzers.append(TelnetAnalyzer())
        JDPacketAnalyzerLoader.analyzers.append(SSHAnalyzer())
        JDPacketAnalyzerLoader.analyzers.append(SMTPAnalyzer())
        JDPacketAnalyzerLoader.analyzers.append(POP3Analyzer())
        JDPacketAnalyzerLoader.analyzers.append(ARPAnalyzer())

        for analyzer in JDPacketAnalyzerLoader.analyzers:
            JDPacketAnalyzerLoader.layer_analyzers[analyzer.layer].append(analyzer)

    @staticmethod
    def get_analyzers() -> List:
        return JDPacketAnalyzerLoader.analyzers

    @staticmethod
    def get_analyzers_of(layer: int) -> List:
        return JDPacketAnalyzerLoader.layer_analyzers[layer]

# Example usage
JDPacketAnalyzerLoader.load_default_analyzer()
analyzers = JDPacketAnalyzerLoader.get_analyzers()
layer1_analyzers = JDPacketAnalyzerLoader.get_analyzers_of(1)
