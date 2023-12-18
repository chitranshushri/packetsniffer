import java.awt as awt
import java.awt.Color as Color
import javax.swing as swing

class PieGraph(swing.JPanel):
    def __init__(self, labels, values):
        self.labels = labels
        self.values = values

        self.colors = [Color.blue, Color.green, Color.yellow, Color.red, Color.cyan, Color.pink, Color.orange]

    def change_value(self, values):
        self.values = values
        self.repaint()

    def paint_component(self, g):
        super().paint_component(g)

        if not self.labels or not self.values:
            return

        r = min(self.getWidth(), self.getHeight()) // 2 - 20
        x, y = self.getWidth() // 2, self.getHeight() // 2
        sum_values = sum(self.values)

        start_angle = 90.0
        for i in range(len(self.values)):
            if self.values[i] == 0:
                continue
            angle = self.values[i] * 360.0 / sum_values

            c = self.colors[i % len(self.colors)]
            for j in range(i // len(self.colors)):
                c.darker()
            g.setColor(c)
            g.fillArc(x - r, y - r, r * 2, r * 2, int(start_angle), int(-angle))

            start_angle -= angle

        start_angle = 90.0
        for i in range(len(self.values)):
            if self.values[i] == 0:
                continue
            angle = self.values[i] * 360.0 / sum_values

            sx = int(math.cos(2 * math.pi * (start_angle - angle / 2) / 360) * (r + 10))
            sy = int(math.sin(2 * math.pi * (start_angle - angle / 2) / 360) * (r + 10))
            g.setColor(Color.black)
            g.drawString(self.labels[i], x + sx, y - sy)

            start_angle -= angle

    def get_preferred_size(self):
        return awt.Dimension(100, 100)
