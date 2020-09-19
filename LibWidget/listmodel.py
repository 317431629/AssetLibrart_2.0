# _ * _ coding: utf-8 _ * _ #
# @Time         :2020/7/25 15:24
# @FileName     :library_UI.py
# @Author       :LiuYang
import os
import dayu_widgets as dy
from PySide2 import QtGui
from PySide2.QtCore import Signal
from pprint import pprint


class ListModel(object):
    def __init__(self):
        self.module_item = None

    def set_item(self, items):
        self.module_item = items


class Card(dy.MMeta):
    double_click_signal = Signal()

    def __init__(self, parent, data):
        """

        :param parent: LibraryTool
        :param data: 单个实例数据
        """
        self.parent = parent
        self.assets_data = data
        self.project = self.get_project()
        self.menu = None

        super(Card, self).__init__()

    def get_project(self):
        """
        获取Project 标签
        :return:
        """
        try:
            project = File.File(os.path.join(self.parent.root_path,
                                             "{}/project.yaml".format(os.path.split(
                                                 self.assets_data["TexturePath"])[0])
                                             )
                                ).read_data_from_file()
        except IOError:
            project = {"Project": ""}
        return project["Project"]

    def mouseDoubleClickEvent(self, event):
        super(Card, self).mouseDoubleClickEvent(event)
        self.parent.introdiction.hide()

    def mousePressEvent(self, event):
        super(Card, self).mousePressEvent(event)
        self.menu = CardMenu(self)
        if event.button() == QtCore.Qt.LeftButton:
            if QtWidgets.QApplication.keyboardModifiers() == QtCore.Qt.ShiftModifier:
                if self not in self.parent.select_items:
                    self.parent.select_items.append(self)
                    self.setStyleSheet("background-color:rgb(100,150,200)")
                else:
                    self.parent.select_items.remove(self)
                    self.setStyleSheet("background-color:rgb(50,50,50)")
            else:
                self.parent.introdiction.set_data(self.assets_data)
                self.parent.introdiction.assetsInformation.add_texture_widget(self.assets_data["TexturePath"])
                self.parent.open_introdiction_win()

        elif event.button() == QtCore.Qt.RightButton:
            self.menu.close()
            if self.parent.select_items:
                self.menu.show_button(True)
            else:
                self.menu.show_button()

            self.menu.setProjectButton.clicked.connect(partial(self.set_project, self.parent.select_items))
            self.menu.show()
            self.menu.move(QtGui.QCursor.pos())

            for item in self.parent.select_items:
                item.setStyleSheet("background-color:rgb(50,50,50)")

        return self.menu

    def set_project(self, item_list):
        items = File.File(package.get("LibData/project_data.yaml").replace("\\", "/")).read_data_from_file()
        project_data = QtWidgets.QInputDialog().getItem(self, "Get item", "Project:", items, 0, False)[0]
        for item in item_list:
            item.menu.set_project(project_data)

