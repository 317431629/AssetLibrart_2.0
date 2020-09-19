# _ * _ coding: utf-8 _ * _ #
# @Time         :2020/7/25 15:24
# @FileName     :library_UI.py
# @Author       :LiuYang


import dayu_widgets as dy
from PySide2 import QtWidgets
from PySide2.QtCore import Qt
from PySide2.QtGui import QPixmap


class LoginUI(QtWidgets.QWidget):
    def __init__(self):
        """
        初始化窗口
        """
        super(LoginUI, self).__init__()
        self.setWindowTitle(u"登录Library")
        self.setGeometry(750, 300, 350, 350)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.mainLayout = QtWidgets.QVBoxLayout(self)

        self.closeLayout = QtWidgets.QHBoxLayout(self)
        self.closeButton = dy.MPushButton("", icon=dy.qt.MIcon('close_line.svg', '#ddd')).small().danger()
        self.closeButton.clicked.connect(self.close)

        self.userAvatarLayout = QtWidgets.QHBoxLayout()
        self.userAvatar = dy.MAvatar()
        self.userAvatar.set_dayu_size(150)
        self.userAvatar.set_dayu_image(QPixmap("D:/ToolBox_Project/library/Icon/male.svg"))
        self.userNameLayout = QtWidgets.QHBoxLayout()
        self.userNameLabel = dy.MAvatar()
        self.userAvatar.set_dayu_image(QPixmap("D:/ToolBox_Project/library/Icon/male.svg"))
        self.userNameLine = dy.MLineEdit()
        self.userNameLine.setMinimumWidth(250)
        self.userNameLine.setPlaceholderText('Enter user name...')

        self.passwordLayout = QtWidgets.QHBoxLayout()
        self.passwordLabel = dy.MAvatar()
        self.passwordLabel.set_dayu_image(QPixmap("D:/ToolBox_Project/library/Icon/edit_fill.svg"))
        self.passwordLine = dy.MLineEdit().password()
        self.passwordLine.setMinimumWidth(250)
        self.passwordLine.setPlaceholderText('Enter the password...')

        self.loginButton = dy.MPushButton("Login").warning()

        self.setup_ui()
        self.set_theme()

    def setup_ui(self):
        self.mainLayout.addLayout(self.closeLayout)
        self.mainLayout.addLayout(self.userAvatarLayout)
        self.mainLayout.addWidget(dy.MLabel("\n"))
        self.mainLayout.addLayout(self.userNameLayout)
        self.mainLayout.addLayout(self.passwordLayout)
        self.mainLayout.addWidget(dy.MDivider("login"))
        self.mainLayout.addWidget(self.loginButton)

        self.closeLayout.addStretch()
        self.closeLayout.addWidget(self.closeButton)

        self.userAvatarLayout.addStretch()
        self.userAvatarLayout.addWidget(self.userAvatar)
        self.userAvatarLayout.addStretch()

        self.userNameLayout.addStretch()
        self.userNameLayout.addWidget(self.userNameLabel)
        self.userNameLayout.addWidget(self.userNameLine)
        self.userNameLayout.addStretch()

        self.passwordLayout.addStretch()
        self.passwordLayout.addWidget(self.passwordLabel)
        self.passwordLayout.addWidget(self.passwordLine)
        self.passwordLayout.addStretch()

    def set_theme(self):
        theme = dy.MTheme(theme="dark")
        theme.apply(self)


if __name__ == '__main__':
    login_ui =LoginUI()
    login_ui.show()
