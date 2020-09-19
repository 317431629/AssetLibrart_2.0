# _ * _ coding: utf-8 _ * _ #
# @Time         :2020/7/25 15:24
# @FileName     :library_UI.py
# @Author       :LiuYang

import dayu_widgets as dy
from PySide2 import QtWidgets
from PySide2 import QtCore


class InfoUI(QtWidgets.QWidget):
    def __init__(self):
        super(InfoUI, self).__init__()
        self.setWindowTitle("About")
        self.setGeometry(800, 300, 500, 400)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        self.mainLayout = QtWidgets.QVBoxLayout(self)

        self.checkLayout = QtWidgets.QHBoxLayout()
        self.checkButton = dy.MPushButton("ok").primary()
        self.checkButton.setMinimumWidth(60)

        self.setup_ui()
        self.set_theme()
        self.connect_ui()

    def setup_ui(self):
        self.mainLayout.addStretch()
        self.mainLayout.addLayout(self.checkLayout)

        self.checkLayout.addStretch()
        self.checkLayout.addWidget(self.checkButton)

    def connect_ui(self):
        self.checkButton.clicked.connect(self.close)

    def set_theme(self):
        theme = dy.MTheme(theme="dark")
        theme.apply(self)


if __name__ == '__main__':
    # app = QtWidgets.QApplication(sys.argv)
    Library = InfoUI()
    Library.show()
    # sys.exit(app.exec_())
