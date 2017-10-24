#!/usr/bin/env python
# Copyright (c) 2007-8 Qtrac Ltd. All rights reserved.
# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 2 of the License, or
# version 3 of the License, or (at your option) any later version. It is
# provided for educational purposes and is distributed in the hope that
# it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU General Public License for more details.

import os
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class MyWidget(QWidget):
    def __init__(self, parent=None):
        super(MyWidget, self).__init__(parent)
        self.setAcceptDrops(True)
        self.setMouseTracking(True)
        self.topbox = QVBoxLayout()
        self.title = QLabel('custom widget')
        self.topbox.addWidget(self.title)

        self.bodybox = QGridLayout()

        self.topbox.addLayout(self.bodybox)

        self.setLayout(self.topbox)
        self.mouse_position = QPoint()

        self.current_rows = 0
        self.current_columns = 0
        self.current_width = 0
        self.current_height = 0

    def dragEnterEvent(self, e):
        if e.mimeData().hasFormat('text/plain'):
            e.accept()
            self.current_columns = self.bodybox.columnCount()
            self.current_rows = self.bodybox.rowCount()
            self.current_height = self.height()
            self.current_width = self.width()

        else:
            e.ignore()

    def dropEvent(self, e):
        #self.setText(e.mimeData().text())
        #print(self.bodybox.rowCount())
        #print(self.height(),',',self.width())

        #self.bodybox.addWidget(QPushButton(e.mimeData().text()), self.bodybox.rowCount(), 0)
        position = self.get_nearest_position(e.pos())
        self.bodybox.addWidget(QPushButton(e.mimeData().text()), position[0], position[1])

    def mouseMoveEvent(self, event):
        self.mouse_position = event.pos()
        print(event.pos())

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

        myWidget.bodybox.addWidget(QPushButton('0,0'), 0, 0)
        myWidget.bodybox.addWidget(QPushButton('0,1'), 0, 1)
        myWidget.bodybox.addWidget(QPushButton('1,0'), 1, 0)
        myWidget.bodybox.addWidget(QPushButton('1,1'), 1, 1)


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

