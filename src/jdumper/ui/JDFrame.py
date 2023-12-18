from java.awt import *
from java.awt.event import *
from javax.swing import *
from jdumper import JDCaptor, JDStatisticsTakerLoader, JpcapDumper, JDFrameUpdater

class JDFrame(JFrame, ActionListener):
    def __init__(self, captor):
        self.captor = captor
        self.tablePane = JDTablePane(captor)
        captor.setJDFrame(self)
        self.setTitle("JpcapDumper Main Window")

        # Create Menu
        menuBar = JMenuBar()
        self.setJMenuBar(menuBar)
        
        # System Menu
        menu = JMenu("System")
        menuBar.add(menu)
        item = JMenuItem("New Window")
        item.setActionCommand("NewWin")
        item.addActionListener(self)
        menu.add(item)
        item = JMenuItem("Exit")
        item.setActionCommand("Exit")
        item.addActionListener(self)
        menu.add(item)
        
        # File Menu
        menu = JMenu("File")
        menuBar.add(menu)
        self.openMenu = JMenuItem("Open")
        self.openMenu.setIcon(self.getImageIcon("/image/open.gif"))
        self.openMenu.setActionCommand("Open")
        self.openMenu.addActionListener(self)
        menu.add(self.openMenu)
        self.saveMenu = JMenuItem("Save")
        self.saveMenu.setIcon(self.getImageIcon("/image/save.gif"))
        self.saveMenu.setActionCommand("Save")
        self.saveMenu.addActionListener(self)
        self.saveMenu.setEnabled(False)
        menu.add(self.saveMenu)

        # Capture Menu
        menu = JMenu("Capture")
        menuBar.add(menu)
        self.captureMenu = JMenuItem("Start")
        self.captureMenu.setIcon(self.getImageIcon("/image/capture.gif"))
        self.captureMenu.setActionCommand("Start")
        self.captureMenu.addActionListener(self)
        menu.add(self.captureMenu)
        self.stopMenu = JMenuItem("Stop")
        self.stopMenu.setIcon(self.getImageIcon("/image/stopcap.gif"))
        self.stopMenu.setActionCommand("Stop")
        self.stopMenu.addActionListener(self)
        self.stopMenu.setEnabled(False)
        menu.add(self.stopMenu)
        
        # Stat Menu
        self.statMenu = JMenu("Statistics")
        menuBar.add(self.statMenu)
        menu = JMenu("Cumulative")
        self.statMenu.add(menu)
        stakers = JDStatisticsTakerLoader.getStatisticsTakers()
        for i in range(len(stakers)):
            item = JMenuItem(stakers[i].getName())
            item.setActionCommand("CUMSTAT" + str(i))
            item.addActionListener(self)
            menu.add(item)
        menu = JMenu("Continuous")
        self.statMenu.add(menu)
        for i in range(len(stakers)):
            item = JMenuItem(stakers[i].getName())
            item.setActionCommand("CONSTAT" + str(i))
            item.addActionListener(self)
            menu.add(item)

        # View menu
        menu = JMenu("View")
        menuBar.add(menu)
        self.tablePane.setTableViewMenu(menu)
        
        # Create Toolbar
        toolbar = JToolBar()
        toolbar.setFloatable(False)
        self.openButton = JButton(self.getImageIcon("/image/open.gif"))
        self.openButton.setActionCommand("Open")
        self.openButton.addActionListener(self)
        toolbar.add(self.openButton)
        self.saveButton = JButton(self.getImageIcon("/image/save.gif"))
        self.saveButton.setActionCommand("Save")
        self.saveButton.addActionListener(self)
        self.saveButton.setEnabled(False)
        toolbar.add(self.saveButton)
        toolbar.addSeparator()
        self.captureButton = JButton(self.getImageIcon("/image/capture.gif"))
        self.captureButton.setActionCommand("Start")
        self.captureButton.addActionListener(self)
        toolbar.add(self.captureButton)
        self.stopButton = JButton(self.getImageIcon("/image/stopcap.gif"))
        self.stopButton.setActionCommand("Stop")
        self.stopButton.addActionListener(self)
        self.stopButton.setEnabled(False)
        toolbar.add(self.stopButton)
        
        self.statusLabel = JLabel("JpcapDumper started.")
        
        self.getContentPane().setLayout(BorderLayout())
        self.getContentPane().add(self.statusLabel, BorderLayout.SOUTH)
        self.getContentPane().add(self.tablePane, BorderLayout.CENTER)
        self.getContentPane().add(toolbar, BorderLayout.NORTH)
        
        self.addWindowListener(WindowAdapter(windowClosing=self.windowClosing))
        
        self.loadProperty()
        # pack()

    def actionPerformed(self, evt):
        cmd = evt.getActionCommand()

        if cmd == "Open":
            self.captor.loadPacketsFromFile()
        elif cmd == "Save":
            self.captor.saveToFile()
        elif cmd == "NewWin":
            JpcapDumper.openNewWindow()
        elif cmd == "Exit":
            self.saveProperty()
            System.exit(0)
        elif cmd == "Start":
            self.captor.capturePacketsFromDevice()
        elif cmd == "Stop":
            self.captor.stopCapture()
        elif cmd.startswith("CUMSTAT"):
            index = int(cmd[7:])
            self.captor.addCumulativeStatFrame(JDStatisticsTakerLoader.getStatisticsTakerAt(index))
        elif cmd.startswith("CONSTAT"):
            index = int(cmd[7:])
            self.captor.addContinuousStatFrame(JDStatisticsTakerLoader.getStatisticsTakerAt(index))

    def clear(self):
        self.tablePane.clear()

    def startUpdating(self):
        JDFrameUpdater.setRepeats(True)
        JDFrameUpdater.start()

    def stopUpdating(self):
        JDFrameUpdater.stop()
        JDFrameUpdater.setRepeats(False)
        JDFrameUpdater.start()

    def windowClosing(self, evt):
        self.saveProperty()
        JpcapDumper.closeWindow(evt.getSource())

    def loadProperty(self):
        self.setSize(int(JpcapDumper.preferences.get("WinWidth", "640")),
                     int(JpcapDumper.preferences.get("WinHeight", "480")))
        self.setLocation(int(JpcapDumper.preferences.get("WinX", "0")),
                         int(JpcapDumper.preferences.get("WinY", "0")))

    def saveProperty(self):
        JpcapDumper.preferences.put("WinWidth", str(self.getBounds().width))
        JpcapDumper.preferences.put("WinHeight", str(self.getBounds().height))
        JpcapDumper.preferences.put("WinX", str(self.getBounds().x))
        JpcapDumper.preferences.put("WinY", str(self.getBounds().y))

        self.tablePane.saveProperty()
        JpcapDumper.saveProperty()

    def enableCapture(self):
        self.openMenu.setEnabled(True)
        self.openButton.setEnabled(True)
        self.saveMenu.setEnabled(True)
        self.saveButton.setEnabled(True)
        self.captureMenu.setEnabled(True)
        self.captureButton.setEnabled(True)
        self.stopMenu.setEnabled(False)
        self.stopButton.setEnabled(False)

    def disableCapture(self):
        self.openMenu.setEnabled(False)
        self.openButton.setEnabled(False)
        self.captureMenu.setEnabled(False)
        self.captureButton.setEnabled(False)
        self.saveMenu.setEnabled(True)
        self.saveButton.setEnabled(True)
        self.stopMenu.setEnabled(True)
        self.stopButton.setEnabled(True)

    def getImageIcon(self, path):
        return ImageIcon(self.getClass().getResource(path))
