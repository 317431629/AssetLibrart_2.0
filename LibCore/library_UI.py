# _ * _ coding: utf-8 _ * _ #
# @Time         :2020/7/25 15:24
# @FileName     :library_UI.py
# @Author       :LiuYang

import dayu_widgets as dy
import os
from LibPackages import package
from LibPackages import File
from LibWidget import info_widget
from LibWidget import listview
from LibWidget import fileview
from LibWidget.screen.screen_shot_widget import ScreenShot
from LibWidget import export_assets_widget
from LibWidget import assets_introduction
from LibWidget import toolBar
from LibWidget import tag_widget
from LibWidget import menu
from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui

reload(info_widget)
reload(listview)
reload(fileview)
reload(export_assets_widget)
reload(assets_introduction)
reload(toolBar)
reload(File)
reload(tag_widget)
reload(menu)

class LibraryUI(QtWidgets.QMainWindow):
    def __init__(self):
        """
        UI界面
        """
        super(LibraryUI, self).__init__()
        self.config_file = File.File(package.get("LibData/library_config.yaml"))
        self.config = self.config_file.read_data_from_file()

        self.setWindowTitle("Library Tool")
        self.setGeometry(150, 50, 1600, 900)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        self.iconPath = package.get("LibIcon")
        self._root_path = None
        self.reset_library()
        self.mainWidget = QtWidgets.QWidget(self)
        self.mainWidget.setGeometry(0, 0, 1600, 900)
        self.mainLayout = QtWidgets.QVBoxLayout(self.mainWidget)

        # menu 模块
        self.menuLayout = QtWidgets.QHBoxLayout()

        self.avatar = dy.MAvatar()
        self.loginButton = LoginAvatar(self.iconPath)
        self.inforButton = InfoAvatar(self.iconPath)

        self.projectCombobox = dy.MComboBox()
        self.projectCombobox.setMaximumWidth(100)

        project_data = File.File(package.get("LibData/Project_data.yaml")).read_data_from_file()
        project_menu = dy.MMenu()
        project_menu.set_data(project_data)
        self.projectCombobox.set_menu(project_menu)

        self.hideButton = dy.MPushButton("", dy.qt.MIcon('minus_line.svg', '#ddd')).small()
        self.hideButton.setFlat(True)
        self.closeButton = dy.MPushButton("", dy.qt.MIcon('close_line.svg', '#ddd')).small()
        self.closeButton.setFlat(True)
        self.uploadButotn = dy.MPushButton("", dy.qt.MIcon('cloud_line.svg', '#ddd')).small().primary()
        self.uploadButotn.setFlat(True)

        self.SpliterLayout = QtWidgets.QHBoxLayout()

        self.toolbar = toolBar.ToolBar()

        self.mainSplitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        self.mainSplitter.setStyleSheet("width:0px")

        self.listFrame = QtWidgets.QFrame()
        self.listLayout = QtWidgets.QVBoxLayout(self.listFrame)

        self.searchLayout = QtWidgets.QHBoxLayout()
        self.listSearchLine = dy.MLineEdit().search()
        self.tagButton = dy.MPushButton("", QtGui.QPixmap(package.get("LibIcon/tag.png"))).warning()
        self.tagButton.setMinimumWidth(60)

        self.ListScrollArea = QtWidgets.QScrollArea()
        self.ListScrollArea.setWidgetResizable(True)

        self.CardWidget = QtWidgets.QWidget()
        self.CardLayout = dy.MFlowLayout(self.CardWidget)
        self.ListScrollArea.setWidget(self.CardWidget)

        # export view 导出模块
        self.exportFrame = QtWidgets.QFrame()
        self.exportFrame.hide()
        self.exportFrame.setMinimumWidth(500)
        self.exportFrame.setMaximumWidth(500)

        self.exportLayout = QtWidgets.QVBoxLayout(self.exportFrame)
        self.exportLayout.setContentsMargins(0, 0, 0, 0)

        self.screenShot = ScreenShot("请拖拽一个\n预览文件")
        self.screenShot.setMaximumHeight(350)

        self.dragLayout = QtWidgets.QHBoxLayout()
        self.zbDragButton = dy.MDragFileButton()
        self.zbDragButton.setFixedSize(120, 120)
        self.zbDragButton.set_dayu_svg(package.get("LibIcon/Zbrush.png"))
        self.zbDragButton.setText("")
        self.zbDragButton.setIconSize(QtCore.QSize(1080, 1080))
        self.zbDragButton.set_dayu_filters([".ZBR", ".ZTL", ".ZPR"])
        self.spDragButton = dy.MDragFileButton("")
        self.spDragButton.setFixedSize(120, 120)
        self.spDragButton.set_dayu_filters([".spp"])
        self.spDragButton.set_dayu_svg(package.get("LibIcon/substance_Icon.png"))

        self.textureDragButton = dy.MDragFolderButton()
        self.textureDragButton.setText("")
        self.textureDragButton.setFixedSize(120, 120)

        self.informationWidget = export_assets_widget.PublishInformation()

        self.updateLayout = QtWidgets.QHBoxLayout()
        self.updateButton = dy.MPushButton('Upload To Library', dy.qt.MIcon('cloud_line.svg', '#ddd')).warning().large()

        self.introdiction = assets_introduction.Introduction(self.root_path)
        self.introdiction.setMinimumWidth(500)
        self.introdiction.setMaximumWidth(500)
        self.introdiction.hide()

        self.tagFrame = tag_widget.TagWidget()
        self.tagFrame.setMinimumWidth(500)
        self.tagFrame.setMaximumWidth(500)
        self.tagFrame.hide()

        self.info_window = info_widget.InfoUI()

        self.set_theme()
        self.setup_ui()
        self.connect_ui()

    def setup_ui(self):
        self.mainLayout.addLayout(self.menuLayout)
        self.mainLayout.addLayout(self.SpliterLayout)

        self.SpliterLayout.addWidget(self.toolbar)

        self.SpliterLayout.addWidget(self.mainSplitter)

        self.menuLayout.addWidget(self.avatar)
        self.menuLayout.addWidget(self.loginButton)
        self.menuLayout.addWidget(self.inforButton)
        self.menuLayout.addStretch()
        self.menuLayout.addWidget(self.projectCombobox)
        self.menuLayout.addWidget(self.hideButton)
        self.menuLayout.addWidget(self.closeButton)
        self.menuLayout.addWidget(self.uploadButotn)

        self.listLayout.addLayout(self.searchLayout)
        self.listLayout.addWidget(self.ListScrollArea)

        self.searchLayout.addWidget(self.listSearchLine)
        self.searchLayout.addWidget(self.tagButton)

        self.exportLayout.addWidget(self.screenShot)
        self.exportLayout.addWidget(dy.MDivider(""))
        self.exportLayout.addLayout(self.dragLayout)
        self.exportLayout.addWidget(dy.MDivider(""))
        self.exportLayout.addWidget(self.informationWidget)
        self.exportLayout.addWidget(dy.MLabel(""))
        self.exportLayout.addLayout(self.updateLayout)
        self.exportLayout.addWidget(dy.MLabel(""))

        self.dragLayout.addWidget(self.zbDragButton)
        self.dragLayout.addWidget(self.spDragButton)
        self.dragLayout.addWidget(self.textureDragButton)

        self.updateLayout.addStretch()
        self.updateLayout.addWidget(self.updateButton)
        self.updateLayout.addStretch()

        self.mainSplitter.addWidget(self.listFrame)
        self.mainSplitter.addWidget(self.exportFrame)
        self.mainSplitter.addWidget(self.introdiction)
        self.mainSplitter.addWidget(self.tagFrame)

    def connect_ui(self):
        """
        链接信号和槽
        :return:
        """
        self.closeButton.clicked.connect(self.close)
        self.uploadButotn.clicked.connect(self.open_export_win)
        self.inforButton.left_chilcked.connect(self.info_window.show)
        self.tagButton.clicked.connect(self.tag_frame_show_hide)

    @property
    def root_path(self):
        """
        资产库根路径
        :return:
        """
        return self._root_path

    @root_path.setter
    def root_path(self, path):
        self._root_path = path

    def reset_library(self):
        self.root_path = self.config["ROOT_PATH"]

    def set_theme(self):
        """
        配置sty
        :return:
        """
        theme = dy.MTheme(theme="dark")
        theme.apply(self)

    def tag_frame_show_hide(self):
        self.exportFrame.hide()
        self.introdiction.hide()

        if self.tagFrame.isHidden():
            self.tagFrame.show()
        else:
            self.tagFrame.hide()

    # 实现拖拽移动窗口
    def mousePressEvent(self, event):
        super(LibraryUI, self).mousePressEvent(event)
        if event.button() == QtCore.Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.move(event.globalPos() - self.dragPosition)
            event.accept()

    def open_export_win(self):
        """
        打开导出窗口
        :return:
        """
        self.introdiction.hide()
        self.tagFrame.hide()
        if self.exportFrame.isHidden():
            self.exportFrame.show()
        else:
            self.exportFrame.hide()

    def open_introdiction_win(self):
        """
        打开右侧资产信息窗口
        :return:
        """
        self.exportFrame.hide()
        self.tagFrame.hide()
        if self.introdiction.isHidden():
            self.introdiction.show()


