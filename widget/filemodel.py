# -*- coding: utf-8 -*-
import os
from Libs import package
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *


class FileSystemModel(QFileSystemModel):
    def __init__(self, parent=None):
        super(FileSystemModel, self).__init__()
        self._parent = parent
        self.iconPath = package.get("Icon")
        self.setFilter(QDir.Dirs | QDir.NoDotAndDotDot)

    def columnCount(self, *args, **kwargs):
        return 1

    def data(self, index, role):
        if role == Qt.DecorationRole:
            if index.column() == 0:
                pix_map = QPixmap(os.path.join(self.iconPath, "close.png").replace("\\", "/"))
                if self._parent.isExpanded(self._parent.model().mapFromSource(index)):
                    pix_map = QPixmap(os.path.join(self.iconPath, "folder-open.png").replace("\\", "/"))
                scaled = pix_map.scaled(self._parent.iconSize(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                return scaled

        if role == Qt.DisplayRole:
            text = QFileSystemModel.data(self, index, role)
            return text

        if role == Qt.FontRole:
            pass

        return QFileSystemModel.data(self, index, role)

    def setData(self, index, value, role):
        print index, value, role
        column = index.column()
        if not column == 0:
            return
        if value:
            if role == Qt.DecorationRole:
                file_info = self.fileInfo(index)
                self.dataChanged.emit(index, index)
            return True
        return False


class SortFilterProxyModel(QSortFilterProxyModel):
    """
    过滤model类， 作用为对model数据进行排序过滤
    """
    
    def __init__(self, parent):
        super(SortFilterProxyModel, self).__init__(parent)
        self.setFilterKeyColumn(0)  # 仅对第一行做过滤
        self.setDynamicSortFilter(True)
        self.setFilterCaseSensitivity(Qt.CaseInsensitive)

    def filterAcceptsRow(self, source_row, source_parent):
        # another way
        try:
            path_valid = self.is_path_valid(source_row, source_parent)
            ret = self.is_parent_root(source_parent)
            if ret:
                _filter = self.filter_accepts_row_itself(source_row, source_parent)
                if _filter:
                    return True and path_valid
                if self.filter_accepts_any_parent(source_parent):
                    return True
                return self.has_accepted_children(source_row, source_parent)
            return True
        except:
            return True

    def filter_accepts_row_itself(self, row_num, parent):
        filter_result = super(SortFilterProxyModel, self).filterAcceptsRow(row_num, parent)
        return filter_result

    def filter_accepts_any_parent(self, source_parent):
        ''' Traverse to the root node and check if any of the
            ancestors match the filter
        '''
        while source_parent.isValid():
            if self.filter_accepts_row_itself(source_parent.row(), source_parent.parent()):
                return True
            source_parent = source_parent.parent()
        return False

    def has_accepted_children(self, row_num, parent):
        ''' Starting from the current node as root, traverse all
            the descendants and test if any of the children match
        '''
        model = self.sourceModel()
        source_index = model.index(row_num, 0, parent)
        children_count = model.rowCount(source_index)
        for i in xrange(children_count):
            if self.filterAcceptsRow(i, source_index):
                return True
            if self.has_accepted_children(i, source_index):
                return True
        return False

    def is_parent_root(self, index):
        source_model = self.sourceModel()
        if index.isValid():
            if index == source_model.index(source_model.rootPath()):
                return True
            else:
                return self.is_parent_root(index.parent())
        return False

    def is_path_valid(self, source_row, source_parent):
        source_model = self.sourceModel()
        index = source_model.index(source_row, 0, source_parent)
        path = str(self.sourceModel().filePath(index))
        path_valid = self.sourceModel().is_path_valid(path)
        return path_valid
