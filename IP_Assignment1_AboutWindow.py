from PyQt5.QtWidgets import QWidget, QLabel, QPushButton
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QPen, QFont
from PyQt5.QtCore import Qt


class AboutWindow(QWidget):
    def __init__(self, parent=None):
        super(AboutWindow, self).__init__(parent)
        self.title = 'About Mini Paint'
        self.x_pos = 650
        self.y_pos = 250
        self.width = 600
        self.height = 450
        self.ui_components()

    def ui_components(self):
        self.setGeometry(self.x_pos, self.y_pos, self.width, self.height)
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon(r'pic\icon\icon_win.png'))

        # reset window color
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)
        # ums logo
        self.label_ums = QLabel(self)
        pixmap = QPixmap(r'pic\logo\UMS_logo.png')
        self.label_ums.setPixmap(pixmap)
        self.label_ums.move(42, 61)
        # mcg logo
        self.label_mcg = QLabel(self)
        pixmap = QPixmap(r'pic\logo\MCG_logo.png')
        self.label_mcg.setPixmap(pixmap)
        self.label_mcg.move(350, 54)
        # message label
        self.label_message01 = QLabel("This product is the assignment for the course \nImage Processing 2020.", self)
        self.label_message01.move(42, 220)
        self.label_message01.setFont(QFont('Arial', 14))
        self.label_message02 = QLabel("©2020 Liew Ming Kai BS18110392. All right reserved.", self)
        self.label_message02.move(42, 350)
        self.label_message02.setFont(QFont('Arial', 9.5))
        # OK button
        self.button = QPushButton('OK', self)
        self.button.move(485, 405)
        self.button.clicked.connect(self.close_win)

    def close_win(self):
        self.close()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.draw_line(qp)
        qp.end()

    @staticmethod
    def draw_line(qp):
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        qp.setPen(pen)
        qp.drawLine(42, 180, 558, 180)
