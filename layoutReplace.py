from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys


class BaseClass(QWidget):
    def __init__(self, parent=None):
        super(BaseClass, self).__init__(parent)


class App(QWidget):
    def __init__(self):
        super().__init__()

        self.vbox = QVBoxLayout()
        self.lb = QPushButton('label')
#        self.lb.clicked.connect(self.replaceLayout)
        self.lb.clicked.connect(self.replaceLayout)
        self.vbox.addWidget(self.lb)

        self.setLayout(self.vbox)

        self.splitterH = QSplitter(Qt.Horizontal)
        self.splitterV = QSplitter(Qt.Vertical)

    def splitArea(self, pb):

        #self.splitterH.replaceWidget(0, QPushButton('replaced'))
        #return

        current_container = QWidget()
        current_layout = QHBoxLayout()

        self.tmp_sp = QSplitter(Qt.Horizontal)
        self.tmp_sp.addWidget(QPushButton('iiiii'))
        self.tmp_sp.addWidget(QPushButton('x'))

        current_layout.addWidget(self.tmp_sp)
        current_container.setLayout(current_layout)
        print(self.splitterH.count())
        self.splitterH.replaceWidget(1, current_container)
        return

        #current_layout.addWidget(pb)
        #current_container.setLayout(current_layout)

        container = QWidget()
        container_layout = QHBoxLayout()
        container_layout.addWidget(QPushButton('x'))
        container.setLayout(container_layout)


        self.vbox.addWidget(tmp_sp)
        #self.hbox = QHBoxLayout()
        #self.hbox.addWidget(tmp_sp)
        #container.setLayout(self.hbox)
        #self.vbox.addLayout(current_layout)
        #QWidget().setLayout(self.layout()) # remove current layout

#        self.Layout(self.vbox)


    def replaceLayout(self):
        container = QWidget()
        splitterH = QSplitter(Qt.Horizontal)

        self.pb = QPushButton('button')
        self.splitterH.addWidget(self.pb)
        self.abc_pb = QPushButton('ABC')
        self.splitterH.addWidget(self.abc_pb)
        self.abc_pb.clicked.connect(lambda :self.splitArea(self.abc_pb))

        QWidget().setLayout(self.layout()) # remove current layout

        self.newlayout = QVBoxLayout()
        self.newlayout.addWidget(self.splitterH)
        #self.vbox.addLayout(self.newlayout)
        self.setLayout(self.newlayout)



        print('aa', self.splitterH.count())

        return
        QWidget().setLayout(self.layout())

        self.newlayout = QHBoxLayout()
        self.pb = QPushButton('button')
        self.newlayout.addWidget(self.pb)
        self.setLayout(self.newlayout)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()

    ex.show()

    sys.exit(app.exec_())