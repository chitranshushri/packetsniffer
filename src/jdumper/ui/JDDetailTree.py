from jpcap.packet import *
from java.awt import *
from javax.swing import *
from javax.swing.tree import *
from java.util import *
from java.util.List import *

class JDDetailTree(JComponent):
    def __init__(self):
        self.root = DefaultMutableTreeNode()
        self.tree = JTree(self.root)
        self.tree.setRootVisible(False)
        treeView = JScrollPane(self.tree)
        
        self.setLayout(BorderLayout())
        self.add(treeView, BorderLayout.CENTER)
        
    def analyzePacket(self, packet):
        isExpanded = [self.tree.isExpanded(TreePath(root.getChildAt(i).getPath())) for i in range(root.getChildCount())]
        self.root.removeAllChildren()
        
        analyzers = JDPacketAnalyzerLoader.getAnalyzers()
        for analyzer in analyzers:
            if analyzer.isAnalyzable(packet):
                analyzer.analyze(packet)
                node = DefaultMutableTreeNode(analyzer.getProtocolName())
                self.root.add(node)
                names = analyzer.getValueNames()
                values = analyzer.getValues()
                
                for j in range(len(names)):
                    if isinstance(values[j], Vector):
                        self.addNodes(node, names[j], values[j])
                    elif values[j] is not None:
                        self.addNode(node, names[j] + ": " + str(values[j]))
                    else:
                        self.addNode(node, names[j] + ": Not available")
        
        self.tree.getModel().nodeStructureChanged(self.root)
        
        for i in range(min(self.root.getChildCount(), len(isExpanded))):
            if isExpanded[i]:
                self.tree.expandPath(TreePath(root.getChildAt(i).getPath())))
    
    def addNode(self, node, string):
        node.add(DefaultMutableTreeNode(string))
    
    def addNodes(self, node, string, v):
        subnode = DefaultMutableTreeNode(string)
        for i in range(v.size()):
            subnode.add(DefaultMutableTreeNode(v.elementAt(i)))
        node.add(subnode)
    
    def setUserObject(self, node, obj):
        node.setUserObject(obj)
