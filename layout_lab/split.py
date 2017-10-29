from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys




class App(QWidget):
    def __init__(self):
        super().__init__()

        self.resize(200, 200)
        self.my_layout = QVBoxLayout()
        self.pb = QPushButton('Do it', self)
        self.pb.clicked.connect(self.pb_clicked)
        self.top_wgt = QPushButton('top')
        #self.top_wgt.resize(200, 200)
        self.bottom_wgt = QPushButton('bottm')
        #self.bottom_wgt.resize(200, 200)

        self.my_layout.addWidget(self.pb)
        self.my_layout.addWidget(self.top_wgt)
        self.my_layout.addWidget(self.bottom_wgt)

        self.setLayout(self.my_layout)

    def pb_clicked(self):
        print('hello')

        self.wgt = QWidget()
        self.wgt.resize(self.bottom_wgt.width(), self.bottom_wgt.height())

        self.new_wgt = QPushButton('New Label')
        tmp_sp = QSplitter(Qt.Vertical)
        tmp_sp.addWidget(self.bottom_wgt)
        tmp_sp.addWidget(self.new_wgt)

        self.my_layout.removeWidget(self.bottom_wgt)

        self.newlayout = QVBoxLayout()
        self.newlayout.addWidget(tmp_sp)
        self.wgt.setLayout(self.newlayout)
        self.my_layout.addWidget(self.wgt)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    ex = App()

    ex.show()

    sys.exit(app.exec_())