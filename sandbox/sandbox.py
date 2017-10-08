import sys
from PyQt5.QtWidgets import QApplication, QWidget


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setGeometry(0, 0, 1920, 1080)
        self.setWindowTitle('Pi Lovers')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    ex = Window()
    sys.exit(app.exec_())
