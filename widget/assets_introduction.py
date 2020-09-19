# _ * _ coding: utf-8 _ * _ #
# @Time         :2020/7/25 15:24
# @FileName     :library_UI.py
# @Author       :LiuYang

import os
import re
import dayu_widgets as dy
from Libs import package
from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui
from widget import image_preview


class Introduction(QtWidgets.QWidget):
    def __init__(self, root_path):
        super(Introduction, self).__init__()
        self.root_path = root_path
        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.ScrollAreaWidget = QtWidgets.QScrollArea()

        self.ScrollAreaWidget.setWidgetResizable(True)

        self.mainWidget = QtWidgets.QWidget()
        self.ScrollAreaWidget.setWidget(self.mainWidget)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        self.Label = QtWidgets.QLabel()
        self.Label.setMinimumHeight(80)
        self.ScrollLayout = QtWidgets.QVBoxLayout(self.mainWidget)
        self.ScrollLayout.setContentsMargins(0, 0, 0, 0)

        self.data = None

        self.previewLayout = QtWidgets.QHBoxLayout()

        self.previewLabel = PreviewLabel()
        self.previewLabel.setMaximumHeight(300)

        # self.max_preview = image_preview.Preview()

        self.previewNameLayout = QtWidgets.QHBoxLayout()
        self.previewNameLabel = dy.MLabel().strong().h2()

        self.assetsInformation = AssetsInformation()

        self.modifyLayout = QtWidgets.QHBoxLayout()
        self.modifyButton = dy.MPushButton(u"修改").primary()
        self.modifyButton.setMinimumWidth(180)
        self.modifyButton.setMinimumHeight(150)

        self.setup_ui()
        self.connect_ui()
        self.set_theme()

    def connect_ui(self):
        self.previewLabel.DoubleClickSignal.connect(self.show_max_preview)

    def show_max_preview(self, path):
        self.max_preview = image_preview.Preview(path)
        self.max_preview.show()

    def set_data(self, data):
        """
        设置信息窗口
        :param data:
        :return:
        """
        assets_data = data
        image_path = assets_data["PreviewPath"]
        assets_name = assets_data["AssetsName"]
        ma_path = assets_data["MAPath"]
        mb_path = assets_data["MBPath"]
        substance_path = assets_data["SubPainterPath"]
        zbrush_path = assets_data["ZbrshPath"]
        texture_path = assets_data["TexturePath"]
        top_category = assets_data["TopCategory"]
        describe = assets_data["Describe"]
        map_resolution = assets_data["MapResolution"]

        self.set_preview_image(image_path)
        self.set_preview_name(assets_name)
        self.assetsInformation.assetText.setText(describe)

        self.assetsInformation.mayaPath.setText("Home/{0}".format(os.path.splitext(ma_path)[0]))
        self.assetsInformation.spPath.setText("Home/{0}".format(os.path.splitext(substance_path)[0]))
        self.assetsInformation.zbPath.setText("Home/{0}".format(os.path.splitext(zbrush_path)[0]))
        self.assetsInformation.texture_resolutionCombobox.set_value(map_resolution)

    def set_preview_image(self, image_path):
        """
        设置预览图
        :param image_path:  预览图尺寸
        :return:
        """
        image_path = os.path.join(self.root_path, image_path)
        if not os.path.exists(image_path):
            image_path = package.get("Icon/app-maya.png")
        self.previewLabel.setPixmap(image_path)

    def set_preview_name(self, name):
        """
        设置资产预览名称
        :param name:
        :return:
        """
        self.previewNameLabel.setText(name)

    def setup_ui(self):
        self.mainLayout.addWidget(self.ScrollAreaWidget)
        self.mainLayout.addWidget(dy.MLabel())
        self.mainLayout.addLayout(self.modifyLayout)
        self.mainLayout.addWidget(dy.MLabel())

        self.ScrollLayout.addLayout(self.previewLayout)
        self.ScrollLayout.addWidget(dy.MDivider(""))

        self.previewLayout.addStretch()
        self.previewLayout.addWidget(self.previewLabel)
        self.previewLayout.addStretch()

        self.ScrollLayout.addWidget(self.Label)
        self.ScrollLayout.addLayout(self.previewNameLayout)
        self.ScrollLayout.addWidget(self.Label)
        self.ScrollLayout.addWidget(dy.MDivider(""))
        self.ScrollLayout.addWidget(self.assetsInformation)

        self.previewNameLayout.addWidget(self.Label)
        self.previewNameLayout.addWidget(self.previewNameLabel)
        self.previewNameLayout.addStretch()

        self.modifyLayout.addStretch()
        self.modifyLayout.addWidget(self.modifyButton)
        self.modifyLayout.addStretch()

    def set_theme(self):
        theme = dy.MTheme(theme="dark")
        theme.apply(self)
        self.modifyButton.setStyleSheet("border-radius: 15px;")


