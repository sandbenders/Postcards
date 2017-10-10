import random
import traceback, sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from Database import Database
from ProcessLines import ProcessLines


class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        `tuple` (exctype, value, traceback.format_exc() )

    result
        `object` data returned from processing, anything

    progress
        `int` indicating % progress

    '''
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)


class Worker(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''

        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done


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
        self.database.gender = 1

        self.process_lines = ProcessLines()

        self.init_ui()

        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

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

    def start_thread_gui(self):
        worker_update_gui = Worker(self.update_gui)
        self.threadpool.start(worker_update_gui)

    def start_thread_get_line(self):
        worker_get_line = Worker(self.get_line)
        self.threadpool.start(worker_get_line)

    def update_gui(self):
        self.update()

    def get_line(self):
        line = self.database.get_line().lower()
        line_processed = self.process_lines.process_line(line)
        self.line_after_processing = line_processed
        print(line)
        if line != line_processed:
            print(line_processed)
            self.database.insert_post(line_processed)

        if self.number_of_drawings > random.randrange(1, 10):
            self.number_of_drawings = 0
            if self.database.gender == 0:
                self.x = random.randrange(0, 1920)
                self.y = random.randrange(0, 1080)

        ascii_line_processed = '%d' * len(line_processed) % tuple(map(ord, line_processed))

        len_line = int(len(ascii_line_processed) / 3)

        if self.database.gender == 0:
            line_style = [Qt.SolidLine, Qt.DashLine, Qt.DotLine, Qt.DashDotLine, Qt.DashDotDotLine]
            if len(ascii_line_processed) % 2 == 0:
                final_x = self.x + (len(ascii_line_processed) * random.randrange(1, 3))
                final_y = self.y + (len(ascii_line_processed) * random.randrange(1, 3))
            else:
                final_x = self.x - (len(ascii_line_processed) * random.randrange(1, 3))
                final_y = self.y - (len(ascii_line_processed) * random.randrange(1, 3))
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
        else:
            height_rect = len(ascii_line_processed) * random.randrange(1, 3)
            draw = {
                "gender": 0,
                "x": 0,
                "y": self.y,
                "transparency": random.randrange(0, 255),
                "r": self.get_color_from_str(ascii_line_processed[:len_line]),
                "g": self.get_color_from_str(ascii_line_processed[len_line:len_line * 2]),
                "b": self.get_color_from_str(ascii_line_processed[len_line * 2:]),
                "height": height_rect
            }
            self.y += height_rect
            if self.y > 1080:
                self.y = 0

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
        self.showFullScreen()

    @staticmethod
    def closeEvent(event):
        event.accept()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        qp.setRenderHint(QPainter.Antialiasing)
        if len(self.drawings) > 0:
            self.draw_list(qp)
        qp.end()

    def draw_text(self, qp):
        pen = QPen(QColor(random.randrange(10, 255),
                          random.randrange(10, 255),
                          random.randrange(10, 255),
                          random.randrange(10, 255)))
        qp.setPen(pen)
        qp.setFont(QFont('Decorative', random.randrange(5, 1000)))
        qp.drawText(random.randrange(0, 1920), random.randrange(0, 1080), self.line_after_processing)

    def draw_list(self, qp):
        for d in self.drawings:
            if d["transparency"] >= 0:
                if d["gender"] == 1:
                    self.draw_bezier(qp, d["x"], d["y"], d["between_x"], d["between_y"],
                                     d["transparency"], d["r"], d["g"], d["b"], d["stroke"], d["style"],
                                     d["final_x"], d["final_y"])
                else:
                    self.draw_rect(qp, d["x"], d["y"], d["transparency"], d["r"], d["g"], d["b"], d["height"])
                d["transparency"] -= 2

    def draw_rect(self, qp, x, y, transparency, r, g, b, height):
        qp.setPen((QColor(r, g, b, transparency)))
        qp.setBrush(QColor(r, g, b, transparency))
        qp.drawRect(x, y, 1920, y + height)
        if random.uniform(0, 1) < 0.05:
            self.draw_text(qp)

    def draw_bezier(self, qp, x, y, between_x, between_y, transparency, r, g, b, stroke, style, final_x, final_y):
        if random.uniform(0, 1) < 0.05:
            self.draw_text(qp)
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
