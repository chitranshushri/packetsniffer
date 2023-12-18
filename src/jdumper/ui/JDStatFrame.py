from java.awt.event import ActionListener
from javax.swing import JFrame, Timer

class JDStatFrame(JFrame):
    def __init__(self, title):
        super(JDStatFrame, self).__init__(title)
        self.JDStatFrameUpdater = Timer(500, self.ActionHandler())
        self.JDStatFrameUpdater.start()
        self.addWindowListener(self.WindowAdapter())
        
    def fireUpdate(self):
        pass
    
    def addPacket(self, p):
        pass
    
    def clear(self):
        pass
    
    def startUpdating(self):
        self.JDStatFrameUpdater.setRepeats(True)
        self.JDStatFrameUpdater.start()
    
    def stopUpdating(self):
        self.JDStatFrameUpdater.stop()
        self.JDStatFrameUpdater.setRepeats(False)
        self.JDStatFrameUpdater.start()
    
    class ActionHandler(ActionListener):
        def actionPerformed(self, evt):
            self.fireUpdate()
            self.repaint()
    
    class WindowAdapter(java.awt.event.WindowAdapter):
        def windowClosed(self, evt):
            # hide()
            self.setVisible(False)
