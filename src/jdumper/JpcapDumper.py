import sys
from java.util.prefs import BackingStoreException, Preferences
from javax.swing import JOptionPane, UIManager

from jdumper import JDPacketAnalyzerLoader, JDStatisticsTakerLoader
from jdumper.ui import JDFrame
from jdumper.JDCaptor import JDCaptor

class JpcapDumper:
    preferences = None
    chooser = None
    frames = []

    @staticmethod
    def main(args):
        UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName())
        JpcapDumper.chooser = javax.swing.JFileChooser()

        try:
            Class.forName("jpcap.JpcapCaptor")
            devices = jpcap.JpcapCaptor.getDeviceList()
            if len(devices) == 0:
                JOptionPane.showMessageDialog(
                    None,
                    "No network interface found.\nYou need to be admin/su to capture packets.",
                    "Warning",
                    JOptionPane.WARNING_MESSAGE,
                )
        except ClassNotFoundException:
            JOptionPane.showMessageDialog(
                None, "Cannot find Jpcap. Please install Jpcap.", "Error", JOptionPane.ERROR_MESSAGE
            )
            sys.exit(-1)
        except UnsatisfiedLinkError:
            JOptionPane.showMessageDialog(
                None,
                "Cannot find Jpcap and/or libpcap/WinPcap.\n Please install Jpcap and libpcap/WinPcap.",
                "Error",
                JOptionPane.ERROR_MESSAGE,
            )
            sys.exit(-1)

        JpcapDumper.preferences = Preferences.userNodeForPackage(JpcapDumper)
        JDPacketAnalyzerLoader.load_default_analyzer()
        JDStatisticsTakerLoader.load_statistics_taker()
        JpcapDumper.open_new_window()

    @staticmethod
    def save_property():
        try:
            JpcapDumper.preferences.flush()
        except BackingStoreException:
            JOptionPane.showMessageDialog(
                None, "Could not save preferences.", "Error", JOptionPane.ERROR_MESSAGE
            )

    @staticmethod
    def open_new_window():
        captor = JDCaptor()
        JpcapDumper.frames.append(JDFrame.open_new_window(captor))

    @staticmethod
    def close_window(frame):
        frame.captor.stop_capture()
        frame.captor.save_if_not()
        frame.captor.close_all_windows()
        JpcapDumper.frames.remove(frame)
        frame.dispose()
        if not JpcapDumper.frames:
            JpcapDumper.save_property()
            sys.exit(0)

    def __del__(self):
        JpcapDumper.save_property()

# Example usage
if __name__ == "__main__":
    JpcapDumper.main(sys.argv)
