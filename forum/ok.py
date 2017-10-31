from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys

class BaseClass(QFrame):
    def __init__(self, base=None, parent=None):
        super(BaseClass, self).__init__(parent)
        self.parent = parent
        self.base = base

        from datetime import datetime
        QLabel(datetime.now().strftime('%H:%M:%S'), self)

        self.setMouseTracking(True)
        self.mouse_pos = QPoint()
        self.setFrameStyle(QFrame.Box)
        #self.show()

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

        # Upper
        self.upper_widget = QFrame()
        self.upper_widget.setStyleSheet("background-color: #fff")
        self.upper_widget.setFrameStyle(QFrame.StyledPanel)
        self.pb = QPushButton('top', self.upper_widget)
        self.pb.resize(self.upper_widget.width(), self.upper_widget.height())
        #self.pb.clicked.connect(self.place_base)

        # Lower
        self.canvas = QWidget()
        self.canvas.setContentsMargins(0,0,0,0)
        self.canvas_layout = QVBoxLayout()
        self.canvas.setLayout(self.canvas_layout)
        self.canvas.setStyleSheet("background-color: #888")

        self.layoutV.addWidget(self.upper_widget)
        self.layoutV.addWidget(self.canvas)

        self.container_in_canvas = QWidget()

        self.setLayout(self.layoutV)

        self.place_base()

    def place_base(self):
        container_wgt = QWidget()
        bs = BaseClass(base=self, parent=container_wgt)
        '''
        container_wgt = BaseClass(base=self, parent=self.canvas)   # Container widget
        '''

        bs.resize(self.canvas.width(), self.canvas.height())

        self.canvas_layout.addWidget(container_wgt)
        self.container_in_canvas = container_wgt
        return


    @pyqtSlot(object, object)
    def split_wgt(self, wgt, orientation):
        if orientation =='T':
            container_wgt = QWidget()
            container_wgt.setContentsMargins(0,0,0,0)

            self.new_wgt = BaseClass(base=self)
            self.new_wgt.resize(wgt.width(), wgt.height())

            #new_items_spltr = self.split_widget(wgt, self.new_wgt, 'V')

            self.new_layout = QVBoxLayout()


            #self.new_layout.addWidget(new_items_spltr)
            self.new_layout.addWidget(self.new_wgt)
            self.new_layout.addWidget(wgt)
            container_wgt.setLayout(self.new_layout)

            self.canvas_layout.replaceWidget(self.container_in_canvas, container_wgt)
            self.container_in_canvas = container_wgt


    def destroy_layout(self, wgt):
        www = wgt.layout()
        QWidget().setLayout(wgt.layout())  # remove the wgt's layout


    def split_widget(self, current_wgt, new_wgt, spltr):
        splitter = QSplitter(Qt.Vertical) if spltr == 'V' else QSplitter(Qt.Horizontal)

        current_wgt.resize(current_wgt.width(), current_wgt.height() /2)

        new_wgt.resize(current_wgt.width(), current_wgt.height() /2)
        splitter.addWidget(current_wgt)
        splitter.addWidget(new_wgt)

        return splitter



if __name__ == '__main__':
    app = QApplication(sys.argv)

    ex = App()

    ex.show()

    sys.exit(app.exec_())