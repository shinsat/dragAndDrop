from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys




class App(QWidget):
    def __init__(self):
        super().__init__()

        my_layout = QHBoxLayout()

        self.splitterH = QSplitter(Qt.Horizontal)
        self.splitterH.addWidget(QLabel('1'))
        self.splitterH.addWidget(QLabel('2'))
        self.splitterH.addWidget(QLabel('3'))

        pb = QPushButton('replace 2')
        pb.clicked.connect(self.pb_clicked)
        my_layout.addWidget(pb)
        my_layout.addWidget(self.splitterH)

        self.setLayout(my_layout)

    def pb_clicked(self):
        self.splitterH.replaceWidget(1, QLabel('replaced'))


if __name__ == '__main__':
    app = QApplication(sys.argv)

    ex = App()

    ex.show()

    sys.exit(app.exec_())