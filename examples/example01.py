import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 drag and drop - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 320
        self.height = 60
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        editBox = QLineEdit('Drag this', self)
        editBox.setDragEnabled(True)
        editBox.move(10, 10)
        editBox.resize(100, 32)

        button = CustomLabel('Drop here.', self)
        button.move(130, 15)

        self.splitterH = QSplitter(Qt.Horizontal)
        self.splitterH.addWidget(editBox)
        self.splitterH.addWidget(button)
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.splitterH)
        self.setLayout(self.layout)
        self.splitterH.setAcceptDrops(True)

        self.show()

    @pyqtSlot()
    def on_click(self):
        print('PyQt5 button click')


class CustomLabel(QLabel):
    def __init__(self, title, parent):
        super().__init__(title, parent)
        self.setAcceptDrops(True)
        self.parent = parent

    def dragEnterEvent(self, e):
        if e.mimeData().hasFormat('text/plain'):
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        self.setText(e.mimeData().text())
        newBtn = QPushButton(e.mimeData().text())
        self.parent.splitterH.insertWidget(0, newBtn)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())