import javax.swing as swing
import java.awt as awt
from java.awt import Color
from javax.swing import BorderFactory, BoxLayout, CompoundBorder, EmptyBorder, JFrame, JLabel, JPanel, SwingConstants


class LineGraph(swing.JPanel):
    DATALINK_LAYER = 0
    NETWORK_LAYER = 1
    TRANSPORT_LAYER = 2
    APPLICATION_LAYER = 3

    def __init__(self, labels, values=None, min_value=Integer.MAX_VALUE, max_value=Integer.MIN_VALUE, auto_min=True, auto_max=True):
        self.labels = labels
        self.values = Vector()
        self.max_value = Long.MIN_VALUE
        self.min_value = Long.MAX_VALUE
        self.auto_max = auto_max
        self.auto_min = auto_min
        self.margin_y = 20
        self.margin_x = 20

        self.colors = [Color.blue, Color.green, Color.yellow.darker(), Color.red, Color.cyan, Color.pink, Color.orange]

        if values is not None:
            for i in range(len(values)):
                self.values.addElement(values[i])
                if auto_min or auto_max:
                    for j in range(len(values[i])):
                        if auto_max and values[i][j] > self.max_value:
                            self.max_value = values[i][j]
                        if auto_min and values[i][j] < self.min_value:
                            self.min_value = values[i][j]

        self.setLayout(BoxLayout(self, BoxLayout.X_AXIS))
        self.add(GraphPane())
        self.add(LabelPane())

    def add_value(self, values):
        self.values.addElement(values)

        if self.auto_min or self.auto_max:
            for i in range(len(values)):
                if self.auto_max and values[i] > self.max_value:
                    self.max_value = values[i]
                if self.auto_min and values[i] < self.min_value:
                    self.min_value = values[i]
        self.repaint()

    def clear(self):
        self.values.removeAllElements()
        self.max_value = Long.MIN_VALUE
        self.min_value = Long.MAX_VALUE
        self.repaint()

    def set_min_value(self, min_value):
        self.min_value = min_value

    def set_max_value(self, max_value):
        self.max_value = max_value

    def set_min_value_auto_set(self, auto_min):
        self.auto_min = auto_min

    def set_max_value_auto_set(self, auto_max):
        self.auto_max = auto_max

    class GraphPane(swing.JPanel):
        def paint_component(self, g):
            super().paint_component(g)

            self.background = Color.white
            if not self.labels or not self.values or not self.values.size():
                return

            ylabelw = 0
            for i in range(4):
                w = g.getFontMetrics().stringWidth(str(float(self.max_value - (self.max_value - self.min_value) * i / 4.0)))
                if w > ylabelw:
                    ylabelw = w

            h = self.getHeight() - self.margin_y - self.margin_y
            w = self.getWidth()
            h2 = self.max_value - self.min_value
            d = (w - self.margin_x - self.margin_x) / (self.values.size() - 1.0)
            x = d + self.margin_x + ylabelw

            g.setColor(Color.black)
            g.drawLine(self.margin_x + ylabelw, 0, self.margin_x + ylabelw, self.getHeight())
            g.setColor(Color.gray)
            for i in range(5):
                y = self.margin_y + (self.getHeight() - self.margin_y - self.margin_y) / 4 * i
                g.drawLine(self.margin_x + ylabelw, y, self.getWidth(), y)
                g.drawString(str(float(self.max_value - (self.max_value - self.min_value) * i / 4.0)),
                             self.margin_x - 5, y)

            vv = self.values.firstElement()
            for i in range(1, self.values.size()):
                x += d
                v = self.values.elementAt(i)

                for j in range(len(v)):
                    c = self.colors[j % len(self.colors)]
                    for k in range(j // len(self.colors)):
                        c.darker()
                    g.setColor(c)

                    g.drawLine(int(x - d), int(h + self.margin_y - (vv[j] - self.min_value) * h / h2), int(x),
                               int(h + self.margin_y - (v[j] - self.min_value) * h / h2))

                vv = v

    class LabelPane(swing.JPanel):
        def __init__(self):
            self.setLayout(BoxLayout(self, BoxLayout.Y_AXIS))
            self.setBackground(Color.white)

            for i in range(len(self.labels)):
                cont = swing.JPanel()
                cont.setLayout(BoxLayout(cont, BoxLayout.X_AXIS))
                cont.setBackground(Color.white)
                label = swing.JLabel(self.labels[i], SwingConstants.LEFT)
                label.setForeground(Color.black)
                box = swing.JLabel("    ")
                box.setOpaque(True)

                c = self.colors[i % len(self.colors)]
                for j in range(i // len(self.colors)):
                    c.darker()
                box.setBackground(c)

                cont.add(box)
                cont.add(swing.Box.create_rigid_area(awt.Dimension(5, 0)))
                cont.add(label)
                cont.setAlignmentX(0.0)
                self.add(cont)
                self.add(swing.Box.create_rigid_area(awt.Dimension(0, 5)))

            self.setBorder(CompoundBorder(BorderFactory.create_line_border(Color.black, 1),
                                          EmptyBorder(10, 10, 10, 10)))

        def get_minimum_size(self):
            return awt.Dimension(50, 1)

    def get_preferred_size(self):
        return awt.Dimension(300, 200)

if __name__ == "__main__":
    labels = ["layout", "box"]
    data = [[1, 1], [2, 4], [3, 2]]

    f = JFrame()
    f.add_window_listener(lambda e: System.exit(0))
    l = LineGraph(labels, None, 0, 10)
    f.get_content_pane().add(l)
    f.pack()
    f.set_visible(True)