class LoginAvatar(dy.MAvatar):
    def __init__(self, icon_path=None):
        super(LoginAvatar, self).__init__()
        self.menu = menu.Menu(self)
        menu_data = {"Login": package.get("LibIcon/login.svg"),
                     "Logout": package.get("LibIcon/logout.svg"),
                     "Set Root Path": package.get("LibIcon/tree_view.svg"),
                     "导入资产": package.get("LibIcon/import.svg"),
                     }
        self.menu.add_menu(menu_data)

        self.iconPath = icon_path
        self.set_dayu_image(QtGui.QPixmap(package.get("LibIcon/shezhi_mian.png")))

    def mousePressEvent(self, event):
        super(LoginAvatar, self).mousePressEvent(event)
        self.set_dayu_image(QtGui.QPixmap(package.get("LibIcon/shezhi_mian.png")))
        if event.button() == QtCore.Qt.LeftButton:
            self.menu.close()
            self.menu.show()
            self.menu.move(QtGui.QCursor.pos())
        elif event.button() == QtCore.Qt.RightButton:
            self.menu.close()

    def mouseReleaseEvent(self, event):
        super(LoginAvatar, self).mouseReleaseEvent(event)
        self.set_dayu_image(QtGui.QPixmap(package.get("LibIcon/shezhi.png")))

    def login(self):
        """
        登入
        :return:
        """
        print "登入"

    def logout(self):
        """
        登出
        :return:
        """
        print "登出"

    def set_root_path(self):
        """
        设置资产库路径
        :return:
        """
        pass

    def import_assets(self):
        pass

