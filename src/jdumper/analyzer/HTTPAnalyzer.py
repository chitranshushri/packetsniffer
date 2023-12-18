from jpcap.packet import Packet
from jdumper.analyzer import JDPacketAnalyzer
from io import StringIO

class HTTPAnalyzer(JDPacketAnalyzer):
    value_names = [
        "Method",
        "Header"
    ]
    
    def __init__(self):
        self.method = ""
        self.headers = []
        self.layer = self.APPLICATION_LAYER
    
    def is_analyzable(self, p):
        return isinstance(p, TCPPacket) and (
                (p.src_port == 80) or (p.dst_port == 80)
        )
    
    def get_protocol_name(self):
        return "HTTP"
    
    def get_value_names(self):
        return self.value_names
    
    def analyze(self, p):
        self.method = ""
        self.headers.clear()
        
        if not self.is_analyzable(p):
            return
        
        try:
            data_str = p.data.decode('utf-8')
            data_stream = StringIO(data_str)
            lines = data_stream.readlines()
            
            if len(lines) < 1 or not lines[0].startswith("HTTP"):
                self.method = "Not HTTP Header"
                return
            
            self.method = lines[0].strip()
            self.headers = [line.strip() for line in lines[1:] if line.strip()]
            
        except UnicodeDecodeError as e:
            # Handle decoding errors
            print(f"Error decoding packet data: {e}")
            self.method = "Decoding Error"
    
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
