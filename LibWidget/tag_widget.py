# _ * _ coding: utf-8 _ * _ #
# @Time         :2020/7/25 15:24
# @FileName     :library_UI.py
# @Author       :LiuYang

import dayu_widgets as dy
from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui
from LibPackages import package
from LibPackages import File
from random import random


class TagWidget(QtWidgets.QWidget):
    change_signal = QtCore.Signal(list)

    def __init__(self):
        super(TagWidget, self).__init__()
        self.tag_data = File.File(package.get("LibData/tag_data.yaml")).read_data_from_file()
        self.MainLayout = QtWidgets.QVBoxLayout(self)
        self.MainLayout.setContentsMargins(0, 0, 0, 0)
        self.split = QtWidgets.QSplitter()
        self.split.setStyleSheet("width: 0px;")
        self.split.setOrientation(QtCore.Qt.Vertical)

        self.viewWidget = QtWidgets.QWidget()
        self.viewWidget.setMaximumHeight(self.split.height()/3)
        self.viewLayout = dy.MFlowLayout(self.viewWidget)
        self.viewLayout.setContentsMargins(0, 0, 0, 0)

        self.tagScrollArea = QtWidgets.QScrollArea()
        self.tagScrollArea.setStyleSheet("width:0px;")
        self.tagScrollArea.setWidgetResizable(True)
        self.tagWidget = QtWidgets.QWidget()
        self.tagLayout = dy.MFlowLayout(self.tagWidget)
        self.tagScrollArea.setWidget(self.tagWidget)

        self.setup_ui()

    def setup_ui(self):
        self.MainLayout.addWidget(self.split)

        self.split.addWidget(self.viewWidget)
        self.split.addWidget(self.tagScrollArea)

    @staticmethod
    def __clean_children(widget, widget_filter=[]):
        if len(widget.children()) == 1:
            return True

        for i in range(widget.children()[0].count()):
            if widget.children()[0].itemAt(i).widget() in widget_filter:
                pass
            else:
                widget.children()[0].itemAt(i).widget().deleteLater()

    def init_tag_view(self, module):
        module_tags = self.tag_data[module]
        self.__clean_children(self.tagWidget)
        self.__clean_children(self.viewWidget)
        for module_tag in module_tags:
            tag = Tag(module_tag)
            tag.left_signal.connect(self.add_tag_to_view)
            self.tagLayout.addWidget(tag)

    def add_tag_to_view(self, module_tag):
        """
        添加标签去视图
        :param module_tag:
        :return:
        """

        tag = Tag(module_tag)
        tag.left_signal.connect(self.remove_tag_from_view)

        view_object_name = [view_tag.objectName() for view_tag in self.viewWidget.children()]
        if tag.objectName() not in view_object_name:
            self.viewLayout.addWidget(tag)
        cur_tag = [self.viewLayout.itemAt(i).widget().objectName() for i in range(self.viewLayout.count())]
        self.change_signal.emit(cur_tag)

    def remove_tag_from_view(self, module_tag):
        """
        移除标签
        :return:
        """
        cur_tag = [self.viewLayout.itemAt(i).widget().objectName() for i in range(self.viewLayout.count())]
        for i in range(self.viewLayout.count()):
            if self.viewLayout.itemAt(i).widget().objectName() == module_tag:
                self.viewLayout.itemAt(i).widget().deleteLater()
                cur_tag.remove(self.viewLayout.itemAt(i).widget().objectName())

        self.change_signal.emit(cur_tag)


class Tag(QtWidgets.QWidget):
    left_signal = QtCore.Signal(str)

    def __init__(self, name):
        super(Tag, self).__init__()
        self.setObjectName(name)
        self.MainLayout = QtWidgets.QHBoxLayout(self)
        self.MainLayout.setContentsMargins(0, 0, 0, 0)
        self.setMinimumWidth(100)
        self.setMaximumWidth(100)
        self.Avatar = dy.MAvatar()
        self.Avatar.set_dayu_image(QtGui.QPixmap(package.get("LibIcon/tag_small.png")))

        self.Label = dy.MLabel(name).strong()

        self.MainLayout.addWidget(self.Avatar)
        self.MainLayout.addWidget(self.Label)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.left_signal.emit(self.objectName())


if __name__ == '__main__':
    TagWidget = TagWidget()
    theme = dy.MTheme(theme="dark")
    theme.apply(TagWidget)
    TagWidget.init_tag_view("character")

    TagWidget.show()
