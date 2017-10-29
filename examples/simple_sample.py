import os
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class MyWidget(QWidget):
    def __init__(self, parent=None):
        super(MyWidget, self).__init__(parent)

        self.setMouseTracking(True)
        self.setAcceptDrops(True)
        self.setAcceptDrops(True)

        self.mouse_pos = QPoint()

    def mouseMoveEvent(self, QMouseEvent):
        self.mouse_pos = QMouseEvent.pos()
        print(self.mouse_pos)


class Form(QWidget):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.setMouseTracking(True)
        self.setAcceptDrops(True)
        self.setAcceptDrops(True)

        self.main_layout = QHBoxLayout()
        self.wgt = MyWidget()
        self.main_layout.addWidget(self.wgt)
        self.wgt2 = MyWidget()
        self.main_layout.addWidget(self.wgt2)

        self.setLayout(self.main_layout)



if __name__ == '__main__':
    app = QApplication(sys.argv)

    form = Form()
    form.show()

    app.exec_()