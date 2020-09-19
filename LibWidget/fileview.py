# _ * _ coding: utf-8 _ * _ #
# @Time         :2020/7/25 15:24
# @FileName     :library_UI.py
# @Author       :LiuYang
import os

from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from dayu_widgets import MTreeView
from LibWidget import filemodel

reload(filemodel)


class FolderWidget(QTreeView):

    itemSelectionChanged = Signal(list)
    leftPressed = Signal()

    def __init__(self, super_user=True, parent=None):
        super(FolderWidget, self).__init__(parent)
        self.setFocusPolicy(Qt.NoFocus)  # 设置起始状态没有focus的元素
        self.set_icon_size(2)
        self.super_user = super_user
        self.path = None

        # 设置mod
        self._source_model = filemodel.FileSystemModel(self)

        proxy_model = filemodel.SortFilterProxyModel(self)
        proxy_model.setSourceModel(self._source_model)
        proxy_model.sort(0)

        self.setModel(proxy_model)
        self.setHeaderHidden(True)
        # self.setAnimated(True)

        self.setSelectionMode(QTreeWidget.ExtendedSelection)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)

        selection_model = self.selectionModel()
        selection_model.selectionChanged.connect(self.on_selection_changed)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

        self.set_style_sheet()
        # self.create_actions()

    def set_root_path(self, path):
        """
        :param path: str
        :return:
        """
        self.path = path
        self.model().sourceModel().setRootPath(path)

        index = self.index_from_path(path)
        self.setRootIndex(index)

    def on_selection_changed(self, selected, diselected):
        """
        :param selected: QModuleIndex
        :param diselected: QModuleIndex
        :return:
        """
        paths = self.selected_paths()
        self.itemSelectionChanged.emit(paths)

    def path_from_index(self, index):
        """
        :param index: QModuleIndex
        :return:
        """
        index = self.model().mapToSource(index)
        return self.model().sourceModel().filePath(index)

    def index_from_path(self, path):
        """
        :param path: a location <str>
        :return:
        """
        index = self.model().sourceModel().index(path)
        return self.model().mapFromSource(index)

    def selected_paths(self):
        """
        get all the selected paths
        :return: list
        """
        paths = list()
        for index in self.selectionModel().selectedIndexes():
            path = self.path_from_index(index)
            paths.append(path)
        return paths

    def create_actions(self):
        """
        create actions
        :return:
        """
        pass
        # self.delete_action = QAction(QPixmap(os.path.join(self.iconPath, "delete.png")), "Delete", self,
        #                              triggered=self.delete_folder)

        # self.show_in_folder_action = QAction(QPixmap(os.path.join(self.iconPath, "show_in_folder.png")), "Show in Folder", self,
        #                                      triggered=self.open_selected_folders)

        # self.rename_action = QAction(QPixmap(os.path.join(self.iconPath, "rename.png")), "Rename", self,
        #                              triggered=self.rename)

        # self.add_folder_action = QAction(QPixmap(os.path.join(self.iconPath, "add_folder.png")), "Add Folder", self,
        #                                  triggered=self.add_folder)

        # self.addAction(self.add_folder_action)

        # self.add_category_action = QAction(QPixmap(os.path.join(self.iconPath, "category.png")), "Add Category", self,
        #                                    triggered=self.add_category)

    def create_edit_menu(self):
        """
        create popup menu when right clicked
        :return:
        """
        selected_paths = self.selected_paths()
        menu = QMenu(self)
        # if selected_paths:
        #     if len(selected_paths) == 1:
        #         menu.addAction(self.show_in_folder_action)
        #         if self.super_user:
        #             menu.addAction(self.rename_action)
        #             menu.addAction(self.add_folder_action)
        #     if self.super_user:
        #         menu.addSeparator()
        #         menu.addAction(self.delete_action)
        # else:
        #     if self.super_user:
        #         menu.addAction(self.add_category_action)
        #         menu.addAction(self.show_in_folder_action)
        return menu

    def show_context_menu(self, *args):
        """
        show the popup menu
        :return:
        """
        menu = self.create_edit_menu()
        menu.exec_(QCursor.pos())

    def set_ignore_filter(self, ignore_filter):
        """
        :param ignore_filter: list
        :return:
        """
        self.model().sourceModel().set_ignore_filter(ignore_filter)

    def set_icon_size(self, dpi):
        """
        :param dpi: int
        :return:
        """
        size = 24 * dpi
        self.setIndentation(15 * dpi)
        self.setMinimumWidth(35 * dpi)
        self.setIconSize(QSize(size, size))

    def rename(self):
        """
        rename selected path
        :return:
        """
        paths = self.selected_paths()
        if paths:
            print paths
            # p = Path(paths[0])
            p = paths
            new_name, ok = QInputDialog.getText(self, "Rename", "New Name", text=p.basename())
            if new_name and ok:
                new_path = "{0}/{1}".format(p.dirname(), new_name)
                p.rename(new_path)

    # def open_selected_folders(self):
    #     """
    #     open the selected folder
    #     :return:
    #     """
    #     paths = self.selected_paths()
    #     if paths:
    #         utils.open_location(paths[0])
    #     else:
    #         utils.open_location(self.path)
    #
    # def add_folder(self):
    #     """
    #     add a child folder of selected
    #     :return:
    #     """
    #     paths = self.selected_paths()
    #     if paths:
    #         path = paths[0]
    #         name, ok = QInputDialog.getText(self, "Add Folder", "Folder Name")
    #         if name and ok:
    #             if re.findall("[ |\*]+", name):
    #                 MessageBox.warning(self, "warning", "Can't include space and \"*\".")
    #                 return
    #             new_folder = "{0}/{1}".format(path, name)
    #             Path(new_folder).create()
    #             self.set_root_path(self.path)
    #             index = self.index_from_path(path)
    #             self.expand(index)
    #
    # def delete_folder(self):
    #     """
    #     delete selected folders
    #     :return:
    #     """
    #     text, ok = QInputDialog.getText(self, "Delete", "Please input \"delete\" to delete.")
    #     if ok and text == "delete":
    #         paths = self.selected_paths()
    #         for path in paths:
    #             Path(path).remove()
    # #
    # def add_category(self):
    #     if self.super_user:
    #         root_path = self.model().sourceModel().rootPath()
    #
    #         name, ok = QInputDialog.getText(self, "Add Category", "Category Name")
    #         if name and ok:
    #             if re.findall("[ |\*]+", name):
    #                 MessageBox.warning(self, "warning", "Can't include space and \"*\".")
    #                 return
    #             path = "{0}/{1}".format(root_path, name)
    #             Path(path).create()
    #     else:
    #         MessageBox.warning(self, "Warning", u"您不是超级用户，没有权限执行此操作。")
    #
    # def mousePressEvent(self, event):
    #     focused_widget = QApplication.focusWidget()
    #     if isinstance(focused_widget, QLineEdit):
    #         focused_widget.clearFocus()
    #     if event.type() == QEvent.MouseButtonPress:
    #         if event.button() == Qt.LeftButton:
    #             self.leftPressed.emit()
    #     super(FolderWidget, self).mousePressEvent(event)

    def set_style_sheet(self):
        self.setStyleSheet("QTreeView::branch:has-children:!has-siblings:closed, "
                           "QTreeView::branch:closed:has-children:has-siblings{border-image: none; image: url('D:/ToolBox_Project/library/LibIcon/vline.png');}"
                           "QTreeView::branch:open:has-children:!has-siblings,"
                           "QTreeView::branch:open:has-children:has-siblings{border-image: none; image: url('D:/ToolBox_Project/library/LibIcon/vline.png');}"
                           )

