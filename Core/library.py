# _ * _ coding: utf-8 _ * _ #
# @Time         :2020/7/25 15:24
# @FileName     :library_UI.py
# @Author       :LiuYang

import os
import json
import re
import time
import shutil
import dayu_widgets as dy
try:
    import pymel.core as pm
except ImportError:
    pass

from Core import library_UI
from Libs import File
from Libs import package
from widget import login_ui
from functools import wraps
from functools import partial
from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtGui

reload(library_UI)
reload(File)


def timer(a_func):
    @wraps(a_func)
    def wrap_the_function(obj, path):
        start_time = time.time()
        a_func(obj, path)
        end_time = time.time()
        run_time = (end_time - start_time)
        print run_time
    return wrap_the_function


class LibraryTool(library_UI.LibraryUI):
    def __init__(self):
        super(LibraryTool, self).__init__()
        self.cur_path = None
        self.select_items = []

    def connect_ui(self):
        super(LibraryTool, self).connect_ui()
        self.toolbar.categoryBar.left_signal.connect(lambda paths: self.set_card(paths))
        self.toolbar.toolbar.tag_signal.connect(lambda code: self.set_target(code))

        self.loginButton.menu.login_signal.connect(self.login)
        self.loginButton.menu.logout_signal.connect(self.logout)
        self.loginButton.menu.set_root_signal.connect(self.set_root_path)

        self.listSearchLine.sig_delay_text_changed.connect(self.search_item)

        self.projectCombobox.currentTextChanged.connect(self.search_project_change)

        self.screenShot.screenButton.sig_file_changed.connect(self.change_preview_button_image)
        self.zbDragButton.sig_file_changed.connect(self.change_zb_button_image)
        self.spDragButton.sig_file_changed.connect(self.change_sp_button_image)
        self.textureDragButton.sig_folder_changed.connect(self.change_texture_text)

        self.introdiction.assetsInformation.Maya_Signal.connect(self.import_maya)

        self.tagFrame.change_signal.connect(self.search_tag_change)

        self.updateButton.clicked.connect(self.publish)

    def screen_file_changed(self, preview_file):
        file_suffix = os.path.splitext(preview_file)[1]
        if file_suffix not in [".png", ".jpg"]:
            dy.MMessage.error("Place Drag preview File", self)
            raise TypeError("The file suffix {0} is not recognized".format(file_suffix))
        self.screenShot.set_dayu_svg(preview_file)
        self.screenShot.setText(" ")

    def search_tag_change(self, tags=[]):
        """
        搜索对应的标签类型
        :param tags:
        :return:
        """
        self.set_card(self.cur_path)
        for i in range(self.CardLayout.count()):
            for tag in tags:
                if tag not in self.CardLayout.itemAt(i).widget().tag:
                    self.CardLayout.itemAt(i).widget().deleteLater()

    def search_item(self):
        """
        根据名字搜索
        :return:
        """
        search_name = self.listSearchLine.text()
        if search_name:
            name_compile = re.compile("{}*".format(search_name))
            right_card = [card for card in self.CardWidget.children() if re.match(name_compile, card.objectName())]
            self.__clean_children(self.CardWidget, widget_filter=right_card)
        else:
            self.set_card(self.cur_path)

    def search_project_change(self):
        """
        筛选 project
        :return:
        """

        self.set_card(self.cur_path)
        search_project = self.projectCombobox.currentText()
        if search_project == "None":
            self.set_card(self.cur_path)
        else:
            right_card = []
            if search_project:
                for card in self.CardWidget.children():
                    try:
                        if card.project == search_project:
                            right_card.append(card)
                    except AttributeError:
                        pass

                self.__clean_children(self.CardWidget, widget_filter=right_card)
            else:
                self.set_card(self.cur_path)

    def set_target(self, name):
        self.tagFrame.init_tag_view(name)

    def set_card(self, path):
        """
        设置卡片实例
        :param path: TopCategory/SecCategory/ThirdCategory
        :return:
        """
        full_path = os.path.join(self.root_path, path).replace("\\", "/")

        if not os.path.exists(full_path):
            dy.MMessage.warning(u"该分类下没有资产", self)
            return

        self.cur_path = full_path

        data = self.get_card_data(full_path)
        self.__clean_children(self.CardWidget)
        #
        if not data:
            return True

        cards = []

        for card_data in data:
            preview_image = os.path.join(self.root_path, card_data["PreviewPath"]).replace("\\", "/")
            if not os.path.exists(preview_image):
                preview_image = os.path.join(self.iconPath, "app-maya.png")

            setting = self.__set_card_setting(title=card_data["AssetsName"], description=card_data["Describe"],
                                              cover=QtGui.QPixmap(preview_image))

            card = Card(self, card_data)

            card.setup_data(setting)

            card.setObjectName(card_data["AssetsCode"])

            cards.append(card)

        for i in iter(cards):
            self.CardLayout.addWidget(i)

    def get_card_data(self, path):
        """
        获取卡片实例数据
        :param path: root_path/TopCategory/SecCategory/ThirdCategory
        :return:
        """
        # 判断当前路径下是否存在文件
        file = [file_name for file_name in os.listdir(path) if os.path.isfile(os.path.join(path, file_name))]
        if not file:
            return self._get_data(path)
        else:
            return True

    @staticmethod
    def _get_data(path):
        yaml_data = []

        def get_file(file_path):
            for file_name in os.listdir(file_path.replace("\\", "/")):
                if os.path.isfile(os.path.join(file_path, file_name).replace("\\", "/")):
                    if file_name == "information.yaml":
                        yaml_data.append(File.File(os.path.join(file_path, file_name)).read_data_from_file())
                else:
                    get_file(os.path.join(file_path, file_name))

            return yaml_data

        file_data = get_file(path)
        return file_data

    @staticmethod
    def __clean_children(widget, widget_filter=[]):
        if len(widget.children()) == 1:
            return True

        for i in range(widget.children()[0].count()):
            if widget.children()[0].itemAt(i).widget() in widget_filter:
                pass
            else:
                widget.children()[0].itemAt(i).widget().deleteLater()

    @staticmethod
    def __set_card_setting(title, description, cover):
        setting_template = {"title": title,
                            "description": description,
                            "cover": cover}

        return setting_template

    def refresh_list(self):
        self.set_card(self.cur_path)

    def login(self):
        self.loginButton.menu.close()
        self.login_win = login_ui.LoginUI()
        self.login_win.show()

    def logout(self):
        self.loginButton.menu.close()
        dy.MMessage.success("logout success!", self)

    def set_root_path(self):
        self.loginButton.menu.close()
        root_path = QtWidgets.QFileDialog.getExistingDirectory().replace("\\", "/")
        self.config["ROOT_PATH"] = root_path
        self.config_file.write_data_to_file(self.config, write_mode="w")
        self.root_path = root_path

    def change_preview_button_image(self, preview_file):
        file_suffix = os.path.splitext(preview_file)[1]
        if file_suffix not in [".jpg", ".png"]:
            dy.MMessage.error("Place Drag preview File", self)
            raise TypeError("The file suffix {0} is not recognized".format(file_suffix))
        self.screenShot.screenButton.set_dayu_svg(preview_file)
        self.screenShot.screenButton.setIconSize(QtCore.QSize(1080, 1080))
        self.screenShot.screenButton.setText("")
        self.informationWidget.previewCheckBox.setChecked(True)
        self.informationWidget.previewLabel.setText(os.path.split(preview_file)[-1])
        self.preview_path = preview_file
        return self.preview_path

    def change_zb_button_image(self, zb_file):
        file_suffix = os.path.splitext(zb_file)[1]
        if file_suffix not in [".ZBR", ".ZTL", ".ZPR"]:
            dy.MMessage.error("Place Drag Zbrush File", self)
            raise TypeError("The file suffix {0} is not recognized".format(file_suffix))
        self.zbDragButton.set_dayu_svg(package.get("Icon/Zbrush_done.png"))
        self.informationWidget.zbCheckBox.setChecked(True)
        self.informationWidget.zbLabel.setText(os.path.split(zb_file)[-1])
        self.zb_path = zb_file
        return self.zb_path

    def change_sp_button_image(self, sp_file):
        file_suffix = os.path.splitext(sp_file)[1]
        if file_suffix not in [".spp"]:
            dy.MMessage.error("Place Drag Substance Paint File", self)
            raise TypeError("The file suffix {0} is not recognized".format(file_suffix))
        self.spDragButton.set_dayu_svg(package.get("Icon/substance_done.png"))
        self.informationWidget.spCheckBox.setChecked(True)
        self.informationWidget.spLabel.setText(os.path.split(sp_file)[-1])
        self.sp_path = sp_file
        return self.sp_path

    def change_texture_text(self, texture_dir):
        if not os.listdir(texture_dir):
            dy.MMessage.warning("There are no files in this path! Place Check", self)
        self.informationWidget.textureCheckBox.setChecked(True)
        self.informationWidget.textureLabel.setText(os.path.split(texture_dir)[-1])
        self.texture_path = texture_dir
        return self.texture_path

    def publish(self):
        """
        发布资产到资产库
        assets_name： 资产名字
        assets_code： 资产Code
        top_category： 第一级分类
        sec_category： 第二级分类
        third_category： 第三级分类
        map_resolution： 贴图分辨率
        assets_path： 资产路径
        ma_path： ma文件路径
        mb_path： mb文件路径
        fbx_path： fbx文件路径
        zbrush_path： zbrush文件路径
        sub_paint_path： sunstance paint文件路径
        texture_path： 贴图文件文件路径
        preview_path： 预览图文件路径
        describe： 描述文字
       :return:
        """

        assets_name = self.informationWidget.assetsNameLine.text()
        assets_code = self.informationWidget.assetsCodeLine.text()
        top_category = self.informationWidget.TopCategoryLine.objectName()
        sec_category = self.informationWidget.SecondaryCategoryLine.objectName()
        third_category = self.informationWidget.ThirdCategoryLine.objectName()
        map_resolution = self.informationWidget.MapResolutionCombobox.currentText()
        assets_path = os.path.join(top_category, sec_category, third_category, assets_name).replace("\\", "/")
        if not third_category:
            assets_path = os.path.join(top_category, sec_category, assets_name).replace("\\", "/")
        ma_path = "{0}/{1}.ma".format(assets_path, assets_name)
        mb_path = "{0}/{1}.mb".format(assets_path, assets_name)
        fbx_path = "{0}/{1}.fbx".format(assets_path, assets_name)
        zbrush_path = "{0}/{1}.ZTL".format(assets_path, assets_name)
        sub_paint_path = "{0}/{1}.spp".format(assets_path, assets_name)
        texture_path = "{0}/Texture".format(assets_path, assets_name)
        preview_path = "{0}/{1}.jpg".format(assets_path, assets_name)

        describe = self.informationWidget.describeText.toPlainText()

        if not assets_name:
            dy.MMessage.error(u"没有指定资产名称, 请检查 Assets Name", self)
            self.informationWidget.assetsNameLabel.set_dayu_type("danger")
        if not top_category:
            dy.MMessage.error(u"没有指定资产类型, 请检查 Top Category", self)
            self.informationWidget.TopCategoryLabel.set_dayu_type("danger")
        if not sec_category:
            dy.MMessage.error(u"没有指定资产类型, 请检查 Sec Category", self)
            self.informationWidget.SecondaryCategoryLabel.set_dayu_type("danger")

        if not os.path.exists(os.path.join(self.root_path, texture_path)):
            os.makedirs(os.path.join(self.root_path, texture_path))

        self.write_information(os.path.join(self.root_path, assets_path, "information.yaml").replace("\\", "/"),
                               self.format_information(assets_name, assets_code, top_category, sec_category,
                                                       third_category, ma_path, mb_path, fbx_path, sub_paint_path,
                                                       zbrush_path, preview_path, texture_path,
                                                       map_resolution, describe)
                               )

        self._copy_file(self.preview_path, os.path.join(self.root_path, preview_path))

        self._copy_file(self.sp_path, os.path.join(self.root_path, sub_paint_path))

        self._copy_file(self.zb_path, os.path.join(self.root_path, zbrush_path))

        for texture in os.listdir(self.texture_path):
            self._copy_file(
                os.path.join(self.texture_path, texture),
                os.path.join(os.path.join(self.root_path, texture_path), texture)
            )

        if self.informationWidget.maCheckBox.isChecked():
            self.save_maya_file(os.path.join(self.root_path, ma_path))
        if self.informationWidget.mbCheckBox.isChecked():
            self.save_maya_file(os.path.join(self.root_path, mb_path))
        if self.informationWidget.fbxCheckBox.isChecked():
            pm.exportAll(os.path.join(self.root_path, fbx_path),
                         force=True, options="v=0", type="FBX export", pr=True, ea=True)

        dy.MMessage.success(u"上传成功！", self)

    @staticmethod
    def _copy_file(ori_path, new_file):
        """
        copy file to target path
        :param ori_path: ori_path
        :return:
        """
        if os.path.isfile(ori_path):
            shutil.copy(ori_path, new_file)

    @staticmethod
    def save_maya_file(path):
        pm.saveAs(path)

    @staticmethod
    def write_information(file_path, data):
        """
        :param file_path: (str), json file of file data
        :param data:
        :return:
        """
        with open(file_path, "w", encoding='utf-8') as information_file:
            json.dump(data, information_file)
        return True

    @staticmethod
    def format_information(assets_name, assets_code, top_cate, sec_cate, third_category, ma_path, mb_path,
                           fbx_path, zb_path, sp_path, pre_path, tex_path, map_resolution, describe):
        assets_information = {
            "AssetsName": assets_name,
            "AssetsCode": assets_code,
            "TopCategory": top_cate,
            "SecCategory": sec_cate,
            "ThridCategory": third_category,
            "MAPath": ma_path,
            "MBPath": mb_path,
            "FBXPath": fbx_path,
            "ZbrshPath": zb_path,
            "SubPainterPath": sp_path,
            "PreviewPath": pre_path,
            "TexturePath": tex_path,
            "MapResolution": map_resolution,
            "Describe": describe
            }
        return assets_information

    def _get_assets_path(self, top_type, sec_type, file_name):
        assets_path = os.path.join(self.root_path, top_type, sec_type, file_name)
        return assets_path

    def import_maya(self):
        maya_file = os.path.join(self.root_path, self.introdiction.assetsInformation.mayaPath.text().split("Home/")[-1])

        if os.path.exists("{}.ma".format(maya_file)):
            maya_file = "{}.ma".format(maya_file)
        else:
            maya_file = "{}.mb".format(maya_file)

        pm.openFile(maya_file, force=True)
        dy.MMessage.success("import success!", self)


