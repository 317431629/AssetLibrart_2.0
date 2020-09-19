# _ * _ coding: utf-8 _ * _ #
# @Time         :2020/7/25 15:24
# @FileName     :library_UI.py
# @Author       :LiuYang

from PySide2 import QtWidgets


class ListView(QtWidgets.QScrollArea):
    def __init__(self):
        super(ListView, self).__init__()
        self.list_view.setViewMode(QtWidgets.QListView.IconMode)
        self.list_view.setMovement(QtWidgets.QListView.Static)
        self.module = None

    def set_model(self, module):
        self.module = module
