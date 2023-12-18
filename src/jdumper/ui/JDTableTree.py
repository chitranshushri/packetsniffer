from javax.swing import JComponent, JTree, JScrollPane
from javax.swing.tree import DefaultMutableTreeNode, DefaultTreeModel, TreePath
from java.awt import BorderLayout
from jpcap.packet import Packet
from java.util import Vector
from jdumper import JDPacketAnalyzerLoader
from jdumper.analyzer import JDPacketAnalyzer

class JDTableTree(JComponent):
    def __init__(self):
        self.root = DefaultMutableTreeNode()
        self.analyzers = JDPacketAnalyzerLoader.getAnalyzers()
        self.tree = JTree(self.root)
        self.tree.setRootVisible(False)
        tree_view = JScrollPane(self.tree)

        self.setLayout(BorderLayout())
        self.add(tree_view, BorderLayout.CENTER)

    def analyze_packet(self, packet):
        is_expanded = [self.tree.isExpanded(TreePath(self.root.getChildAt(i).getPath())) for i in range(self.root.getChildCount())]

        self.root.removeAllChildren()

        for analyzer in self.analyzers:
            if analyzer.isAnalyzable(packet):
                analyzer.analyze(packet)
                node = DefaultMutableTreeNode(analyzer.getProtocolName())
                self.root.add(node)
                names = analyzer.getValueNames()
                values = analyzer.getValues()
                if names is None:
                    continue

                for j in range(len(names)):
                    if isinstance(values[j], Vector):
                        self.add_nodes(node, names[j], values[j])
                    elif values[j] is not None:
                        self.add_node(node, f"{names[j]}: {values[j]}")

        ((DefaultTreeModel)(self.tree.getModel())).nodeStructureChanged(self.root)

        for i in range(min(self.root.getChildCount(), len(is_expanded))):
            if is_expanded[i]:
                self.tree.expandPath(TreePath(self.root.getChildAt(i).getPath()))

    def add_node(self, node, string):
        node.add(DefaultMutableTreeNode(string))

    def add_nodes(self, node, string, vector):
        sub_node = DefaultMutableTreeNode(string)

        for i in range(vector.size()):
            sub_node.add(DefaultMutableTreeNode(vector.elementAt(i)))

        node.add(sub_node)

    def set_user_object(self, node, obj):
        node.setUserObject(obj)
