from jpcap.packet import *
from java.awt import *
from java.util import *
from jdumper.stat import JDStatisticsTaker
from jdumper.ui.graph import LineGraph
from jdumper.ui import JDStatFrame

class JDContinuousStatFrame(JDStatFrame):
    lineGraph = None
    
    def __init__(self, packets, count, isTime, staker, statType):
        super(JDContinuousStatFrame, self).__init__(staker.getName() + " [" + staker.getStatTypes()[statType] + "]")
        self.staker = staker
        self.drawTimescale = isTime
        self.count = count
        self.statType = statType
        
        self.lineGraph = LineGraph(staker.getLabels())
        
        self.getContentPane().setLayout(BorderLayout())
        self.getContentPane().add(self.lineGraph, BorderLayout.CENTER)
        self.setSize(400, 400)
        
        if packets is None or len(packets) == 0:
            return
        
        it = iter(packets)
        self.currentSec = packets[0].sec
        self.currentCount = 0
        index = 0
        
        if isTime:
            while index < len(packets):
                p = packets[index]
                index += 1
                
                while index < len(packets) and p.sec - self.currentSec <= count:
                    staker.addPacket(p)
                    p = packets[index]
                    index += 1
                
                if index == len(packets):
                    break
                
                self.currentSec += count
                index -= 1
                self.lineGraph.addValue(staker.getValues(statType))
                staker.clear()
        else:
            while True:
                for i in range(count):
                    try:
                        packet = next(it)
                        self.currentCount += 1
                        staker.addPacket(packet)
                    except StopIteration:
                        break
                
                if not packet:
                    break
                
                self.currentCount = 0
                self.lineGraph.addValue(staker.getValues(statType))
                staker.clear()
    
    def addPacket(self, p):
        self.staker.addPacket(p)
        
        if self.drawTimescale:
            if self.currentSec == 0:
                self.currentSec = p.sec
            
            if p.sec - self.currentSec > self.count:
                self.lineGraph.addValue(self.staker.getValues(self.statType))
                self.staker.clear()
                self.currentSec += self.count
                
                if p.sec - self.currentSec > self.count:
                    while p.sec - self.currentSec - self.count > self.count:
                        self.lineGraph.addValue(self.staker.getValues(self.statType))
        else:
            self.currentCount += 1
            
            if self.currentCount == self.count:
                self.lineGraph.addValue(self.staker.getValues(self.statType))
                self.staker.clear()
                self.currentCount = 0
    
    def clear(self):
        self.currentCount = 0
        self.currentSec = 0
        self.lineGraph.clear()
    
    def fireUpdate(self):
        self.repaint()

    @staticmethod
    def openWindow(packets, staker):
        frame = JDContinuousStatFrame(packets, 5, True, staker, 0)
        frame.setVisible(True)
        return frame
