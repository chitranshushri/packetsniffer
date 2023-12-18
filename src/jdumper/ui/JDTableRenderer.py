from java.awt import Color
from javax.swing import JLabel, SwingConstants
from javax.swing.table import TableCellRenderer
from javax.swing.border import EmptyBorder

class JDTableRenderer(JLabel, TableCellRenderer):
    noFocusBorder = EmptyBorder(1, 1, 1, 1)

    def __init__(self):
        super(JDTableRenderer, self).__init__()
        self.setOpaque(True)

    def getTableCellRendererComponent(self, table, value, isSelected, hasFocus, row, column):
        if isSelected:
            self.setForeground(table.getSelectionForeground())
            self.setBackground(table.getSelectionBackground())
        else:
            self.setForeground(table.getForeground())
            self.setBackground(table.getBackground())

        self.setFont(table.getFont())

        if hasFocus:
            self.setBorder(UIManager.getBorder("Table.focusCellHighlightBorder"))
        else:
            self.setBorder(self.noFocusBorder)

        if value is None:
            self.setText("Not Available")
            return self

        self.setText(str(value))

        if value.__class__ == Integer or value.__class__ == Long:
            self.setHorizontalAlignment(SwingConstants.RIGHT)

        # Optimization to avoid painting background
        back = self.getBackground()
        colorMatch = (back is not None) and (back.equals(table.getBackground())) and table.isOpaque()
        self.setOpaque(not colorMatch)

        return self
