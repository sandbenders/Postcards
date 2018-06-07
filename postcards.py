import random
import sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from Worker import *
from Entities import *

FACTOR_PAINT_HIT = 1500
SPEED_TO_POSTMAN = 600


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.drawings = []
        self.number_of_drawings = 0
        self.x = random.randrange(0, 1920)
        self.y = random.randrange(0, 1080)
        self.stroke = 1
        self.line_processed = ''

        self.init_ui()

        # read csv and assign cities
        self.entities = Entities()
        self.players = self.entities.random_cities()
        # print the entities
        for entity in self.players:
            print(entity)

        self.threadpool = QThreadPool()
        print("Multithreading with maximum {} threads".format(self.threadpool.maxThreadCount()))

        self.timers = []
        timer_gui = QTimer()
        timer_gui.setInterval(41)
        timer_gui.timeout.connect(self.start_thread_gui)
        timer_gui.start()
        self.timers.append(timer_gui)

        timer_get_line = QTimer()
        timer_get_line.setInterval(1000)
        timer_get_line.timeout.connect(self.start_thread_get_line)
        timer_get_line.start()
        self.timers.append(timer_get_line)

    def random_extract_data_xlsx(self):
        random_sample = self.excel_file.sample()
        return [random_sample.country.all(),
                random_sample.city.all(),
                random_sample.latitude.mean(),
                random_sample.longitude.mean()]

    def init_ui(self):
        self.setGeometry(0, 0, 1920, 1080)
        self.setWindowTitle("Postcards")
        # self.showFullScreen()
        self.show()
        self.setCursor(Qt.BlankCursor)

    def start_thread_gui(self):
        worker_update_gui = Worker(self.update_gui)
        self.threadpool.start(worker_update_gui)

    def start_thread_get_line(self):
        worker_get_line = Worker(self.central_post)
        self.threadpool.start(worker_get_line)

    def update_gui(self):
        self.update()

    def central_post(self):
        for entity in self.players:
            if entity['entity'] != 'postman':
                letters = entity['letters']
                if letters['sending']:
                    letters['to_postman'] -= SPEED_TO_POSTMAN
                    if letters['to_postman'] < 1:
                        letters['to_postman'] = 0
                        letters['sending'] = False
                        self.players[0]['hit']['iteration'] = 512

    @staticmethod
    def get_color_from_str(value_str):
        color = 0
        for c in value_str:
            color += int(c)
            if color > 255:
                color = 0
        return color

    @staticmethod
    def closeEvent(event):
        event.accept()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        qp.setRenderHint(QPainter.Antialiasing)
        self.paint_hits(qp)
        qp.end()

    def paint_hits(self, qp):
        for entity in self.players:
            if entity['hit']['iteration'] > 0:
                size = entity['hit']['size']
                transparency = entity['hit']['iteration']
                if transparency > 256:
                    transparency = (transparency - 512) * -1
                if transparency > 255:
                    transparency = 255
                color = entity['color']
                qp.setPen(QColor(0, 0, 0, 0))
                qp.setBrush((QColor(*color, transparency)))
                qp.drawEllipse(entity['pos']['x'], entity['pos']['y'], size, size)
                if entity['entity'] != 'postman':
                    entity['hit']['iteration'] -= entity['distance'] / FACTOR_PAINT_HIT
                else:
                    entity['hit']['iteration'] -= size / 20


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())
