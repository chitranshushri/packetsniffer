from javax.swing.table import AbstractTableModel
from javax.swing.event import TableModelListener, TableModelEvent

class TableMap(AbstractTableModel, TableModelListener):
    def __init__(self):
        self.model = None

    def getModel(self):
        return self.model

    def setModel(self, model):
        self.model = model
        self.model.addTableModelListener(self)

    # By default, implement TableModel by forwarding all messages to the model.
    def getValueAt(self, aRow, aColumn):
        return self.model.getValueAt(aRow, aColumn)

    def setValueAt(self, aValue, aRow, aColumn):
        self.model.setValueAt(aValue, aRow, aColumn)

    def getRowCount(self):
        return 0 if self.model is None else self.model.getRowCount()

    def getColumnCount(self):
        return 0 if self.model is None else self.model.getColumnCount()

    def getColumnName(self, aColumn):
        return self.model.getColumnName(aColumn)

    def getColumnClass(self, aColumn):
        return self.model.getColumnClass(aColumn)

    def isCellEditable(self, row, column):
        return self.model.isCellEditable(row, column)

    # Implementation of the TableModelListener interface
    # By default, forward all events to all the listeners.
    def tableChanged(self, e):
        self.fireTableChanged(e)