class AssetsInformation(QtWidgets.QWidget):
    Maya_Signal = QtCore.Signal()
    Sp_Signal = QtCore.Signal()
    ZB_Signal = QtCore.Signal()

    def __init__(self):
        super(AssetsInformation, self).__init__()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.tabletLayout = QtWidgets.QHBoxLayout(self)
        self.tabletLayout.setContentsMargins(0, 0, 0, 0)

        self.AssetInfo_menu = TableMenu(u"资产信息", index=0)
        self.DownSet_menu = TableMenu(u"贴图信息", index=1)

        self.resetStacked = dy.qt.QStackedWidget()

        self.setup_ui()
        self.connect_ui()
        self.set_theme()

    def setup_ui(self):
        self.mainLayout.addLayout(self.tabletLayout)
        self.mainLayout.addWidget(self.resetStacked)

        self.tabletLayout.addStretch()
        self.tabletLayout.addWidget(self.AssetInfo_menu)
        self.tabletLayout.setContentsMargins(0, 0, 0, 0)
        self.tabletLayout.addStretch()
        self.tabletLayout.addWidget(self.DownSet_menu)
        self.tabletLayout.addStretch()

        self.assetScroll = QtWidgets.QScrollArea()
        self.assetScroll.setWidgetResizable(True)

        self.assetInfo = QtWidgets.QWidget()
        self.assetInfo.setObjectName("assetInfo")
        self.assetScroll.setWidget(self.assetInfo)

        self.assetLayout = QtWidgets.QVBoxLayout(self.assetInfo)
        self.assetLayout.setContentsMargins(0, 0, 0, 0)

        self.assetText = dy.MTextEdit()
        self.assetText.setObjectName("assetText")
        self.assetText.setMinimumHeight(150)
        self.assetText.setReadOnly(True)

        self.mayaLayout = QtWidgets.QHBoxLayout()
        self.mayaLabel = dy.MLabel("Maya File:").strong()
        self.mayaPath = dy.MLabel("").strong()
        self.mayaButton = dy.MPushButton("打开").warning()
        self.mayaButton.setMaximumWidth(60)
        self.mayaButton.setStyleSheet("")

        self.mayaLayout.addWidget(self.mayaLabel)
        self.mayaLayout.addWidget(self.mayaPath)
        self.mayaLayout.addWidget(self.mayaButton)

        self.zbLayout = QtWidgets.QHBoxLayout()
        self.zbLabel = dy.MLabel("Zbrush File:").strong()
        self.zbPath = dy.MLabel("").strong()
        self.zbButton = dy.MPushButton("打开").warning()
        self.zbButton.setMaximumWidth(60)
        self.zbButton.setStyleSheet("")

        self.zbLayout.addWidget(self.zbLabel)
        self.zbLayout.addWidget(self.zbPath)
        self.zbLayout.addWidget(self.zbButton)

        self.spLayout = QtWidgets.QHBoxLayout()
        self.spLabel = dy.MLabel("Substance File:").strong()
        self.spPath = dy.MLabel("").strong()
        self.spButton = dy.MPushButton("打开",).warning()
        self.spButton.setMaximumWidth(60)
        self.spButton.setStyleSheet("")

        self.spLayout.addWidget(self.spLabel)
        self.spLayout.addWidget(self.spPath)
        self.spLayout.addWidget(self.spButton)

        self.assetLayout.addWidget(self.assetText)
        self.assetLayout.addWidget(dy.MDivider(""))
        self.assetLayout.addLayout(self.mayaLayout)
        self.assetLayout.addWidget(dy.MDivider(""))
        self.assetLayout.addLayout(self.zbLayout)
        self.assetLayout.addWidget(dy.MDivider(""))
        self.assetLayout.addLayout(self.spLayout)
        self.assetLayout.addWidget(dy.MDivider(""))

        self.textureScroll = QtWidgets.QScrollArea()
        self.textureScroll.setObjectName("textureScroll")
        self.textureScroll.setWidgetResizable(True)

        self.textureInfo = QtWidgets.QWidget()
        self.textureInfo.setObjectName("textureInfo")

        self.textureScroll.setWidget(self.textureInfo)

        self.textureLayout = QtWidgets.QVBoxLayout(self.textureInfo)
        self.textureLayout.setContentsMargins(0, 0, 0, 0)

        self.texture_resolutionLayout = QtWidgets.QHBoxLayout()
        self.texture_resolutionLabel = dy.MLabel(u"贴图分辨率").strong()
        self.texture_resolutionCombobox = dy.MComboBox()
        self.texture_resolutionCombobox.setMinimumWidth(250)

        menu = dy.MMenu()
        menu.set_data(["8K", "4K", "2K"])
        self.texture_resolutionCombobox.set_menu(menu)
        self.texture_resolutionCombobox.set_value("8K")

        self.texture_resolutionLayout.addWidget(dy.MLabel())
        self.texture_resolutionLayout.addWidget(self.texture_resolutionLabel)
        self.texture_resolutionLayout.addStretch()
        self.texture_resolutionLayout.addWidget(self.texture_resolutionCombobox)
        self.texture_resolutionLayout.addWidget(dy.MLabel())

        self.texture_type_Layout = QtWidgets.QHBoxLayout()
        self.texture_type_leftLayout = QtWidgets.QVBoxLayout()
        self.texture_type_rightLayout = QtWidgets.QVBoxLayout()

        self.texture_type_Layout.addLayout(self.texture_type_leftLayout)
        self.texture_type_Layout.addLayout(self.texture_type_rightLayout)

        self.textureLayout.addWidget(dy.MLabel(""))
        self.textureLayout.addLayout(self.texture_resolutionLayout)
        self.textureLayout.addWidget(dy.MLabel(""))
        self.textureLayout.addWidget(dy.MDivider(""))
        self.textureLayout.addLayout(self.texture_type_Layout)

        self.resetStacked.addWidget(self.assetScroll)
        self.resetStacked.addWidget(self.textureScroll)

    def connect_ui(self):
        self.AssetInfo_menu.left_single.connect(self.set_table_widget)
        self.DownSet_menu.left_single.connect(self.set_table_widget)
        self.mayaButton.clicked.connect(self.Maya_Signal.emit)
        self.spButton.clicked.connect(self.Sp_Signal.emit)
        self.zbButton.clicked.connect(self.ZB_Signal.emit)

    def add_texture_widget(self, texture_path):
        if not os.path.exists(texture_path):
            pass
        self.__clean_children(self.texture_type_leftLayout)
        self.__clean_children(self.texture_type_rightLayout)

        left_texture = {"Albedo": "[a-zA-z\s]*_albedo\.[a-zA-z\s]*", "Cavity": "[a-zA-z\s]*_cavity\.[a-zA-z\s]*",
                        "Gloss": "[a-zA-z\s]*_gloss\.[a-zA-z\s]*",
                        "NormalBump": "[a-zA-z\s]*_normal\.[a-zA-z\s]*",
                        "Specular": "[a-zA-z\s]*_specular\.[a-zA-z\s]*"}

        check = False
        tex_type = "JPEG"
        for texture in left_texture.keys():
            re_com = re.compile(left_texture[texture])
            try:
                match = re_com.findall(str(os.listdir(texture_path)))
            except WindowsError:
                match = None

            if match:
                check = True
                tex_type = match[0].split(".")[-1].upper()
            texture_group_box = TextureWidgetGroup(texture, checked=check, tex_type=tex_type)
            self.texture_type_leftLayout.addWidget(texture_group_box)

        right_texture = {"Bump": "[a-zA-z\s]*_bump\.[a-zA-z\s]*", "Displacement": "[a-zA-z\s]*_displace\.[a-zA-z\s]*",
                         "Normal": "[a-zA-z\s]*_normal\.[a-zA-z\s]*",
                         "Roughness": "[a-zA-z\s]*_roughness\.[a-zA-z\s]*",
                         "Transmission": "[a-zA-z\s]*_transmission\.[a-zA-z\s]*"}

        for texture in right_texture.keys():
            re_com = re.compile(right_texture[texture])
            try:
                match = re_com.findall(str(os.listdir(texture_path)))
            except WindowsError:
                match = None
            check = False
            if match:
                check = True
                tex_type = match[0].split(".")[-1].upper()
            texture_group_box = TextureWidgetGroup(texture, checked=check, tex_type=tex_type)
            self.texture_type_rightLayout.addWidget(texture_group_box)

    @staticmethod
    def __clean_children(widget, widget_filter=[]):
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

    def set_table_widget(self, index):
        if index == 0:
            self.DownSet_menu.setStyleSheet("color: rgb(120, 120, 120);")
            self.AssetInfo_menu.setStyleSheet("color: rgb(250, 250, 250);")
        else:
            self.AssetInfo_menu.setStyleSheet("color: rgb(120, 120, 120);")
            self.DownSet_menu.setStyleSheet("color: rgb(250, 250, 250);")
        self.resetStacked.setCurrentIndex(index)

    def set_theme(self):
        theme = dy.MTheme(theme="drak")
        theme.apply(self)
        self.setStyleSheet("QTextEdit#assetText{border:0px; border-radius: 0px; background-color: rgb(40, 40, 40)}")
        self.textureScroll.setStyleSheet("QScrollArea#textureScroll{border:0px; border-radius: 0px; background-color: rgb(40, 40, 40)}")


