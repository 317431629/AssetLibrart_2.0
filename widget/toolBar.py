# _ * _ coding: utf-8 _ * _ #
# @Time         :2020/7/25 15:24
# @FileName     :ToolBar.py
# @Author       :LiuYang

import dayu_widgets as dy
import time
import functools
from Libs import package
from Libs import File
from PySide2 import QtWidgets
from PySide2 import QtGui
from PySide2 import QtCore


class ToolBar(QtWidgets.QWidget):
    enter_signal = QtCore.Signal()
    leave_signal = QtCore.Signal()

    def __init__(self):
        super(ToolBar, self).__init__()

        self.mainLayout = QtWidgets.QHBoxLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.setMaximumWidth(65)

        icon_data = File.File(package.get("Data/library_config.yaml")).read_data_from_file()["CATEGORY"]

        self.toolbar = ToPBar(icon_data)
        self.categoryBar = CategoryWidget()
        self.categoryBar.hide()

        self._hold = False
        self.setup_ui()
        self.connect_ui()

    def setup_ui(self):
        self.mainLayout.addWidget(self.toolbar)
        self.mainLayout.addWidget(self.categoryBar)
        self.mainLayout.addStretch()

    def enterEvent(self, event):
        """
        鼠标进入事件
        :return:
        """
        if not self._hold:
            self.categoryBar.setFixedHeight(self.height())
            self.setMinimumWidth(220)
            self.setMaximumWidth(220)
            self.categoryBar.show()

    def leaveEvent(self, event):
        """
        鼠标离开事件
        :param event:
        :return:
        """
        if not self._hold:
            self.categoryBar.hide()
            self.setMinimumWidth(65)
            self.setMaximumWidth(65)

    def mousePressEvent(self, event):
        super(ToolBar, self).mousePressEvent(event)
        if event.button() == QtCore.Qt.RightButton:
            menu = QtWidgets.QMenu(self)
            action = QtWidgets.QAction("Allow stay here", self)
            action.triggered.connect(self.set_holder)
            menu.addAction(action)
            menu.move(QtGui.QCursor.pos())
            menu.show()

    def set_holder(self):
        if not self._hold:
            self._hold = True
        else:
            self._hold = False

    def connect_ui(self):
        self.toolbar.icon_signal.connect(self.categoryBar.setup_ui)


class ToPBar(QtWidgets.QWidget):
    icon_signal = QtCore.Signal(dict)
    tag_signal = QtCore.Signal(str)

    def __init__(self, tool_data):
        super(ToPBar, self).__init__()
        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("ToolBar")
        self.tool_button_data = tool_data
        self.set_tool_button()
        # self.setStyleSheet("QWidget#ToolBar{border:0px; border-radius: 0px; background-color: rgb(40, 40, 40)}")
        self.mainLayout.addStretch()

    def set_tool_button(self):
        """
        设置图标
        :return:
        """
        for tool_data in self.tool_button_data:
            top_name = tool_data["name"]
            tool_button = TopLabel(tool_data)
            self.mainLayout.addWidget(tool_button)
            tool_button.left_signal.connect(self.icon_emit)

    def icon_emit(self, data):
        self.icon_signal.emit(data)
        self.tag_signal.emit(data["code"])


class TopLabel(dy.MLabel):
    left_signal = QtCore.Signal(dict)

    def __init__(self, label_data):
        super(TopLabel, self).__init__(text=label_data["name"])
        self.tool_data = label_data
        self.cur_code = label_data["code"]
        self.strong()
        self.setObjectName(label_data['code'])
        self.set_theme()

    def mousePressEvent(self, event):
        self.left_signal.emit(self.tool_data)

    def enterEvent(self, event):
        """
        鼠标进入事件
        :return:
        """
        pass

    def leaveEvent(self, event):
        pass

    def set_theme(self):
        theme = dy.MTheme(theme="dark")
        theme.apply(self)