class InfoAvatar(dy.MAvatar):
    left_chilcked = QtCore.Signal()
    def __init__(self, icon_path=None):
        super(InfoAvatar, self).__init__()
        self.set_dayu_image(QtGui.QPixmap(package.get("LibIcon/info_fill.svg")))

    def mousePressEvent(self, event):
        super(InfoAvatar, self).mousePressEvent(event)
        self.left_chilcked.emit()


class MyMenu(QtWidgets.QWidget):
    login_signal = QtCore.Signal()
    logout_signal = QtCore.Signal()
    set_root_signal = QtCore.Signal()

    def __init__(self, parent):
        super(MyMenu, self).__init__()
        self.parent = parent
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.setMaximumWidth(110)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        self.loginButton = dy.MPushButton("Login",
                                               icon=dy.qt.MIcon(package.get("LibIcon/login.svg"))).tiny()
        self.loginButton.setMaximumWidth(100)
        self.logoutButton = dy.MPushButton("Logout",
                                             icon=dy.qt.MIcon(package.get("LibIcon/logout.png"))).tiny()
        self.logoutButton.setMaximumWidth(100)
        self.setRootPath = dy.MPushButton("Set Root Path",
                                          icon=dy.qt.MIcon(package.get("LibIcon/tree_view.svg"))).tiny()
        self.setRootPath.setMaximumWidth(100)

        self.importButton = dy.MPushButton("导入资产",
                                           icon=dy.qt.MIcon(package.get("LibIcon/import.jpg"))).tiny()

        self.importButton.setMaximumWidth(100)
        self.set_theme()
        self.setup_ui()
        self.connect_ui()

    def setup_ui(self):
        self.mainLayout.addWidget(self.loginButton)
        self.mainLayout.addWidget(self.logoutButton)
        self.mainLayout.addWidget(dy.MDivider(""))
        self.mainLayout.addWidget(self.setRootPath)
        self.mainLayout.addWidget(self.importButton)

    def connect_ui(self):
        self.loginButton.clicked.connect(self.login)
        self.logoutButton.clicked.connect(self.logout)
        self.setRootPath.clicked.connect(self.set_root_path)

    def login(self):
        self.login_signal.emit()

    def logout(self):
        self.logout_signal.emit()

    def set_root_path(self):
        self.set_root_signal.emit()

    def set_theme(self):
        theme = dy.MTheme(theme="dark")
        theme.apply(self)


if __name__ == '__main__':
    Library = LibraryUI()
    Library.show()
