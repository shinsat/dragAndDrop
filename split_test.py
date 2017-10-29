from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys


class BaseClass(QFrame):
    def __init__(self, base=None, parent=None):
        super(BaseClass, self).__init__(parent)
        self.parent = parent
        self.base = base

        self.setMouseTracking(True)
        self.mouse_pos = QPoint()
        self.setFrameStyle(QFrame.Box)
        self.splitter = QSplitter()
        self.show()

    def mouseMoveEvent(self, event):
        self.mouse_pos = event.pos()

    def mousePressEvent(self, event):
        print('mouse pressed at ', event.pos().x(), ',', event.pos().y())
        if event.pos().y() > self.height() /2:
            print("Bottom insert")
            self.base.split_signal.emit(self, 'B')
        else:
            print("Top insert")
            self.base.split_signal.emit(self, 'T')



class App(QWidget):
    split_signal = pyqtSignal(object, object)

    def __init__(self):
        super().__init__()

        self.setGeometry(50, 50, 500, 600)
        self.layoutV = QVBoxLayout()

        self.split_signal.connect(self.split_wgt)

        # 上部画面
        self.upper_widget = QWidget()
        #upper_size_polity = self.upper_widget.sizePolicy()
        #upper_size_polity.setVerticalStretch(1)
        #self.upper_widget.resize(self.width(), self.height() /2)
        self.pb = QPushButton('', self.upper_widget)
        #self.pb.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.pb.resize(self.upper_widget.width(), self.upper_widget.height())
        self.pb.clicked.connect(self.place_base)

        # 下部画面
        self.canvas = QWidget()
        #self.canvas_layout = QVBoxLayout()
        #self.canvas.setLayout(self.canvas_layout)
        #canvas_sizepolity = self.canvas.sizePolicy()
        #canvas_sizepolity.setVerticalStretch(1)
        #self.canvas.resize(self.width(), self.height() /2)

        self.layoutV.addWidget(self.upper_widget)
        self.layoutV.addWidget(self.canvas)


        self.setLayout(self.layoutV)

        #self.pb.setMinimumWidth(self.upper_widget.width())
        #self.pb.setMinimumHeight(self.upper_widget.height())

    def place_base(self):
        container_wgt = BaseClass(base=self, parent=self.canvas)   # 敷物ウィジェット
        container_wgt.resize(self.canvas.width(), self.canvas.height())
        #container_wgt.resize(self.canvas.width(), self.canvas.height())

        #self.base_wgt = BaseClass(parent=container_wgt)
        #self.base_wgt.resize(container_wgt.width(), container_wgt.height())
        #self.layoutV.addWidget(container_wgt)

    @pyqtSlot(object, object)
    def split_wgt(self, wgt, orientation):
        print(wgt, ',', orientation)

        if orientation =='T':
            self.new_wgt = BaseClass(base=self)
            self.new_wgt.resize(wgt.width() /2, wgt.height() /2)

            self.current_wgt_container = QWidget()
            self.current_wgt_container.resize(wgt.width() /2, wgt.height() /2)

            if wgt.layout() == None:
                self.my_layout = QVBoxLayout()
                self.my_layout.addWidget(wgt)
                self.current_wgt_container.setLayout(self.my_layout)

            else:
                self.current_wgt_container.setLayout(wgt.layout())

            self.new_splitter = QSplitter(Qt.Vertical)

            self.new_splitter.addWidget(self.new_wgt)
            self.new_splitter.addWidget(self.current_wgt_container)
            #self.new_splitter.addWidget(QPushButton('bbb'))
            #self.new_splitter.addWidget(QPushButton('ccc'))

            self.new_layout = QVBoxLayout()
            #self.new_layout.insert
            #self.new_layout.addWidget(self.new_splitter)
            #self.new_layout.addWidget(new_wgt)
            #self.new_layout.addWidget(self.current_wgt_container)
            self.new_layout.addWidget(self.new_splitter)

            #self.destroy_layout(self.canvas)
#            self.canvas.setLayout(self.new_layout)
            self.upper_widget.setLayout(self.new_layout)

        elif orientation == 'B':
            new_splitter = QSplitter(Qt.Horizontal)
            new_wgt = BaseClass(base=self)
            new_wgt.resize(wgt.width(), wgt.height())

            new_splitter.addWidget(wgt)
            new_splitter.addWidget(new_wgt)

            my_layout = QHBoxLayout()
            my_layout.addWidget(new_splitter)

            #self.destroy_layout(self.canvas)
            #self.layoutV.removeWidget(self.canvas)
            #self.layoutV.addWidget()

            self.canvas.setLayout(my_layout)


    def destroy_layout(self, wgt):
        www = wgt.layout()
        QWidget().setLayout(wgt.layout())  # remove the wgt's layout



if __name__ == '__main__':
    app = QApplication(sys.argv)

    ex = App()

    ex.show()

    sys.exit(app.exec_())