class CategoryWidget(QtWidgets.QWidget):
    left_signal = QtCore.Signal(str)

    def __init__(self):
        super(CategoryWidget, self).__init__()
        self.setObjectName("CategoryWidget")
        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        self.setStyleSheet("QWidget#CategoryWidget{border:0px; border-radius: 0px; background-color: rgb(50, 50, 50)}")
        # self.setFixedWidth(350)
        self.top_category = None
        self.categoryLayout = QtWidgets.QVBoxLayout()

        self.mainLayout.addWidget(dy.MLabel("Category").h3().strong())
        self.mainLayout.addLayout(self.categoryLayout)
        self.mainLayout.addStretch()

    def setup_ui(self, data):
        self.clean_children(self.categoryLayout)

        for category in data["category"]:
            top_category = category["parent"]
            name = category["name"]
            code = category["code"]
            next_category = category["category"]
            sec_label = MyLabel(category)

            thirdWidget = QtWidgets.QWidget()
            thirdLayout = QtWidgets.QVBoxLayout(thirdWidget)
            thirdLayout.setContentsMargins(0, 0, 0, 0)
            thirdWidget.hide()

            self.categoryLayout.addWidget(sec_label)
            self.categoryLayout.addWidget(thirdWidget)

            sec_label.nameLabel.left_signal.connect(functools.partial(self.emit_sec_signal, next_category, thirdWidget))

    def emit_sec_signal(self,next_category, thirdWidget, path):
        """
        :param next_category:
        :param thirdWidget:
        :param data:
        :return: path [str] eg :"ch/man/woman"
        """
        if next_category:
            self.clean_children(thirdWidget.children()[0])
            for category in next_category:
                third_label = MyLabel(category)
                third_label.nameLabel.left_signal.connect(self.emit_third_signal)
                thirdWidget.children()[0].addWidget(third_label)

                if thirdWidget.isHidden():
                    thirdWidget.show()
                else:
                    thirdWidget.hide()
        self.left_signal.emit(path)

    def emit_third_signal(self, path):

        self.left_signal.emit(path)

    @staticmethod
    def clean_children(widget, widget_filter=[]):
        if not widget.count():
            return
        for i in range(widget.count()):
            if widget.itemAt(i).widget() in widget_filter:
                pass
            else:
                try:
                    widget.itemAt(i).widget().deleteLater()
                except AttributeError:
                    pass


class MyLabel(QtWidgets.QWidget):
    def __init__(self, category):
        super(MyLabel, self).__init__()
        self.cur_code = category["parent"]
        self.space_label = " "
        if "category" not in category.keys():
            self.space_label = "     "

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.nameLabel = Label(category["name"]).strong()
        self.nameLabel.setObjectName("{0}/{1}".format(category["parent"], category["code"]))
        self.nameLabel.setStyleSheet("color: rgb(120, 120, 120);")
        self.spaceLabel = QtWidgets.QLabel(self.space_label)
        self.layout.addWidget(self.spaceLabel)
        self.layout.addWidget(self.nameLabel)
        self.layout.addStretch()

    def enterEvent(self, event):
        """
        鼠标进入事件
        :return:
        """
        time.sleep(0.1)
        self.nameLabel.setStyleSheet("color: rgb(250, 250, 250);")

    def leaveEvent(self, event):
        """
        鼠标离开事件
        :param event:
        :return:
        """
        time.sleep(0.1)
        self.nameLabel.setStyleSheet("color: rgb(120, 120, 120);")


class Label(dy.MLabel):
    left_signal = QtCore.Signal(str)
    def __init__(self,text):
        super(Label, self).__init__(text=text, parent=None, flags=0)

    def mousePressEvent(self, event):
        """
        鼠标点击事件
        :param event:
        :return:
        """
        if event.button() == QtCore.Qt.LeftButton:
            self.left_signal.emit(self.objectName())

if __name__ == '__main__':
    tool_bal = ToolBar()
    tool_bal.show()
