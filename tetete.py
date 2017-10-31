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
        self.pb.clicked.connect(self.place_base)

        # Lower
        self.canvas = QWidget()
        self.canvas.setContentsMargins(0,0,0,0)
        self.canvas_layout = QVBoxLayout()
        self.canvas.setLayout(self.canvas_layout)
        self.canvas.setStyleSheet("background-color: #888")


        self.layoutV.addWidget(self.upper_widget)
        self.layoutV.addWidget(self.canvas)

        self.container_in_canvas = QWidget()
        self.canvas_layout.addWidget(self.container_in_canvas)

        self.setLayout(self.layoutV)


    def place_base(self):
        container_wgt = QWidget()
        bs = BaseClass(base=self, parent=container_wgt)
        '''
        container_wgt = BaseClass(base=self, parent=self.canvas)   # Container widget
        '''

        #bs.resize(self.canvas.width(), self.canvas.height())
        bs.resize(self.container_in_canvas.width(), self.container_in_canvas.height())

        self.canvas_layout.replaceWidget(self.container_in_canvas, container_wgt)
        self.container_in_canvas = container_wgt
        return

        self.layoutV.replaceWidget(self.canvas, container_wgt)
        # remove old one
        self.canvas.hide()
        self.canvas.deleteLater()

        self.canvas = container_wgt


    @pyqtSlot(object, object)
    def split_wgt(self, wgt, orientation):
        if orientation =='T':
            container_wgt = QWidget()
            #container_wgt.setContentsMargins(0,0,0,0)
            #container_wgt.resize(self.container_in_canvas.width(), self.container_in_canvas.height())

            #new_wgt = BaseClass(base=self, parent=container_wgt)
            new_wgt = BaseClass(base=self)

            #print(wgt.width(), ',', wgt.height())
            #new_items_spltr = self.split_widget(QPushButton('b'), new_wgt, 'V', parent=container_wgt)
            pb_1 = QLabel('xxxxxx')
            pb_2 = QLabel('yyyyyy')
            #just_pb.resize(self.canvas.width(), wgt.height() /2)
            #new_items_spltr = self.split_widget(QLabel('ttttt'), new_wgt=wgt, spltr='V', parent=container_wgt)
            #new_items_spltr.setSizes([200,200])
            #wgt.setMinimumHeight(200)
            #new_wgt.resize(self.canvas.width(), wgt.height())
            #new_wgt.setMinimumHeight(300)
            #new_wgt.setMinimumWidth(300)
            #new_items_spltr = self.split_widget(wgt, new_wgt, 'V', parent=container_wgt)
            #new_items_spltr = QSplitter(Qt.Vertical, parent=container_wgt)
            #new_items_spltr.addWidget(wgt)
            #new_items_spltr.addWidget(new_wgt)

            #new_items_spltr.setSizes([100,200])
            #new_items_spltr.setSizes([100, 200])
            #new_layout = QVBoxLayout()

            #new_items_spltr = QSplitter(Qt.Vertical, parent=container_wgt)
            #new_items_spltr.addWidget(QPushButton('upper'))
            #new_items_spltr.addWidget(QPushButton('lower'))
            #self.new_splitter = QSplitter(Qt.Vertical)
            #self.new_layout.addWidget(self.new_splitter)

            #self.new_splitter.addWidget(self.new_wgt)
            #self.new_splitter.addWidget(wgt)
            #self.new_layout.addWidget(new_items_spltr)

            #self.new_layout.addWidget(wgt)
            #self.new_layout.addWidget(QLabel('hello'))

            tmp_sp = QSplitter(Qt.Vertical, parent=new_wgt)
            tmp_sp.addWidget(pb_1)
            tmp_sp.addWidget(pb_2)

            print(wgt.width(), ',', wgt.height())

            #tmp_sp.addWidget(new_wgt)
            #tmp_sp.addWidget(self.upper_widget)
            #aa = QLabel('aa')
            #aa.setMinimumHeight(50)
            #tmp_sp.addWidget(aa)
            #bb = QLabel('bb')
            #bb.setMinimumHeight(50)
            #tmp_sp.addWidget(bb)

            #container_wgt.setGeometry(wgt.pos().x(), wgt.pos().y(), wgt.width(), wgt.height())
            #new_layout.addWidget(tmp_sp)
            #new_layout.addWidget(QLabel('cc'))
            #new_layout.addWidget(QLabel('dd'))
            #self.new_layout.addWidget(self.new_wgt)
            #container_wgt.setLayout(new_layout)
            #container_wgt.resize(wgt.width(), wgt.height())

            print(self.canvas_layout.count())
            #aaa = self.layoutV.replaceWidget(self.canvas, container_wgt)
            aaa = self.canvas_layout.replaceWidget(self.container_in_canvas, new_wgt)
            #aaa = self.canvas_layout.replaceWidget(self.container_in_canvas, tmp_sp)
            #self.canvas_layout.addWidget(tmp_sp)
            #self.canvas_layout.removeWidget(self.container_in_canvas)

            print(self.canvas_layout.count())
            #self.canvas_layout.addWidget(container_wgt)
            #self.layoutV.addWidget(container_wgt)
            #self.destroy_layout(self.canvas)
            #self.canvas.setLayout(tmp_sp)
            print(self.canvas_layout.count())

            #remove old
            self.container_in_canvas.hide()
            self.container_in_canvas.deleteLater()
            #self.canvas = container_wgt


            #self.container_in_canvas = container_wgt
            self.container_in_canvas = new_wgt
            #container_wgt.show()

            print(self.canvas_layout.count())
            #new_wgt.resize(200,200)
            print(wgt.width(), ',', wgt.height())
            #just_pb.resize(wgt.width(), wgt.height() /2)
            container_wgt.resize(wgt.width(), wgt.height())
            pb_1.setMinimumHeight(100)
            pb_2.setMinimumHeight(100)

    def destroy_layout(self, wgt):
        www = wgt.layout()
        QWidget().setLayout(wgt.layout())  # remove the wgt's layout


    def split_widget(self, current_wgt, new_wgt, spltr, parent=None):
        splitter = QSplitter(Qt.Vertical, parent=parent) if spltr == 'V' else QSplitter(Qt.Horizontal, parent=parent)


        splitter.addWidget(current_wgt)
        splitter.addWidget(new_wgt)

        #current_wgt.resize(current_wgt.width(), current_wgt.height() /2)
        #current_wgt.setMinimumHeight(current_wgt.height() /2)

        #new_wgt.resize(current_wgt.width(), current_wgt.height() /2)
        #new_wgt.setMinimumHeight(current_wgt.height() /2)

        return splitter



if __name__ == '__main__':
    app = QApplication(sys.argv)

    ex = App()

    ex.show()

    sys.exit(app.exec_())