from jpcap import *
from java.awt import *
from java.awt.event import *
from javax.swing import *

class JDCaptureDialog(JDialog, ActionListener):
    jpcap = None

    def __init__(self, parent):
        super(JDCaptureDialog, self).__init__(parent, "Choose Device and Options", True)
        self.devices = JpcapCaptor.getDeviceList()
        if not self.devices:
            JOptionPane.showMessageDialog(parent, "No device found.")
            self.dispose()
            return
        else:
            names = [device.description if device.description else device.name for device in self.devices]
            self.adapterComboBox = JComboBox(names)
            
        adapterPane = JPanel()
        adapterPane.add(self.adapterComboBox)
        adapterPane.setBorder(BorderFactory.createTitledBorder("Choose capture device"))
        adapterPane.setAlignmentX(Component.LEFT_ALIGNMENT)
        
        self.promiscCheck = JCheckBox("Put into promiscuous mode")
        self.promiscCheck.setSelected(True)
        self.promiscCheck.setAlignmentX(Component.LEFT_ALIGNMENT)
        
        self.filterField = JTextField(20)
        filterPane = JPanel()
        filterPane.add(JLabel("Filter"))
        filterPane.add(self.filterField)
        filterPane.setBorder(BorderFactory.createTitledBorder("Capture filter"))
        filterPane.setAlignmentX(Component.LEFT_ALIGNMENT)
        
        caplenPane = JPanel()
        caplenPane.setLayout(BoxLayout(caplenPane, BoxLayout.Y_AXIS))
        self.caplenField = JTextField("1514")
        self.caplenField.setEnabled(False)
        self.wholeCheck = JRadioButton("Whole packet")
        self.wholeCheck.setSelected(True)
        self.wholeCheck.setActionCommand("Whole")
        self.wholeCheck.addActionListener(self)
        self.headCheck = JRadioButton("Header only")
        self.headCheck.setActionCommand("Head")
        self.headCheck.addActionListener(self)
        self.userCheck = JRadioButton("Other")
        self.userCheck.setActionCommand("Other")
        self.userCheck.addActionListener(self)
        group = ButtonGroup()
        group.add(self.wholeCheck)
        group.add(self.headCheck)
        group.add(self.userCheck)
        caplenPane.add(self.caplenField)
        caplenPane.add(self.wholeCheck)
        caplenPane.add(self.headCheck)
        caplenPane.add(self.userCheck)
        caplenPane.setBorder(BorderFactory.createTitledBorder("Max capture length"))
        caplenPane.setAlignmentX(Component.RIGHT_ALIGNMENT)
        
        buttonPane = JPanel(FlowLayout(FlowLayout.RIGHT))
        okButton = JButton("OK")
        okButton.setActionCommand("OK")
        okButton.addActionListener(self)
        cancelButton = JButton("Cancel")
        cancelButton.setActionCommand("Cancel")
        cancelButton.addActionListener(self)
        buttonPane.add(okButton)
        buttonPane.add(cancelButton)
        buttonPane.setAlignmentX(Component.RIGHT_ALIGNMENT)
        
        westPane = JPanel()
        westPane.setLayout(BoxLayout(westPane, BoxLayout.Y_AXIS))
        westPane.add(Box.createRigidArea(Dimension(5, 5)))
        westPane.add(adapterPane)
        westPane.add(Box.createRigidArea(Dimension(0, 10)))
        westPane.add(self.promiscCheck)
        westPane.add(Box.createRigidArea(Dimension(0, 10)))
        westPane.add(filterPane)
        westPane.add(Box.createVerticalGlue())
        eastPane = JPanel()
        eastPane.add(Box.createRigidArea(Dimension(5, 5)))
        eastPane.setLayout(BoxLayout(eastPane, BoxLayout.Y_AXIS))
        eastPane.add(caplenPane)
        eastPane.add(Box.createRigidArea(Dimension(5, 30)))
        eastPane.add(buttonPane)
        eastPane.add(Box.createRigidArea(Dimension(5, 5)))
        
        self.getContentPane().setLayout(BoxLayout(self.getContentPane(), BoxLayout.X_AXIS))
        self.getContentPane().add(Box.createRigidArea(Dimension(10, 10)))
        self.getContentPane().add(westPane)
        self.getContentPane().add(Box.createRigidArea(Dimension(10, 10)))
        self.getContentPane().add(eastPane)
        self.getContentPane().add(Box.createRigidArea(Dimension(10, 10)))
        self.pack()
        
        self.setLocation(parent.getLocation().x + 100, parent.getLocation().y + 100)
    
    def actionPerformed(self, evt):
        cmd = evt.getActionCommand()
        if cmd == "Whole":
            self.caplenField.setText("1514")
            self.caplenField.setEnabled(False)
        elif cmd == "Head":
            self.caplenField.setText("68")
            self.caplenField.setEnabled(False)
        elif cmd == "Other":
            self.caplenField.setText("")
            self.caplenField.setEnabled(True)
            self.caplenField.requestFocus()
        elif cmd == "OK":
            try:
                caplen = int(self.caplenField.getText())
                if caplen < 68 or caplen > 1514:
                    JOptionPane.showMessageDialog(None, "Capture length must be between 68 and 1514.")
                    return
                
                self.jpcap = JpcapCaptor.openDevice(
                    self.devices[self.adapterComboBox.getSelectedIndex()],
                    caplen, self.promiscCheck.isSelected(), 50
                )
                if self.filterField.getText() and len(self.filterField.getText()) > 0:
                    self.jpcap.setFilter(self.filterField.getText(), True)
            except NumberFormatException:
                JOptionPane.showMessageDialog(None, "Please input valid integer in capture length.")
            except java.io.IOException as e:
                JOptionPane.showMessageDialog(None, str(e))
                self.jpcap = None
            finally:
                self.dispose()
        elif cmd == "Cancel":
            self.dispose()
    
    @staticmethod
    def get_jpcap(parent):
        JDCaptureDialog(parent).setVisible(True)
        return JDCaptureDialog.jpcap
