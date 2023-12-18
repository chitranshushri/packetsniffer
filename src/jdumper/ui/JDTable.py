from javax.swing import JComponent, JScrollPane, JTable, ListSelectionModel
from javax.swing.table import AbstractTableModel
from java.util import Vector
from java.awt import BorderLayout

class JDTable(JComponent):
    def __init__(self, parent, captor):
        self.captor = captor
        self.model = self.JDTableModel()
        self.sorter = TableSorter(self.model)
        table = JTable(self.sorter)
        self.sorter.addMouseListenerToHeaderInTable(table)  # ADDED THIS
        table.setSelectionMode(ListSelectionModel.SINGLE_SELECTION)
        table.getSelectionModel().addListSelectionListener(parent)
        table.setDefaultRenderer(Object, JDTableRenderer())
        tableView = JScrollPane(table)
        self.views = Vector()
        
        self.setLayout(BorderLayout())
        self.add(tableView, BorderLayout.CENTER)
    
    def fireTableChanged(self):
        self.model.fireTableRowsInserted(self.captor.getPackets().size() - 1, self.captor.getPackets().size() - 1)
    
    def clear(self):
        self.model.fireTableStructureChanged()
        self.model.fireTableDataChanged()
    
    def setTableView(self, analyzer, name, set):
        if set:
            self.views.addElement(self.TableView(analyzer, name))
        else:
            for i in range(self.views.size()):
                view = self.views.elementAt(i)
                if view.analyzer == analyzer and view.valueName == name:
                    self.views.removeElement(view)
        
        self.model.fireTableStructureChanged()
    
    def getTableViewStatus(self):
        status = []
        for i in range(self.views.size()):
            view = self.views.elementAt(i)
            status.append(f"{view.analyzer.getProtocolName()}:{view.valueName}")
        
        return status
    
    class TableView:
        def __init__(self, analyzer, name):
            self.analyzer = analyzer
            self.valueName = name
    
    class JDTableModel(AbstractTableModel):
        def getRowCount(self):
            return self.captor.getPackets().size()
        
        def getColumnCount(self):
            return len(self.views) + 1
        
        def getValueAt(self, row, column):
            if self.captor.getPackets().size() <= row:
                return ""
            
            packet = self.captor.getPackets().get(row)
            
            if column == 0:
                return row
            
            view = self.views.elementAt(column - 1)
            if view.analyzer.isAnalyzable(packet):
                with view.analyzer:
                    view.analyzer.analyze(packet)
                    obj = view.analyzer.getValue(view.valueName)
                    
                    if isinstance(obj, Vector):
                        if obj.size() > 0:
                            return obj.elementAt(0)
                        else:
                            return None
                    else:
                        return obj
            else:
                return None
        
        def isCellEditable(self, row, column):
            return False
        
        def getColumnName(self, column):
            if column == 0:
                return "No."
            
            return self.views.elementAt(column - 1).valueName
