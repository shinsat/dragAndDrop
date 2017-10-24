

import os
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import copy

class GridManager:
    def __init__(self):
        self.widget_list = {}   # [row, column] = wgt
        self.grid_layout = QGridLayout()
        #self.grid_layout.setSpacing(0)
        #self.grid_layout.setHorizontalSpacing(0)
        #self.grid_layout.setContentsMargins(0,0,0,0)

        self.current_list = {}
        self.first = False

    def choosing_position(self, wgt, row, column):
        self.tmp_list = self.current_list.copy()
        if (row, column) in self.widget_list:
            print('occupied')
            self.tmp_list[max([r[0] for r in self.widget_list.keys()]), column] = wgt
        else:
            self.tmp_list[row, column] = wgt

            #self.grid_layout.addWidget(wgt, row, column)

        self.update_grid(self.current_list, self.tmp_list)
        self.current_list = self.tmp_list.copy()

    def add_widget(self, wgt, row, column):
        if not self.first:
            for row, column in self.current_list.keys():
                if isinstance(self.current_list[row, column], QLabel):
                    self.current_list[row, column].hide()
                    self.current_list.pop(row, column)
                    self.grid_layout.removeWidget(self.current_list[row, column])
                    self.grid_layout.addWidget(wgt, row, column)    # replace 'here' ガイド用のダミーウィジェットのみを正規ものへ置き換えするだけ

            return
        self.first = False

        c = r = 0
        if (row, column) in self.widget_list:
            print('occupied')
            #self.current_list = self.widget_list.copy
            self.widget_list[row +1, column] = wgt
            self.grid_layout.addWidget(wgt, row, column)
        else:
            self.widget_list[row, column] = wgt
            self.grid_layout.addWidget(wgt, row +1, column)
            #self.grid_layout.addWidget(wgt, row, column)

    def remove_widget(self, row, column):
        for i, w, r, c in enumerate(self.widget_list):
            del self.widget_list[i]
            w.deleteLater()

    def update_grid(self, current_list, new_list):
        for w in current_list.values():
            w.hide()
            self.grid_layout.removeWidget(w)

        for pos in new_list.keys():
            print('positioning at ', pos[0],',', pos[1])
            self.grid_layout.addWidget(new_list[pos], pos[0], pos[1])
            new_list[pos].show()


    def capture_current_list(self):
        self.current_list = self.widget_list


class MyWidget(QWidget):
    def __init__(self, parent=None):
        super(MyWidget, self).__init__(parent)
        self.setAcceptDrops(True)
        #self.setMouseTracking(True)
        self.topbox = QVBoxLayout()
        #self.title = QLabel('custom widget')
        #self.topbox.addWidget(self.title)

        self.grid = GridManager()    #QGridLayout()

        self.topbox.addLayout(self.grid.grid_layout)

        self.setLayout(self.topbox)
        self.mouse_position = QPoint()

        self.current_rows = 0
        self.current_columns = 0
        self.current_width = 0
        self.current_height = 0

        self.dragging = False
        self.dragging_position = QPoint()
        self.rowX = self.columnX = 0

        self.dummyWgt = QLabel('here?')


    def dragEnterEvent(self, e):
        if e.mimeData().hasFormat('text/plain'):
            e.accept()
            self.current_columns = self.grid.grid_layout.columnCount()
            self.current_rows = self.grid.grid_layout.rowCount()
            self.current_height = self.height()
            self.current_width = self.width()

            self.dragging = True

            self.grid.capture_current_list()

        else:
            e.ignore()

    def dropEvent(self, e):
        #self.setText(e.mimeData().text())
        #print(self.bodybox.rowCount())
        #print(self.height(),',',self.width())

        #self.bodybox.addWidget(QPushButton(e.mimeData().text()), self.bodybox.rowCount(), 0)
#        position = self.get_nearest_position(e.pos())
#        print('add at (', position[0], ',', position[1], ')')
#        self.bodybox.addWidget(QPushButton(e.mimeData().text()), position[0], position[1])
        self.dragging = False
        if e.mimeData().hasFormat('text/plain'):
            new_pos = self.get_nearest_position(self.dragging_position)
            self.grid.add_widget(QPushButton(e.mimeData().text()), new_pos[0], new_pos[1])
            self.dragging = False

    #def mouseMoveEvent(self, event):
        #self.mouse_position = event.pos()
        #if self.dragging:
        #    position = self.get_nearest_position(self.mouse_position)
        #    print('(', position[0], ',', position[1], ')')

        #print(event.pos())

    def dragMoveEvent(self, event):
        self.dragging_position = event.pos()
        position = self.get_nearest_position(event.pos())
        print('at (', position[0], ',', position[1], ')')
        if self.rowX == position[0] and self.columnY == position[1]:
            return
        # update values
        self.rowX = position[0]
        self.columnY = position[1]
        self.dragging = True
        self.grid.choosing_position(self.dummyWgt, position[0], position[1])

    def get_nearest_position(self, drop_pos):
        '''
        unit_w = max([r[1] for r in self.grid.widget_list.keys()])
        width_unit = self.current_width if unit_w == 0 else int(self.current_width / unit_w)
        unit_h = max([r[0] for r in self.grid.widget_list.keys()])
        height_unit = self.current_height if unit_h == 0 else int(self.current_height / unit_h)
        '''
        width_unit = int(self.current_width / self.current_columns)
        height_unit = int(self.current_height / self.current_rows)

        # get nearest x border
        distances_x = []
        for col in range(self.current_columns):
            distances_x.append(abs(drop_pos.x() - col * width_unit))
        # also add against maximum width
        distances_x.append(abs(drop_pos.x() - self.current_width))

        distance_min_x = 9999999
        selected_col = 0
        for i, dis in enumerate(distances_x):     # determin the minumum distance
            if distance_min_x > dis:
                distance_min_x = dis
                selected_col = i


        # get nearest y border
        distances_y = []
        for row in range(self.current_rows):
            distances_y.append(abs(drop_pos.y() - row * height_unit))
        distances_y.append(abs(drop_pos.y() - self.current_height))

        distance_min_y = 999999
        selected_row = 0
        for i, dis in enumerate(distances_y):
            if distance_min_y > dis:
                distance_min_y = dis
                selected_row = i

        return [selected_row, selected_col]


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

        #myWidget.grid.add_widget(QPushButton('0,0'), 0, 0)
        #myWidget.grid.add_widget(QPushButton('0,1'), 0, 1)
        #myWidget.grid.add_widget(QPushButton('1,0'), 1, 0)
        #myWidget.grid.add_widget(QPushButton('1,1'), 1, 1)

        editBox = QLineEdit('Drag this', self)
        editBox.setDragEnabled(True)


        splitter = QSplitter(Qt.Horizontal)
        #splitter.addWidget(listWidget)
        #splitter.addWidget(iconListWidget)
        #splitter.addWidget(tableWidget)
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

