import random
import sys

import numpy as np

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from Worker import *
from Entities import *

FACTOR_PAINT_HIT = 1500
SPEED_TO_POSTMAN = 600
POSTMAN, FLAUBERT, ELIZABETH, ROBERT = range(0, 4)


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

        self.num_iterations = 0

        # read csv and assign cities
        self.entities = Entities()
        self.players = self.entities.random_cities()

        self.post = []
        for key, player in self.players.items():
            if player['entity'] != 'postman':
                self.post.append([key, player['distance'], player['recipient'], random.randint(1, 4)])

        self.letters = []
        self.letters_content = self.read_letters_content()

        self.text_to_draw = []

        self.type_message = ['bezier',
                             'rect_full',
                             'rect',
                             'ellipse',
                             'triangle']

        self.threadpool = QThreadPool()
        print('Multithreading with maximum {} threads'.format(self.threadpool.maxThreadCount()))

        self.timers = []
        timer_gui = QTimer()
        timer_gui.setInterval(41)
        timer_gui.timeout.connect(self.start_thread_gui)
        timer_gui.start()
        self.timers.append(timer_gui)

        timer_get_line = QTimer()
        timer_get_line.setInterval(1000)
        timer_get_line.timeout.connect(self.start_central_post)
        timer_get_line.start()
        self.timers.append(timer_get_line)

    def read_letters_content(self):
        with open('letters/letters.txt') as f:
            content = f.readlines()
        content = [x.strip() for x in content]
        return content

    def random_extract_data_xlsx(self):
        random_sample = self.excel_file.sample()
        return [random_sample.country.all(),
                random_sample.city.all(),
                random_sample.latitude.mean(),
                random_sample.longitude.mean()]

    def init_ui(self):
        self.setGeometry(0, 0, 1920, 1080)
        self.setWindowTitle("Postcards")
        self.showFullScreen()
        self.setCursor(Qt.BlankCursor)

    def start_thread_gui(self):
        worker_update_gui = Worker(self.update_gui)
        self.threadpool.start(worker_update_gui)

    def start_central_post(self):
        worker_get_line = Worker(self.central_post)
        self.threadpool.start(worker_get_line)

    def update_gui(self):
        self.update()

    def central_post(self):
        for letter in self.post:
            letter[1] -= SPEED_TO_POSTMAN * letter[3]
            if letter[1] < 1:
                if letter[0] != 0:
                    # postman got the letter
                    self.players[0]['hit']['iteration'] = 512
                    self.post.append([0, self.players[letter[2]]['distance'], letter[2], random.randint(1, 4)])
                else:
                    # player got the letter
                    self.add_letter_got_from_player(letter[2])
                    self.players[letter[2]]['hit']['iteration'] = 512
                    self.post.append(
                        [letter[2], self.players[letter[2]]['distance'], self.players[letter[2]]['recipient'],
                         random.randint(1, 4)])
                self.post.remove(letter)
        self.num_iterations += 1
        if self.num_iterations > 10:
            if np.random.rand() < .5:
                self.players = self.entities.random_cities()
            self.num_iterations = 0

    def add_letter_got_from_player(self, player):
        line_style = [Qt.SolidLine, Qt.DashLine, Qt.DotLine, Qt.DashDotLine, Qt.DashDotDotLine]
        type_letter = random.choice(self.type_message)
        params = {}
        x = self.players[player]['pos']['x']
        y = self.players[player]['pos']['y']
        color = list(np.random.randint(0, 255, size=3))
        size = random.randrange(0, 1920)
        if type_letter == 'bezier':
            params = {
                'x': x,
                'y': y,
                'color': color,
                'stroke': random.randrange(1, 1000),
                'style': random.choice(line_style),
                'between_x': random.randrange(x, 1920),
                'between_y': random.randrange(y, 1080),
                'final_x': random.randrange(x, 1920),
                'final_y': random.randrange(y, 1080)
            }
        elif type_letter == 'rect_full':
            params = {
                'x': 0,
                'y': y,
                'color': color,
                'height': random.randrange(0, 1080)
            }
        elif type_letter == 'rect':
            params = {
                'x': x,
                'y': y,
                'color': color,
                'size': size
            }
        elif type_letter == 'ellipse':
            params = {
                'x': x,
                'y': y,
                'color': color,
                'size': size
            }
        elif type_letter == 'triangle':
            params = {
                'x': x,
                'y': y,
                'epx1': random.randrange(0, 1920),
                'epy1': random.randrange(0, 1080),
                'spx2': random.randrange(0, 1920),
                'spy2': random.randrange(0, 1080),
                'epx2': random.randrange(0, 1920),
                'epy2': random.randrange(0, 1080),
                'color': color
            }
        # type_letters, params, transparency
        self.letters.append([type_letter, params, random.randrange(10, 255)])
        if np.random.rand() < .5:
            if np.random.rand() < .5:
                x = random.randrange(0, 1920)
                y = random.randrange(0, 1080)
            self.text_to_draw.append([random.choice(self.letters_content), x, y, random.randrange(5, 1000),
                                          list(np.random.randint(0, 255, size=3)), 255])


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
        self.paint_letters(qp)
        self.paint_text(qp)
        qp.end()

    def paint_hits(self, qp):
        for key, player in self.players.items():
            if player['hit']['iteration'] > 0:
                size = player['hit']['size']
                transparency = player['hit']['iteration']
                if transparency > 256:
                    transparency = (transparency - 512) * -1
                if transparency > 255:
                    transparency = 255
                color = player['color']
                qp.setPen(QColor(0, 0, 0, 0))
                qp.setBrush((QColor(*color, transparency)))
                qp.drawEllipse(player['pos']['x'], player['pos']['y'], size, size)
                if player['entity'] != 'postman':
                    player['hit']['iteration'] -= player['distance'] / FACTOR_PAINT_HIT
                else:
                    player['hit']['iteration'] -= size / 20

    def paint_letters(self, qp):
        for letter in self.letters:
            letter[2] -= 1
            type_letter = letter[0]
            params = letter[1]
            x = params['x']
            y = params['y']
            transparency = letter[2]
            if transparency < 0:
                self.letters.remove(letter)
            else:
                if type_letter == 'bezier':
                    path = QPainterPath()
                    pen = QPen(QColor(*params['color'], transparency), params['stroke'], params['style'])
                    path.moveTo(x, y)
                    path.cubicTo(x, y, params['between_x'], params['between_y'], params['final_x'], params['final_y'])
                    qp.setPen(pen)
                    qp.setBrush(QColor(0, 0, 0, 0))
                    qp.drawPath(path)
                elif type_letter == 'rect_full':
                    qp.setPen(QColor(*params['color'], transparency))
                    qp.setBrush(QColor(*params['color'], transparency))
                    qp.drawRect(x, y, 1920, y + params['height'])
                elif type_letter == 'rect':
                    qp.setPen(QColor(*params['color'], transparency))
                    qp.setBrush(QColor(*params['color'], transparency))
                    qp.drawRect(x, y, params['size'], params['size'])
                elif type_letter == 'ellipse':
                    qp.setPen(QColor(*params['color'], transparency))
                    qp.setBrush(QColor(*params['color'], transparency))
                    qp.drawEllipse(x, y, params['size'], params['size'])
                elif type_letter == 'triangle':
                    path = QPainterPath()
                    qp.setBrush(QColor(*params['color'], transparency))
                    path.moveTo(x, y)
                    path.lineTo(params['epx1'], params['epy1'])
                    path.lineTo(params['epx2'], params['epy2'])
                    path.lineTo(x, y)
                    qp.drawPath(path)

    def paint_text(self, qp):
        for text in self.text_to_draw:
            text[5] -= 1
            if text[5] < 0:
                self.text_to_draw.remove(text)
            else:
                qp.setFont(QFont('Decorative', text[3]))
                qp.setPen(QColor(*text[4], text[5]))
                qp.drawText(text[1], text[2], text[0])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())
