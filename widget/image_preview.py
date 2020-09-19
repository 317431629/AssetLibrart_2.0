# _ * _ coding: utf-8 _ * _ #
# @Time         :2020/7/25 15:24
# @FileName     :library_UI.py
# @Author       :LiuYang

from Libs import package
from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui


class Preview(QtWidgets.QWidget):
    def __init__(self, image):
        super(Preview, self).__init__()
        self.image = QtGui.QPixmap(image)

        width = self.image.width()
        height = self.image.height()
        if width > 1280:
            height = 1280/(width/float(height))
            width = 1280

        if height > 720:
            width = 720/(float(height)/width)
            height = 720

        self.setFixedSize(width, height)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)

        self.label = QtWidgets.QLabel(self)
        self.label.setFixedSize(width, height)
        self.label.setPixmap(self.image.scaled(width, height))

        self.closeButton = CloseLabel(self)
        self.closeButton.move(self.width()-self.closeButton.width - 5, 5)

        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def enterEvent(self, event):
        self.closeButton.show()

    def leaveEvent(self, event):
        self.closeButton.hide()


class CloseLabel(QtWidgets.QLabel):
    def __init__(self, parent):
        super(CloseLabel, self).__init__()
        self.setParent(parent)
        self.parent = parent
        self.nor_pixmap = QtGui.QPixmap(package.get("Icon/close_02.png")).scaled(30, 30)
        self.hight_pixmap = QtGui.QPixmap(package.get("Icon/close_01.png")).scaled(30, 30)
        self.width = self.nor_pixmap.width()
        self.height = self.nor_pixmap.height()

        self.setPixmap(self.nor_pixmap)

    def _close(self):
        self.parent.close()

    def mousePressEvent(self, event):
        super(CloseLabel, self).mousePressEvent(event)
        if event.button() == QtCore.Qt.LeftButton:
            self._close()

    def enterEvent(self, event):
        super(CloseLabel, self).enterEvent(event)
        self.setPixmap(self.hight_pixmap)

    def leaveEvent(self, event):
        super(CloseLabel, self).enterEvent(event)
        self.setPixmap(self.nor_pixmap)


if __name__ == '__main__':
    window = Preview("D:\ToolBox_Project\library\Icon\user.jpg")
    window.show()
