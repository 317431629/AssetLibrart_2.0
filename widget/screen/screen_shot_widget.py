# _ * _ coding: utf-8 _ * _ #
# @Time         :2020/7/25 15:24
# @FileName     :library_UI.py
# @Author       :LiuYang

import dayu_widgets as dy
import tempfile
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from widget.screen import screen_grab
import os


class ScreenShot(QFrame):
    thumbnail_changed = Signal()

    def __init__(self, text):
        super(ScreenShot, self).__init__()
        self.mainLayout = QVBoxLayout(self)
        self.imageLabel = QLabel()
        self.screenButton = ScreenShotButton(text=text)
        self.mainLayout.addWidget(self.imageLabel)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.addWidget(self.screenButton)

        dy.MTheme(theme="dark").apply(self)

        self.temp_preview = os.path.join(tempfile.gettempdir(), "preview.jpg")

        self.screenButton.clicked.connect(self._on_camera_clicked)
        self.thumbnail_changed.connect(self._on_thumbnail_changed)

    # @property
    def _get_thumbnail(self):
        pm_map = self._ui.thumbnail.pixmap()
        return pm_map if pm_map and not pm_map.isNull() else None

    def get_thumbnail_path(self):
        pm_map = self._get_thumbnail()
        if pm_map:
            output_path = tempfile.NamedTemporaryFile(suffix=".png",
                                                      prefix="screencapture_",
                                                      delete=False).name
            pm_map.save(output_path)
            return output_path
        return None

    # @thumbnail.setter
    def _set_thumbnail(self, value):
        self._ui.thumbnail.setPixmap(value if value else QPixmap())
        self._update_ui()
        self.thumbnail_changed.emit()

    thumbnail = property(_get_thumbnail, _set_thumbnail)

    def enable_screen_capture(self, enable):
        self._ui.camera_btn.setVisible(enable)

    # def resizeEvent(self, event):
    #     self._update_ui()
    #
    # def enterEvent(self, event):
    #     """
    #     when the cursor enters the control, show the buttons
    #     """
    #     if self.thumbnail and self._are_any_btns_enabled():
    #         self._ui.buttons_frame.show()
    #         if hasattr(Qtegg.QtCore, "QAbstractAnimati1on"):
    #             self._run_btns_transition_anim(QAbstractAnimation.Forward)
    #         else:
    #             # Q*Animation classes aren't available so just
    #             # make sure the button is visible:
    #             self.btn_visibility = 1.0
    #
    # def leaveEvent(self, event):
    #     """
    #     when the cursor leaves the control, hide the buttons
    #     """
    #     if self.thumbnail and self._are_any_btns_enabled():
    #         if hasattr(Qtegg.QtCore, "QAbstractAnimation"):
    #             self._run_btns_transition_anim(QAbstractAnimation.Backward)
    #         else:
    #             # Q*Animation classes aren't available so just
    #             # make sure the button is hidden:
    #             self._ui.buttons_frame.hide()
    #             self.btn_visibility = 0.0

    def _are_any_btns_enabled(self):
        """
        Return if any of the buttons are enabled
        """
        return not (self._ui.camera_btn.isHidden())

    """
    button visibility property used by QPropertyAnimation
    """

    def get_btn_visibility(self):
        return self._btns_visibility

    def set_btn_visibility(self, value):
        self._btns_visibility = value
        self._ui.buttons_frame.setStyleSheet(
            "#buttons_frame {border-radius: 2px; background-color: rgba(32, 32, 32, %d);}" % (64 * value))

    btn_visibility = Property(float, get_btn_visibility, set_btn_visibility)

    def _run_btns_transition_anim(self, direction):
        """
        Run the transition animation for the buttons
        """
        if not self._btns_transition_anim:
            # set up anim:
            self._btns_transition_anim = QPropertyAnimation(self, "btn_visibility")
            self._btns_transition_anim.setDuration(150)
            self._btns_transition_anim.setStartValue(0.0)
            self._btns_transition_anim.setEndValue(1.0)
            self._btns_transition_anim.finished.connect(self._on_btns_transition_anim_finished)

        if self._btns_transition_anim.state() == QAbstractAnimation.Running:
            if self._btns_transition_anim.direction() != direction:
                self._btns_transition_anim.pause()
                self._btns_transition_anim.setDirection(direction)
                self._btns_transition_anim.resume()
            else:
                pass  # just let animation continue!
        else:
            self._btns_transition_anim.setDirection(direction)
            self._btns_transition_anim.start()

    def _on_btns_transition_anim_finished(self):
        if self._btns_transition_anim.direction() == QAbstractAnimation.Backward:
            self._ui.buttons_frame.hide()

    def _on_camera_clicked(self):
        # if self.parent():
        #     self.parent().parent().parent().parent().hide()
        # else:
        #     self.hide()
        pm_map = self._on_screenshot()
        if pm_map:
            pm_map.save(self.temp_preview)
            self.screenButton.set_dayu_svg(self.temp_preview)
            self.screenButton.setText("")

    def _update_ui(self):
        # maximum size of thumbnail is widget geom:
        thumbnail_geom = self.geometry()
        thumbnail_geom.moveTo(0, 0)
        scale_contents = False

        pm_map = self.thumbnail
        if pm_map:
            # work out size thumbnail should be to maximize size
            # whilst retaining aspect ratio
            pm_sz = pm_map.size()

            h_scale = float(thumbnail_geom.height() - 4) / float(pm_sz.height())
            w_scale = float(thumbnail_geom.width() - 4) / float(pm_sz.width())
            scale = min(1.0, h_scale, w_scale)
            scale_contents = (scale < 1.0)

            new_height = min(int(pm_sz.height() * scale), thumbnail_geom.height())
            new_width = min(int(pm_sz.width() * scale), thumbnail_geom.width())

            new_geom = QRect(thumbnail_geom)
            new_geom.moveLeft(((thumbnail_geom.width() - 4) / 2 - new_width / 2) + 2)
            new_geom.moveTop(((thumbnail_geom.height() - 4) / 2 - new_height / 2) + 2)
            new_geom.setWidth(new_width)
            new_geom.setHeight(new_height)
            thumbnail_geom = new_geom

        self._ui.thumbnail.setScaledContents(scale_contents)
        self._ui.thumbnail.setGeometry(thumbnail_geom)

        # now update buttons based on current thumbnail:
        if not self._btns_transition_anim or self._btns_transition_anim.state() == QAbstractAnimation.Stopped:
            if self.thumbnail or not self._are_any_btns_enabled():
                self._ui.buttons_frame.hide()
                self._btns_visibility = 0.0
            else:
                self._ui.buttons_frame.show()
                self._btns_visibility = 1.0

    def _safe_get_dialog(self):
        """
        Get the widgets dialog parent.

        just call self.window() but this is unstable in Nuke
        Previously this would
        causing a crash on exit - suspect that it's caching
        something internally which then doesn't get cleaned
        up properly...
        """
        current_widget = self
        while current_widget:
            if isinstance(current_widget, QDialog):
                return current_widget
            current_widget = current_widget.parentWidget()
        return None

    def _on_screenshot(self):
        """
        Perform the actual screenshot
        """
        # hide the containing window - we can't actuall hide
        # the window as this will break modality!  Instead
        # we have to move the window off the screen:
        win = self._safe_get_dialog()

        win_geom = None
        if win:
            win_geom = win.geometry()
            win.setGeometry(1000000, 1000000, win_geom.width(), win_geom.height())
            # make sure this event is processed:
            QCoreApplication.processEvents()
            QCoreApplication.sendPostedEvents(None, 0)
            QCoreApplication.flush()
        try:
            # get temporary file to use:
            # to be cross-platform and python 2.5 compliant, we can't use
            # tempfile.NamedTemporaryFile with delete=False.  Instead, we
            # use tempfile.mkstemp which does practically the same thing!
            # tf, path = tempfile.mkstemp(suffix=".png", prefix="tanktmp")
            # if tf:
            #     os.close(tf)
            pm_map = screen_grab.screen_capture()
        finally:
            # restore the window:
            if win:
                win.setGeometry(win_geom)
                QCoreApplication.processEvents()
        return pm_map

    def _on_thumbnail_changed(self):
        if self.parent():
            self.parent().show()
        else:
            self.show()


