from java.awt import BorderLayout
from java.awt.event import ActionListener
from java.util import List
from javax.swing import JPanel, JSplitPane, JMenu, JMenuItem, JCheckBoxMenuItem
from javax.swing.event import ListSelectionEvent, ListSelectionListener

class JDTablePane(JPanel, ActionListener, ListSelectionListener):
    def __init__(self, captor):
        self.captor = captor
        self.table = JDTable(self, captor)
        self.tree = JDTableTree()
        self.text = JDTableTextArea()
        self.tableViewMenu = [JMenu("Datalink Layer"), JMenu("Network Layer"), JMenu("Transport Layer"), JMenu("Application Layer")]
        self.analyzers = JDPacketAnalyzerLoader.getAnalyzers()

        for i, analyzer in enumerate(self.analyzers):
            item = JMenu(analyzer.getProtocolName())
            valueNames = analyzer.getValueNames()
            if valueNames is None:
                continue
            for valueName in valueNames:
                subitem = JCheckBoxMenuItem(valueName)
                subitem.setActionCommand(f"TableView{i}")
                subitem.addActionListener(self)
                item.add(subitem)
            self.tableViewMenu[analyzer.layer].add(item)

        splitPane = JSplitPane(JSplitPane.VERTICAL_SPLIT)
        splitPane2 = JSplitPane(JSplitPane.HORIZONTAL_SPLIT)
        splitPane.setTopComponent(self.table)
        splitPane2.setTopComponent(self.tree)
        splitPane2.setBottomComponent(JScrollPane(self.text))
        splitPane.setBottomComponent(splitPane2)
        splitPane.setDividerLocation(200)
        splitPane2.setDividerLocation(200)

        self.setLayout(BorderLayout())
        self.add(splitPane, BorderLayout.CENTER)

        self.loadProperty()
        self.setSize(400, 200)

    def fireTableChanged(self):
        self.table.fireTableChanged()

    def clear(self):
        self.table.clear()

    def setTableViewMenu(self, menu):
        for tableViewMenu in self.tableViewMenu:
            menu.add(tableViewMenu)

    def actionPerformed(self, evt):
        cmd = evt.getActionCommand()

        if cmd.startswith("TableView"):
            index = int(cmd[9:])
            item = evt.getSource()
            self.table.setTableView(self.analyzers[index], item.getText(), item.isSelected())

    def valueChanged(self, evt):
        if evt.getValueIsAdjusting():
            return

        index = evt.getSource().getMinSelectionIndex()
        if index >= 0:
            p = self.captor.getPackets().get(self.table.sorter.getOriginalIndex(index))
            self.tree.analyzePacket(p)
            self.text.showPacket(p)

    def loadProperty(self):
        menus = []
        for tableViewMenu in self.tableViewMenu:
            menus.extend(tableViewMenu.getMenuComponents())

        status = JpcapDumper.preferences.get("TableView", "Ethernet Frame:Source MAC,Ethernet Frame:Destination MAC,IPv4:Source IP,IPv4:Destination IP").split(",")
        for entry in status:
            name, valueName = entry.split(":")
            for menu in menus:
                if menu.getText() == name:
                    valueItems = menu.getMenuComponents()
                    for valueItem in valueItems:
                        if valueName == valueItem.getText():
                            valueItem.setState(True)
                            break
                    break

            for analyzer in self.analyzers:
                if analyzer.getProtocolName() == name:
                    self.table.setTableView(analyzer, valueName, True)
                    break

    def saveProperty(self):
        viewStatus = self.table.getTableViewStatus()
        if viewStatus:
            buf = ",".join(viewStatus)
            JpcapDumper.preferences.put("TableView", buf)
