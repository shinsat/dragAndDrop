from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys


def split_widget(current_wgt, new_wgt, spltr):
    splitter = QSplitter(Qt.Vertical) if spltr == 'V' else QSplitter(Qt.Horizontal)

    splitter.addWidget(current_wgt)
    splitter.addWidget(new_wgt)

    return new_wgt
    return splitter
