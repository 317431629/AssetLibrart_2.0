# _ * _ coding: utf-8 _ * _ #
# @Time         :2020/7/25 15:24
# @FileName     :library_UI.py
# @Author       :LiuYang

import dayu_widgets as dy
from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui


class SetLibraryUI(QtWidgets.QWidget):
    def __init__(self):
        super(SetLibraryUI, self).__init__()
        self.setWindowTitle("配置Library")
        self.MainLayout = QtWidgets.QVBoxLayout(self)

        # Root Path 设置
        self.RootPathLayout = QtWidgets.QHBoxLayout()
        self.RootPathLabel = dy.MLabel("Root Path:").strong()
        self.RootPathLine = dy.MLineEdit()
        self.RootPathButton = dy.MPushButton("打开")

        # 设置type
        self.CategoryLayout = QtWidgets.QVBoxLayout()

        self.CHLayout = QtWidgets.QVBoxLayout()
        self.CHLabel = dy.MLabel("角色").strong().h2()

        self.PropLayout = QtWidgets.QVBoxLayout()
        self.PropLabel = dy.MLabel("道具").strong().h2()

        self.SCLayout = QtWidgets.QVBoxLayout()
        self.SCLabel = dy.MLabel("场景").strong().h2()

        self.setup_ui()

    def setup_ui(self):
        self.MainLayout.addLayout(self.RootPathLayout)
        self.MainLayout.addWidget(dy.MDivider(""))
        self.MainLayout.addLayout(self.CategoryLayout)

        self.RootPathLayout.addWidget(self.RootPathLabel)
        self.RootPathLayout.addWidget(self.RootPathLine)
        self.RootPathLayout.addWidget(self.RootPathButton)

        self.CategoryLayout.addLayout(self.CHLayout)
        self.CategoryLayout.addLayout(self.PropLayout)
        self.CategoryLayout.addLayout(self.SCLayout)

        self.CHLayout.addWidget(self.CHLabel)
        self.PropLayout.addWidget(self.PropLabel)
        self.SCLayout.addWidget(self.SCLabel)


if __name__ == '__main__':
    theme = dy.MTheme(theme="dark")
    window = SetLibraryUI()
    theme.apply(window)
    window.show()
