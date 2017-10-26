import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class MyWidget(QWidget):
    def __init__(self, myid='X', parent=None):
        super(MyWidget, self).__init__(parent)

        self.setWindowTitle('Its me')

        self.local_layout = QVBoxLayout()
        self.local_layout.addWidget(QLabel('Me'))
        self.setLayout(self.local_layout)
        #self.show()

        self.local_info = myid



class MyCanvas(QWidget):
    def __init__(self, parent=None):
        super(MyCanvas, self).__init__(parent)
        self.setMouseTracking(True)

    def mouseMoveEvent(self, event):
        widget = qApp.widgetAt(QCursor.pos())
        print('cursor at ', event.pos())
        print( widget.width(), ',', widget.height())


if __name__ == '__main__':
    app = QApplication(sys.argv)

    base = MyCanvas()
    layout = QVBoxLayout()

    ex = MyWidget(myid='No1')
    layout.addWidget(ex)
    ex2 = MyWidget(myid='No2')
    layout.addWidget(ex2)

    base.setLayout(layout)
    base.show()


    sys.exit(app.exec_())