class Card(dy.MMeta):
    double_click_signal = QtCore.Signal()

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

    @property
    def tag(self):
        try:
            tag = self.assets_data["Tag"]
        except KeyError:
            tag = []
        return tag

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

    def set_project(self, item_list):
        items = File.File(package.get("Data/project_data.yaml").replace("\\", "/")).read_data_from_file()
        project_data = QtWidgets.QInputDialog().getItem(self, "Get item", "Project:", items, 0, False)[0]
        for item in item_list:
            item.menu.set_project(project_data)


# TODO: 替换Card
class NewCard(QtWidgets.QWidget):
    # TODO: 将Card 替换为图片

    def __init__(self, widget_parent, assets_data):
        super(NewCard, self).__init__()
        self.parent = widget_parent
        self.assets_data = assets_data
        self.menu = None

        self.image_label = QtWidgets.QLabel(self)
        self.setFixedSize(324, 216)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.pix_map = QtGui.QPixmap(self.assets_data["PreviewPath"])

        self.nameLabel = QtWidgets.QLabel(self.assets_data["AssetsName"])
        # self.nameLabel.hide()
        self.nameLabel.setParent(self)

        scale = self.pix_map.width()/float(self.pix_map.height())
        if scale*216 < 324:
            pix_map = self.pix_map.scaled(scale*216, 216)
        else:
            pix_map = self.pix_map.scaled(324, 324/scale)

        self.image_label.setPixmap(pix_map)
        self.nameLabel.move(5, self.height()-15)

    def mouseDoubleClickEvent(self, event):
        super(Card, self).mouseDoubleClickEvent(event)
        self.parent.introdiction.hide()

    def mousePressEvent(self, event):
        super(Card, self).mousePressEvent(event)
        if event.button() == QtCore.Qt.LeftButton:
            self.parent.introdiction.set_data(self.assets_data)
            self.parent.introdiction.assetsInformation.add_texture_widget(self.assets_data["TexturePath"])
            self.parent.set_introdiction_size()

        elif event.button() == QtCore.Qt.RightButton:
            self.menu = CardMenu(self)
            self.menu.close()
            self.menu.show()
            self.menu.move(QtGui.QCursor.pos())


