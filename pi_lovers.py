import random
import sys
from threading import Thread

from PyQt5.QtGui import QPainter, QPainterPath, QColor, QPen, QFont
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt

from Database import Database
from ProcessLines import ProcessLines


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.drawings = []
        self.number_of_drawings = 0
        self.x = random.randrange(0, 1920)
        self.y = random.randrange(0, 1080)
        self.stroke = 1
        self.line_after_processing = ''

        self.database = Database()

        # gender:
        # male = 0
        # female = 1
        self.database.gender = 0

        self.process_lines = ProcessLines()
        self.start_thread()
        self.init_ui()

    def start_thread(self):
        Thread(target=self.run).start()

    def run(self):
        while True:
            self.update()
            Thread(target=self.get_line).start()

    def get_line(self):
        line = self.database.get_line().lower()
        line_processed = self.process_lines.process_line(line)
        self.line_after_processing = line_processed
        print(line)
        if line != line_processed:
            print(line_processed)
            self.database.insert_post(line_processed)

        if self.number_of_drawings > 10:
            self.number_of_drawings = 0
            if self.database.gender == 0:
                self.x = random.randrange(0, 1920)
                self.y = random.randrange(0, 1080)

        ascii_line_processed = '%d' * len(line_processed) % tuple(map(ord, line_processed))

        if self.database.gender == 0:
            line_style = [Qt.SolidLine, Qt.DashLine, Qt.DotLine, Qt.DashDotLine, Qt.DashDotDotLine]
            if len(ascii_line_processed) % 2 == 0:
                final_x = self.x + (len(ascii_line_processed) * random.randrange(1, 3))
                final_y = self.y + (len(ascii_line_processed) * random.randrange(1, 3))
            else:
                final_x = self.x - (len(ascii_line_processed) * random.randrange(1, 3))
                final_y = self.y - (len(ascii_line_processed) * random.randrange(1, 3))
            len_line = int(len(ascii_line_processed) / 3)
            draw = {
                "gender": 1,
                "x": self.x,
                "y": self.y,
                "transparency": random.randrange(0, 255),
                "r": self.get_color_from_str(ascii_line_processed[:len_line]),
                "g": self.get_color_from_str(ascii_line_processed[len_line:len_line * 2]),
                "b": self.get_color_from_str(ascii_line_processed[len_line * 2:]),
                "stroke": len_line / random.randrange(1, 3),
                "style": line_style[random.randrange(0, 4)],
                "between_x": random.randrange(self.x, 1920),
                "between_y": random.randrange(self.y, 1920),
                "final_x": final_x,
                "final_y": final_y
            }
        self.drawings.append(draw)
        self.number_of_drawings += 1

    @staticmethod
    def get_color_from_str(value_str):
        color = 0
        for c in value_str:
            color += int(c)
            if color > 255:
                color = 0
        return color

    def init_ui(self):
        self.setGeometry(0, 0, 1920, 1080)
        self.setWindowTitle('Pi Lovers')
        self.show()

    @staticmethod
    def closeEvent(event):
        event.accept()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        qp.setRenderHint(QPainter.Antialiasing)

        if random.uniform(0, 1) < 0.05:
            self.draw_text(qp)

        if len(self.drawings) > 0:
            self.draw_list(qp)

        qp.end()

    def draw_text(self, qp):
        pen = QPen(QColor(random.randrange(10, 255),
                          random.randrange(10, 255),
                          random.randrange(10, 255),
                          random.randrange(10, 255)))
        qp.setPen(pen)
        qp.setFont(QFont('Decorative', random.randrange(10, 200)))
        qp.drawText(random.randrange(0, 960), random.randrange(0, 540), self.line_after_processing)

    def draw_list(self, qp):
        for d in self.drawings:
            if d["gender"] == 1:
                if d["transparency"] >= 0:
                    self.draw_bezier(qp, d["x"], d["y"], d["between_x"], d["between_y"],
                                     d["transparency"], d["r"], d["g"], d["b"], d["stroke"], d["style"],
                                     d["final_x"], d["final_y"])
                    d["transparency"] -= 10

    @staticmethod
    def draw_bezier(qp, x, y, between_x, between_y, transparency, r, g, b, stroke, style, final_x, final_y):
        path = QPainterPath()
        pen = QPen(QColor(r, g, b, transparency), stroke, style)
        path.moveTo(x, y)
        path.cubicTo(x, y, between_x, between_y, final_x, final_y)
        qp.setPen(pen)
        qp.drawPath(path)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())
