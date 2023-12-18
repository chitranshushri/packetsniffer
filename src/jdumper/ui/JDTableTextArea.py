from javax.swing import JTextArea

class JDTableTextArea(JTextArea):
    def __init__(self):
        super(JDTableTextArea, self).__init__()
        self.setLineWrap(True)
        self.setEditable(False)

    def showPacket(self, p):
        bytes = bytearray(p.header + p.data)

        buf = []
        i = 0
        while i < len(bytes):
            j = 0
            line = ''
            while j < 8 and i < len(bytes):
                d = format(bytes[i], '02x')
                line += f"{d} "
                if bytes[i] < 32 or bytes[i] > 126:
                    bytes[i] = 46  # Replace non-printable characters with '.'
                j += 1
                i += 1
            buf.append(f"[{' '.join(line.split())}]" + "\n")
        text = ''.join(buf)
        self.setText(text)
        self.setCaretPosition(0)
