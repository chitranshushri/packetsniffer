from jpcap.packet import *
from java.awt import *
from javax.swing import *
from javax.swing.event import *
from javax.swing.table import *
from jdumper.stat import JDStatisticsTaker
from jdumper.ui.graph import PieGraph

class JDCumlativeStatFrame(JDStatFrame, ListSelectionListener):
    def __init__(self, packets, staker):
        super(JDCumlativeStatFrame, self).__init__(staker.getName())
        self.staker = staker
        self.staker.analyze(packets)
        
        self.getContentPane().setLayout(BoxLayout(getContentPane(), BoxLayout.Y_AXIS))
        
        self.model = self.TableModel()
        self.table = JTable(self.model)
        self.table.setSelectionMode(ListSelectionModel.SINGLE_SELECTION)
        header = self.table.getTableHeader()
        dim = header.getPreferredSize()
        dim.height = 20
        header.setPreferredSize(dim)
        tablePane = JScrollPane(self.table)
        dim = self.table.getMinimumSize()
        dim.height += 25
        tablePane.setPreferredSize(dim)
        
        if len(self.staker.getLabels()) > 1:
            self.pieGraph = PieGraph(self.staker.getLabels(), self.staker.getValues(0))
            splitPane = JSplitPane(JSplitPane.VERTICAL_SPLIT)
            splitPane.setTopComponent(tablePane)
            splitPane.setBottomComponent(self.pieGraph)
            self.getContentPane().add(splitPane)
            self.table.getSelectionModel().addListSelectionListener(self)
        else:
            self.getContentPane().add(tablePane)
        
        self.setSize(400, 400)
    
    def fireUpdate(self):
        sel = self.table.getSelectedRow()
        if self.pieGraph:
            self.pieGraph.changeValue(self.staker.getValues(self.statType))
        if self.model:
            self.model.update()
        if sel >= 0:
            self.table.setRowSelectionInterval(sel, sel)
        self.repaint()
    
    def addPacket(self, p):
        self.staker.addPacket(p)
    
    def clear(self):
        self.staker.clear()
        if self.pieGraph:
            self.pieGraph.changeValue(self.staker.getValues(self.statType))
        if self.model:
            self.model.update()
    
    def valueChanged(self, evt):
        if evt.getValueIsAdjusting():
            return
        
        lsm = evt.getSource()
        if lsm.isSelectionEmpty():
            self.statType = 0
        else:
            self.statType = lsm.getMinSelectionIndex()
        self.pieGraph.changeValue(self.staker.getValues(self.statType))
    
    class TableModel(AbstractTableModel):
        def __init__(self):
            self.labels = [""]
            self.labels.extend(staker.getLabels())
            
            types = staker.getStatTypes()
            self.values = []
            for i in range(len(types)):
                row = [types[i]]
                v = staker.getValues(i)
                row.extend([Long(val) for val in v])
                self.values.append(row)
        
        def getColumnName(self, c):
            return self.labels[c]
        
        def getColumnCount(self):
            return len(self.labels)
        
        def getRowCount(self):
            return len(self.values)
        
        def getValueAt(self, row, column):
            return self.values[row][column]
        
        def update(self):
            self.values = []
            types = staker.getStatTypes()
            for i in range(len(types)):
                row = [types[i]]
                v = staker.getValues(i)
                row.extend([Long(val) for val in v])
                self.values.append(row)
            self.fireTableDataChanged()
