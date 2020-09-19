# _ * _ coding: utf-8 _ * _ #
# @Time         :2020/7/25 15:24
# @FileName     :library_UI.py
# @Author       :LiuYang

import dayu_widgets as dy
from PySide2 import QtWidgets
from PySide2 import QtCore
from LibPackages import package
from LibPackages import File


class PublishInformation(QtWidgets.QWidget):
    def __init__(self):
        super(PublishInformation, self).__init__()
        self.lib_data = File.File(package.get("LibData/library_config.yaml")).read_data_from_file()["CATEGORY"]
        self.setObjectName("PublishInformation")
        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.tabletLayout = QtWidgets.QHBoxLayout(self)
        self.tabletLayout.setContentsMargins(0, 0, 0, 0)
        self.resetStacked = dy.qt.QStackedWidget()

        self.PublishCheck_menu = TableMenu(u"发布检查", index=0)
        self.PublishSett_menu = TableMenu(u"发布信息", index=1)

        # assetWidget setting
        self.assetScrollArea = QtWidgets.QScrollArea()
        self.assetScrollArea.setObjectName("assetScrollArea")

        self.assetScrollArea.setWidgetResizable(True)

        self.assetWidget = QtWidgets.QWidget()
        self.assetWidget.setObjectName("assetWidget")
        self.assetLayout = QtWidgets.QVBoxLayout(self.assetWidget)

        self.assetScrollArea.setWidget(self.assetWidget)

        self.assetsNameLayout = QtWidgets.QHBoxLayout()
        self.assetsNameLabel = dy.MLabel(u"资产名称:").strong()
        self.assetsNameLine = dy.MLineEdit()
        self.assetsNameLine.setFixedWidth(250)
        self.assetsNameLayout.addWidget(self.assetsNameLabel)
        self.assetsNameLayout.addWidget(self.assetsNameLine)

        self.assetsCodeLayout = QtWidgets.QHBoxLayout()
        self.assetsCodeLabel = dy.MLabel(u"资产CODE:").strong()
        self.assetsCodeLine = dy.MLineEdit()
        self.assetsCodeLine.setFixedWidth(250)
        self.assetsCodeLayout.addWidget(self.assetsCodeLabel)
        self.assetsCodeLayout.addWidget(self.assetsCodeLine)

        self.TopCategoryLayout = QtWidgets.QHBoxLayout()
        self.TopCategoryLabel = dy.MLabel(u"一级分类:").strong()
        self.TopCategoryLine = dy.MComboBox()
        self.set_combobox(self.TopCategoryLine, self.lib_data)
        self.TopCategoryLine.setFixedWidth(200)
        self.TopCategoryLayout.addWidget(self.TopCategoryLabel)
        self.TopCategoryLayout.addWidget(self.TopCategoryLine)

        self.SecondaryCategoryLayout = QtWidgets.QHBoxLayout()
        self.SecondaryCategoryLabel = dy.MLabel(u"二级分类:").strong()
        self.SecondaryCategoryLine = dy.MComboBox()

        self.SecondaryCategoryLine.setFixedWidth(200)
        self.SecondaryCategoryLayout.addWidget(self.SecondaryCategoryLabel)
        self.SecondaryCategoryLayout.addWidget(self.SecondaryCategoryLine)

        self.ThirdCategoryLayout = QtWidgets.QHBoxLayout()
        self.ThirdCategoryLabel = dy.MLabel(u"三级分类:").strong()
        self.ThirdCategoryLine = dy.MComboBox()
        self.ThirdCategoryLine.setFixedWidth(200)
        self.ThirdCategoryLayout.addWidget(self.ThirdCategoryLabel)
        self.ThirdCategoryLayout.addWidget(self.ThirdCategoryLine)

        self.MapResolutionLayout = QtWidgets.QHBoxLayout()
        self.MapResolutionLabel = dy.MLabel(u"贴图分辨率：").strong()
        self.MapResolutionCombobox = dy.MComboBox()
        self.MapResolutionCombobox.setMaximumWidth(200)
        self.menu = dy.MMenu()
        self.menu.set_data(["8K", "4K", "2K"])
        self.MapResolutionCombobox.set_menu(self.menu)
        self.MapResolutionLayout.addWidget(self.MapResolutionLabel)
        self.MapResolutionLayout.addWidget(self.MapResolutionCombobox)
        self.MapResolutionCombobox.set_value("8K")

        self.describeText = dy.MTextEdit()
        self.describeText.setMaximumHeight(500)
        self.describeText.setPlaceholderText(self.tr(u'请输入一些描述'))

        # uploadWidget
        self.uploadScrollArea = QtWidgets.QScrollArea()
        self.uploadScrollArea.setObjectName("uploadScrollArea")
        self.uploadScrollArea.setWidgetResizable(True)

        self.uploadWidget = QtWidgets.QWidget()

        self.uploadLayout = QtWidgets.QVBoxLayout(self.uploadWidget)
        self.uploadScrollArea.setWidget(self.uploadWidget)

        self.previewLayout = QtWidgets.QHBoxLayout()
        self.previewCheckBox = dy.MCheckBox()
        self.previewCheckBoxLabel = dy.MLabel(u"预览图片").strong()
        self.previewLabel = dy.MLabel().strong()

        self.zbLayout = QtWidgets.QHBoxLayout()
        self.zbCheckBox = dy.MCheckBox()
        self.zbCheckBoxLabel = dy.MLabel(u"Zbrush 文件").strong()
        self.zbLabel = dy.MLabel().strong()

        self.spLayout = QtWidgets.QHBoxLayout()
        self.spCheckBox = dy.MCheckBox()
        self.spCheckBoxLabel = dy.MLabel(u"Substance 文件").strong()
        self.spLabel = dy.MLabel().strong()

        self.textureLayout = QtWidgets.QHBoxLayout()
        self.textureCheckBox = dy.MCheckBox()
        self.textureCheckBoxLabel = dy.MLabel(u"贴图文件").strong()
        self.textureLabel = dy.MLabel().strong()

        self.maLayout = QtWidgets.QHBoxLayout()
        self.maCheckBox = dy.MCheckBox()
        self.maCheckBoxLabel = dy.MLabel(u"ma文件").strong()
        self.maLabel = dy.MLabel().strong()

        self.mbLayout = QtWidgets.QHBoxLayout()
        self.mbCheckBox = dy.MCheckBox()
        self.mbCheckBoxLabel = dy.MLabel(u"mb文件").strong()
        self.mbLabel = dy.MLabel().strong()

        self.fbxLayout = QtWidgets.QHBoxLayout()
        self.fbxCheckBox = dy.MCheckBox()
        self.fbxCheckBoxLabel = dy.MLabel(u"fbx文件").strong()
        self.fbxLabel = dy.MLabel().strong()

        self.setup_ui()
        self.connect_ui()
        self.set_theme()

    def setup_ui(self):
        self.mainLayout.addLayout(self.tabletLayout)
        self.mainLayout.addWidget(self.resetStacked)

        self.tabletLayout.addStretch()
        self.tabletLayout.addWidget(self.PublishCheck_menu)
        self.tabletLayout.addStretch()
        self.tabletLayout.addWidget(self.PublishSett_menu)
        self.tabletLayout.addStretch()

        self.resetStacked.addWidget(self.uploadScrollArea)
        self.resetStacked.addWidget(self.assetScrollArea)

        self.assetLayout.addLayout(self.assetsNameLayout)

        self.assetLayout.addLayout(self.assetsCodeLayout)

        self.assetLayout.addLayout(self.TopCategoryLayout)

        self.assetLayout.addLayout(self.SecondaryCategoryLayout)

        self.assetLayout.addLayout(self.ThirdCategoryLayout)

        self.assetLayout.addLayout(self.MapResolutionLayout)

        self.assetLayout.addWidget(self.describeText)

        self.uploadLayout.addLayout(self.previewLayout)
        self.uploadLayout.addWidget(dy.MDivider(""))
        self.uploadLayout.addLayout(self.zbLayout)
        self.uploadLayout.addWidget(dy.MDivider(""))
        self.uploadLayout.addLayout(self.spLayout)
        self.uploadLayout.addWidget(dy.MDivider(""))
        self.uploadLayout.addLayout(self.textureLayout)
        self.uploadLayout.addWidget(dy.MDivider(""))
        self.uploadLayout.addWidget(dy.MLabel())
        self.uploadLayout.addLayout(self.maLayout)
        self.uploadLayout.addWidget(dy.MDivider(""))
        self.uploadLayout.addLayout(self.mbLayout)
        self.uploadLayout.addWidget(dy.MDivider(""))
        self.uploadLayout.addLayout(self.fbxLayout)

        self.uploadLayout.addStretch()

        self.previewLayout.addWidget(self.previewCheckBox)
        self.previewLayout.addWidget(self.previewCheckBoxLabel)
        self.previewLayout.addStretch()
        self.previewLayout.addWidget(self.previewLabel)
        self.previewLayout.addStretch()

        self.zbLayout.addWidget(self.zbCheckBox)
        self.zbLayout.addWidget(self.zbCheckBoxLabel)
        self.zbLayout.addStretch()
        self.zbLayout.addWidget(self.zbLabel)
        self.zbLayout.addStretch()

        self.spLayout.addWidget(self.spCheckBox)
        self.spLayout.addWidget(self.spCheckBoxLabel)
        self.spLayout.addStretch()
        self.spLayout.addWidget(self.spLabel)
        self.spLayout.addStretch()

        self.textureLayout.addWidget(self.textureCheckBox)
        self.textureLayout.addWidget(self.textureCheckBoxLabel)
        self.textureLayout.addStretch()
        self.textureLayout.addWidget(self.textureLabel)
        self.textureLayout.addStretch()

        self.maLayout.addWidget(self.maCheckBox)
        self.maLayout.addWidget(self.maCheckBoxLabel)
        self.maLayout.addStretch()
        self.maLayout.addWidget(self.maLabel)
        self.maLayout.addStretch()

        self.mbLayout.addWidget(self.mbCheckBox)
        self.mbLayout.addWidget(self.mbCheckBoxLabel)
        self.mbLayout.addStretch()
        self.mbLayout.addWidget(self.mbLabel)
        self.mbLayout.addStretch()

        self.fbxLayout.addWidget(self.fbxCheckBox)
        self.fbxLayout.addWidget(self.fbxCheckBoxLabel)
        self.fbxLayout.addStretch()
        self.fbxLayout.addWidget(self.fbxLabel)
        self.fbxLayout.addStretch()

    def connect_ui(self):
        self.PublishCheck_menu.left_single.connect(self.set_table_widget)
        self.PublishSett_menu.left_single.connect(self.set_table_widget)

        self.TopCategoryLine.currentTextChanged.connect(self.set_sec_combobox)

        self.SecondaryCategoryLine.currentTextChanged.connect(self.set_thr_combobox)

    def set_table_widget(self, index):
        if index == 0:
            self.PublishSett_menu.setStyleSheet("color: rgb(120, 120, 120);")
            self.PublishCheck_menu.setStyleSheet("color: rgb(250, 250, 250);")
        else:
            self.PublishCheck_menu.setStyleSheet("color: rgb(120, 120, 120);")
            self.PublishSett_menu.setStyleSheet("color: rgb(250, 250, 250);")

        self.resetStacked.setCurrentIndex(index)

    def set_theme(self):
        theme = dy.MTheme(theme="dark")
        theme.apply(self)
        self.setStyleSheet(
            "QWidget#assetScrollArea{border:0px; border-radius: 0px; background-color: rgb(40, 40, 40)}"
            "QWidget#uploadScrollArea{border:0px; border-radius: 0px; background-color: rgb(40, 40, 40)}"
            "QLineEdit{background-color: rgb(50, 50, 50)}"
            "QTextEdit{background-color: rgb(50, 50, 50)}"
            "QCheckBox{background-color: rgb(40, 40, 40)}"
                           )

    @staticmethod
    def set_combobox(combobox, category):
        menu = dy.MMenu()
        menu.set_data([cate["name"] for cate in category])
        combobox.set_menu(menu)

    def set_sec_combobox(self):
        """
        设置第二级分类
        :return:
        """
        for i in self.lib_data:
            if i["name"] == self.TopCategoryLine.currentText():
                self.set_combobox(self.SecondaryCategoryLine, i["category"])
                self.TopCategoryLine.setObjectName(i["code"])

    def set_thr_combobox(self):
        """
        设置第三级分类
        :return:
        """
        for i in self.lib_data:
            if i["name"] == self.TopCategoryLine.currentText():
                for third in i["category"]:
                    if third["name"] == self.SecondaryCategoryLine.currentText():
                        self.set_combobox(self.ThirdCategoryLine, third["category"])
                        if not third["category"]:
                            self.ThirdCategoryLine.setCurrentText("")
                        self.SecondaryCategoryLine.setObjectName(third["code"])


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

    def mouseMoveEvent(self, event):
        super(TableMenu, self).mouseMoveEvent(event)


if __name__ == '__main__':
    window = PublishInformation()
    window.show()
