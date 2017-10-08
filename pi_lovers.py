from Database import Database
from ProcessLines import ProcessLines

import sys
from PyQt5.QtWidgets import QApplication, QWidget
from threading import Thread


class Window(QWidget):
    def __init__(self):
        super().__init__()
        # gender:
        # male = 0
        # female = 1
        self.database = Database()
        self.database.gender = 0
        self.process_lines = ProcessLines()
        self.start_thread()
        self.init_ui()

    def start_thread(self):
        Thread(target=self.run).start()

    def run(self):
        while True:
            line = self.database.get_line().lower()
            line_processed = self.process_lines.process_line(line)
            print(line)
            print(line_processed)
            if line != line_processed:
                self.database.insert_post(line_processed)

    def init_ui(self):
        self.setGeometry(0, 0, 1920, 1080)
        self.setWindowTitle('Pi Lovers')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())