class CardMenu(QtWidgets.QWidget):
    def __init__(self, parent):
        super(CardMenu, self).__init__()
        self.parent = parent
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        self.mainLayout = QtWidgets.QVBoxLayout(self)

        self.importMayaButton = dy.MPushButton(u"导入Maya文件",
                                               icon=dy.qt.MIcon(package.get("Icon/app-maya.png"))).tiny()

        self.importZbButton = dy.MPushButton(u"打开Zbrush文件",
                                             icon=dy.qt.MIcon(package.get("Icon/Zbrush.png"))).tiny()

        self.importSpButton = dy.MPushButton(u"打开Sp文件",
                                             icon=dy.qt.MIcon(package.get("Icon/SP_Icon.png"))).tiny()

        self.openDirButton = dy.MPushButton(u"打开资产文件夹",
                                            icon=dy.qt.MIcon(package.get("Icon/folder_fill.svg"))).tiny()

        self.removeCardButton = dy.MPushButton(u"从资产库删除资产",
                                               icon=dy.qt.MIcon(package.get("Icon/trash_line.svg"))).tiny().warning()

        self.setProjectButton = dy.MPushButton(u"设置项目",
                                               icon=dy.qt.MIcon(package.get("Icon/gongju_an.svg"))).tiny()
        self.setProjectButton.hide()

        self.set_theme()
        self.setup_ui()
        self.connect_ui()

    def setup_ui(self):
        self.mainLayout.addWidget(self.importMayaButton)
        self.mainLayout.addWidget(dy.MDivider(""))
        self.mainLayout.addWidget(self.importZbButton)
        self.mainLayout.addWidget(self.importSpButton)
        self.mainLayout.addWidget(dy.MDivider(""))
        self.mainLayout.addWidget(self.openDirButton)
        self.mainLayout.addWidget(self.removeCardButton)
        self.mainLayout.addWidget(self.setProjectButton)

    def connect_ui(self):
        self.importMayaButton.clicked.connect(self.import_maya)
        self.importZbButton.clicked.connect(self.import_zb)
        self.importSpButton.clicked.connect(self.import_sp)
        self.openDirButton.clicked.connect(self.open_cur_dir)
        self.removeCardButton.clicked.connect(self.remove_card)
        self.setProjectButton.clicked.connect(self.set_project)

    def show_button(self, shift=False):
        if not shift:
            self.setProjectButton.hide()
        else:
            self.importMayaButton.hide()
            self.importZbButton.hide()
            self.importSpButton.hide()
            self.openDirButton.hide()
            self.removeCardButton.hide()
            self.setProjectButton.show()

    def import_maya(self):
        ma_file = self.parent.assets_data["MAPath"]
        mb_file = self.parent.assets_data["MBPath"]
        maya_file = ma_file
        if not maya_file:
            maya_file = mb_file

        self.close()
        pm.importFile(os.path.join(self.parent.parent.root_path, maya_file))
        dy.MMessage.success("import success!", self.parent.parent)

    def import_zb(self):
        self.close()
        dy.MMessage.success("import success!", self.parent.parent)

    def import_sp(self):
        self.close()
        dy.MMessage.success("import success!", self.parent.parent)

    def remove_card(self):
        # TODO: 等用户信息完善后再完善
        self.close()
        dy.MMessage.success("remove success!", self.parent)

    def open_cur_dir(self):
        """
        打开当前选择目录
        :return:
        """
        start_directory = os.path.split(self.parent.assets_data["SubPainterPath"])[0]
        os.startfile(os.path.join(self.parent.parent.root_path, start_directory))
        self.close()
        dy.MMessage.success("open dir success!", self.parent.parent)

    def set_project(self, project_data):
        """
        设置选择实例的项目属性
        :return:
        """
        start_directory = os.path.split(self.parent.assets_data["SubPainterPath"])[0]
        project = File.File(os.path.join(self.parent.parent.root_path, start_directory, "project.yaml"))
        project_data = {"Project": project_data}
        project.write_data_to_file(project_data, write_mode="w")
        self.close()
        dy.MMessage.success("set project success!", self.parent.parent)

    def set_theme(self):
        theme = dy.MTheme(theme="dark")
        theme.apply(self)


if __name__ == '__main__':
    Library = LibraryTool()
    Library.show()