class TableMenu(dy.MLabel):
    left_single = QtCore.Signal(int)

    def __init__(self, text='', parent=None, flags=0, index=None):
        super(TableMenu, self).__init__(text=text, parent=parent, flags=flags)
        self.setMouseTracking(True)
        self.index = index
        self.setMinimumHeight(40)
        self.strong()
        self.setStyleSheet("color: rgb(120, 120, 120);")

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.left_single.emit(self.index)

    def leaveEvent(self, event):
        pass


class TextureWidgetGroup(QtWidgets.QWidget):
    def __init__(self, tex_name, checked=False, tex_type="JPEG"):
        super(TextureWidgetGroup, self).__init__()
        self.menu_data = ["JPEG", "EXR", "JPEG+EXR", "PNG"]
        self.mainLayout = QtWidgets.QHBoxLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.name_checkbox = dy.MCheckBox(tex_name)
        self.name_checkbox.setStyleSheet("border:0px; border-radius: 0px; background-color: rgb(40, 40, 40)")
        self.name_checkbox.setFont(QtGui.QFont("华文琥珀", 20, QtGui.QFont.Bold))
        self.name_checkbox.setObjectName("{}_name".format(tex_name))
        self.name_checkbox.setChecked(checked)
        self.type_combobox = dy.MComboBox()
        self.type_combobox.setMinimumWidth(80)
        self.type_combobox.setObjectName("{}_type".format(tex_name))
        self.type_combobox.setStyleSheet("background-color: rgb(50, 50, 50)")
        menu = dy.MMenu()
        menu.set_data(self.menu_data)
        self.type_combobox.set_menu(menu)
        self.type_combobox.set_value(tex_type)

        self.setup_ui()

    def setup_ui(self):
        self.mainLayout.addWidget(dy.MLabel(""))
        self.mainLayout.addWidget(self.name_checkbox)
        self.mainLayout.addStretch()
        self.mainLayout.addWidget(self.type_combobox)
        self.mainLayout.addWidget(dy.MLabel(""))


class PreviewLabel(QtWidgets.QLabel):
    DoubleClickSignal = QtCore.Signal(str)

    def __init__(self):
        super(PreviewLabel, self).__init__()
        self.image_path = None

    def mouseDoubleClickEvent(self, event):
        super(PreviewLabel, self).mouseDoubleClickEvent(event)
        if event.button() == QtCore.Qt.LeftButton:
            self.DoubleClickSignal.emit(self.image_path)

    def setPixmap(self, image_path):
        self.image_path = image_path
        preview_image = QtGui.QPixmap(self.image_path)
        scale = preview_image.width() / float(preview_image.height())
        pixmap = QtGui.QPixmap(preview_image)
        super(PreviewLabel, self).setPixmap(pixmap.scaled(300*scale, 300))


if __name__ == '__main__':
    Library = Introduction("D:/")
    Library.show()