class ScreenShotButton(dy.MToolButton):
    """A Clickable and draggable tool button to upload files"""
    sig_file_changed = Signal(str)
    sig_files_changed = Signal(list)
    slot_browser_file = ""

    def __init__(self, text='', multiple=False, parent=None):
        super(ScreenShotButton, self).__init__(parent=parent)
        self.setAcceptDrops(True)
        self.setMouseTracking(True)
        self.text_under_icon()
        self.setText(text)

        self.set_dayu_size(60)
        self.set_dayu_svg('media_line.svg')
        self.setIconSize(QSize(60, 60))

        # self.clicked.connect(self.slot_browser_file)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setToolTip(self.tr('Click to browser file'))

        self._path = None
        self._multiple = multiple
        self._filters = []

    def get_dayu_filters(self):
        """
        Get browser's format filters
        :return: list
        """
        return self._filters

    def set_dayu_filters(self, value):
        """
        Set browser file format filters
        :param value:
        :return: None
        """
        self._filters = value

    def get_dayu_path(self):
        """
        Get last browser file path
        :return: str
        """
        return self._path

    def set_dayu_path(self, value):
        """
        Set browser file start path
        :param value: str
        :return: None
        """
        self._path = value

    def get_dayu_multiple(self):
        """
        Get browser can select multiple file or not
        :return: bool
        """
        return self._multiple

    def set_dayu_multiple(self, value):
        """
        Set browser can select multiple file or not
        :param value: bool
        :return: None
        """
        self._multiple = value

    dayu_multiple = Property(bool, get_dayu_multiple, set_dayu_multiple)
    dayu_path = Property(basestring, get_dayu_path, set_dayu_path)
    dayu_filters = Property(list, get_dayu_filters, set_dayu_filters)

    def dragEnterEvent(self, event):
        """Override dragEnterEvent. Validate dragged files"""
        if event.mimeData().hasFormat("text/uri-list"):
            file_list = self._get_valid_file_list(event.mimeData().urls())
            count = len(file_list)
            if count == 1 or (count > 1 and self.get_dayu_multiple()):
                event.acceptProposedAction()
                return

    def dropEvent(self, event):
        """Override dropEvent to accept the dropped files"""
        file_list = self._get_valid_file_list(event.mimeData().urls())
        if self.get_dayu_multiple():
            self.sig_files_changed.emit(file_list)
            self.set_dayu_path(file_list)
        else:
            self.sig_file_changed.emit(file_list[0])
            self.set_dayu_path(file_list[0])

    def _get_valid_file_list(self, url_list):
        import subprocess
        import sys
        file_list = []
        for url in url_list:
            file_name = url.toLocalFile()
            if sys.platform == 'darwin':
                sub_process = subprocess.Popen(
                    'osascript -e \'get posix path of posix file \"file://{}\" -- kthxbai\''.format(
                        file_name),
                    stdout=subprocess.PIPE,
                    shell=True)
                # print sub_process.communicate()[0].strip()
                file_name = sub_process.communicate()[0].strip()
                sub_process.wait()

            if os.path.isfile(file_name):
                if self.property('format'):
                    if os.path.splitext(file_name)[-1] in self.property('format'):
                        file_list.append(file_name)
                else:
                    file_list.append(file_name)

        return file_list