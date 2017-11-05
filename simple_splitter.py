from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys




class App(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(200, 600)

        self.wgt_list = [
            QLabel('A'),
            QLabel('B'),
            QLabel('C'),
            QLabel('D'),

        ]

        self.wgt1 = QWidget()
        QLabel('wgt1', self.wgt1)
        self.pb = QPushButton('push here', self.wgt1)
        self.pb.setStyleSheet("background-color: #fff")
        self.wgt1.setStyleSheet("background-color: #f0f")

        self.wgt2 = QWidget()
        QLabel('wgt2', self.wgt2)
        self.wgt2.setStyleSheet("background-color: #ff0")
        self.my_layout = QVBoxLayout()

        #my_layout.addWidget(self.wgt1)
        #my_layout.addWidget(self.wgt2)

        self.setLayout(self.my_layout)

        #self.add_splitter()
        self.splitterV = None

        print(self.my_layout.count())
        self.spltr = self.add_splitter()
        self.my_layout.addWidget(self.spltr)
        #my_layout.addWidget(QLabel('x'))
        print(self.my_layout.count())

        self.pb.clicked.connect(self.do_it)


    def do_it(self):
        #self.splitterV.replaceWidget(self.splitterV.indexOf(self.wgt_list[0]), self.wgt_list[3])
        #wgt = self.splitterV.widget(self.splitterV.indexOf(self.wgt_list[0]))
        #print(wgt)
        #wgt.setParent(None)
        #self.splitterV.addWidget(wgt)
        #self.wgt_list[0].setParent(None)
        spliterH = QSplitter(Qt.Horizontal)
        spliterH.addWidget(self.wgt_list[0])
        spliterH.addWidget(self.wgt_list[1])
        spliterH.addWidget(self.wgt_list[2])
        spliterH.addWidget(self.wgt_list[3])
        spliterH.addWidget(self.wgt2)
        #spliterH.addWidget(QLabel('DD'))#self.wgt_list[0])
        self.splitterV.addWidget(spliterH)
        #self.splitterV.addWidget(self.wgt_list[0])
#        self.spltr.replaceWidget(self.spltr.indexOf(self.wgt2), QLabel('replaced'))
        #self.my_layout.addWidget(self.split_ver(QLabel('K'), QLabel('hi')))
        #self.my_layout.addWidget(self.split_ver(self.wgt2, QLabel('hi')))

    def add_splitter(self):
        self.splitterV = QSplitter(Qt.Vertical)
        self.splitterV.addWidget(self.wgt1)

        self.splitterV.addWidget(self.wgt2)

        self.splitterV.addWidget(self.wgt_list[0])
        self.splitterV.addWidget(self.wgt_list[1])
        self.splitterV.addWidget(self.wgt_list[2])
        self.splitterV.addWidget(self.wgt_list[3])

        #splitterV.addWidget(QPushButton('ABC'))
        #splitterV.addWidget(QPushButton('DDD'))
        return self.splitterV

    def split_ver(self, wgt, new_wgt):
        self.splitterV = QSplitter(Qt.Vertical)
        self.splitterV.addWidget(wgt)
        self.splitterV.addWidget(new_wgt)
        return self.splitterV


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()

    ex.show()

    sys.exit(app.exec_())