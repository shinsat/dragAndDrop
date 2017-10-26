
import os
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class BtnManger:
    def __init__(self):
        self.mylist = []

    def addBtn(self, text):
        btn = MyPushButton(text, len(self.mylist))
        btn.setMouseTracking(True)
        btn.setAcceptDrops(True)
        self.mylist.append(btn)
        return btn

    def reorder_widgets(self, splitter):
        for btn in self.mylist:
            btn.id = splitter.indexOf(btn)


class MyPushButton(QPushButton):
    def __init__(self, text, id, parent=None):
        super(MyPushButton, self).__init__(parent)
        self.id = id
        self.setText(text)
        self.setMouseTracking(True)
        self.setAcceptDrops(True)

    def mouseMoveEvent(self, e):

        if e.buttons() != Qt.RightButton:
            return

        mimeData = QMimeData()

        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().topLeft())

        dropAction = drag.exec_(Qt.MoveAction)


class MyWidget(QWidget):
    def __init__(self, parent=None):
        super(MyWidget, self).__init__(parent)
        self.setAcceptDrops(True)
        self.setMouseTracking(True)


        self.buttonMgr = BtnManger()

        self.topbox = QVBoxLayout()
        self.title = QLabel('custom widget')
        self.topbox.addWidget(self.title)

        self.bodybox = QVBoxLayout()
        self.splitterH = QSplitter(Qt.Horizontal)
        self.splitterH.setMouseTracking(True)
        self.splitterV = QSplitter(Qt.Vertical)
        self.splitterV.setMouseTracking(True)

        self.topbox.addLayout(self.bodybox)
        self.bodybox.addWidget(self.splitterH)
        self.bodybox.addWidget(self.splitterV)

        self.setLayout(self.topbox)
        self.mouse_position = QPoint()

        self.current_rows = 0
        self.current_columns = 0
        self.current_width = 0
        self.current_height = 0
        self.wgt_under_cursor = QPushButton()

    def dragEnterEvent(self, e):
        if e.mimeData().hasFormat('text/plain'):
            e.accept()
            #self.current_columns = self.bodybox.columnCount()
            #self.current_rows = self.bodybox.rowCount()
            #self.current_height = self.height()
            #self.current_width = self.width()

        else:
            e.ignore()

    def dragMoveEvent(self, event):
        self.wgt_under_cursor = qApp.widgetAt(QCursor.pos())
        self.mouse_position = event.pos()
        if isinstance(self.wgt_under_cursor, MyPushButton):
            print(self.wgt_under_cursor.id)
        #print(self.wgt_under_cursor)

    def dropEvent(self, e):
        wgt_under = self.wgt_under_cursor
        self.b = self.buttonMgr.addBtn(e.mimeData().text())
        if isinstance(wgt_under, MyPushButton):
            print('inserting at ', wgt_under.id)
            #self.splitterH.insertWidget(wgt_under.id, self.b)  # always left
            self.splitterV.insertWidget(wgt_under.id, self.b)  # always left
        else:
            print('inserting at 0')
            #self.splitterH.insertWidget(0, self.b)  # always left
            self.splitterV.insertWidget(0, self.b)  # always left

        self.buttonMgr.reorder_widgets(self.splitterV)

    def mouseMoveEvent(self, event):
        self.wgt_under_cursor = qApp.widgetAt(QCursor.pos())
        print(self.wgt_under_cursor)
        #print('cursor at ', event.pos())
        if isinstance(self.wgt_under_cursor , MyPushButton):
            print(self.wgt_under_cursor.id, ',', self.wgt_under_cursor.width(), ',', self.wgt_under_cursor.height())

    def get_nearest_position(self, drop_pos):
        width_unit = int(self.current_width / self.current_columns)
        height_unit = int(self.current_height / self.current_rows)

        # get nearest x border
        distances_x = []
        for col in range(self.current_columns):
            distances_x.append(abs(drop_pos.x() - col * width_unit))
        # also add against maximum width
        distances_x.append(abs(drop_pos.x() - self.current_width))

        distance_min_x = 9999999
        x_pos = 0
        for i, dis in enumerate(distances_x):     # determin the minumum distance
            if distance_min_x > dis:
                distance_min_x = dis
                x_pos = i


        # get nearest y border
        distances_y = []
        for row in range(self.current_rows):
            distances_y.append(abs(drop_pos.y() - col * height_unit))
        distances_y.append(abs(drop_pos.y() - self.current_height))

        distance_min_y = 999999
        y_pos = 0
        for i, dis in enumerate(distances_y):
            if distance_min_y > dis:
                distance_min_y = dis
                y_pos = i

        return [x_pos, y_pos]


class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)



        listWidget = QListWidget()
        listWidget.setAcceptDrops(True)
        listWidget.setDragEnabled(True)

        path = os.path.dirname(__file__)
        for image in sorted(os.listdir(os.path.join(path, "images"))):
            if image.endswith(".png"):
                item = QListWidgetItem(
                        image.split(".")[0].capitalize())
                item.setIcon(QIcon(
                        os.path.join(path, "images/%s" % image)))
                listWidget.addItem(item)


        iconListWidget = QListWidget()
        iconListWidget.setAcceptDrops(True)
        iconListWidget.setDragEnabled(True)
        iconListWidget.setViewMode(QListWidget.IconMode)

        tableWidget = QTableWidget()
        tableWidget.setRowCount(5)
        tableWidget.setColumnCount(2)
        tableWidget.setHorizontalHeaderLabels(
                ["Column #1", "Column #2"])
        tableWidget.setAcceptDrops(True)
        tableWidget.setDragEnabled(True)


        myWidget = MyWidget()

        #myWidget.bodybox.addWidget(QPushButton('0,0'), 0, 0)
        #myWidget.bodybox.addWidget(QPushButton('0,1'), 0, 1)
        #myWidget.bodybox.addWidget(QPushButton('1,0'), 1, 0)
        #myWidget.bodybox.addWidget(QPushButton('1,1'), 1, 1)


        editBox = QLineEdit('Drag this', self)
        editBox.setDragEnabled(True)


        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(listWidget)
        splitter.addWidget(iconListWidget)
        splitter.addWidget(tableWidget)
        splitter.addWidget(editBox)
        splitter.addWidget(myWidget)

        layout = QHBoxLayout()
        layout.addWidget(splitter)
        self.setLayout(layout)

        self.setWindowTitle("Drag and Drop")



app = QApplication(sys.argv)
form = Form()
form.show()
app.exec_()

