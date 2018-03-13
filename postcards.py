import random
import sys
import pandas as pd

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from Worker import *
from Entities import *

class Window(QWidget):
    def __init__(self):
        super().__init__()

        # read csv and assign cities
        self.entities = Entities()

        self.drawings = []
        self.number_of_drawings = 0
        self.x = random.randrange(0, 1920)
        self.y = random.randrange(0, 1080)
        self.stroke = 1
        self.line_processed = ''

        self.init_ui()

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
        self.setCursor(Qt.BlankCursor)

    def start_thread_gui(self):
        worker_update_gui = Worker(self.update_gui)
        self.threadpool.start(worker_update_gui)

    def start_thread_get_line(self):
        worker_get_line = Worker(self.get_line)
        self.threadpool.start(worker_get_line)

    def update_gui(self):
        self.update()

    def get_line(self):
        print()

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
        print()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())
