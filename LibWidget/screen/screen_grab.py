# -*- coding: utf-8 -*-
import tempfile
import sys
import os
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *


class ScreenGrabber(QDialog):
    """
    A transparent tool dialog for selecting an area (QRect) on the screen.

    This tool does not by itself perform a screen capture. The resulting
    capture rect can be used (e.g. with the get_desktop_pixmap function) to
    blit the selected portion of the screen into a pixmap.
    """
    def __init__(self, parent=None):
        """
        Constructor
        """
        super(ScreenGrabber, self).__init__(parent)

        self._opacity = 1
        self._click_pos = None
        self._capture_rect = QRect()

        self.setWindowFlags(Qt.FramelessWindowHint |
                            Qt.WindowStaysOnTopHint |
                            Qt.CustomizeWindowHint |
                            Qt.Tool)

        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setCursor(Qt.CrossCursor)
        self.setMouseTracking(True)

        desktop = QApplication.instance().desktop()
        desktop.resized.connect(self._fit_screen_geometry)
        desktop.screenCountChanged.connect(self._fit_screen_geometry)

    @property
    def capture_rect(self):
        """
        The resulting QRect from a previous capture operation.
        """
        return self._capture_rect

    def paintEvent(self, event):
        """
        Paint event
        """
        # Convert click and current mouse positions to local space.
        mouse_pos = self.mapFromGlobal(QCursor.pos())
        click_pos = None
        if self._click_pos is not None:
            click_pos = self.mapFromGlobal(self._click_pos)

        painter = QPainter(self)

        # Draw background. Aside from aesthetics, this makes the full
        # tool region accept mouse events.
        painter.setBrush(QColor(0, 0, 0, self._opacity))
        painter.setPen(Qt.NoPen)
        painter.drawRect(event.rect())

        # Clear the capture area
        if click_pos is not None:
            capture_rect = QRect(click_pos, mouse_pos)
            painter.setCompositionMode(QPainter.CompositionMode_Clear)
            painter.drawRect(capture_rect)
            painter.setCompositionMode(QPainter.CompositionMode_SourceOver)

        pen = QPen(QColor(255, 255, 255, 64), 1, Qt.DotLine)
        painter.setPen(pen)

        # Draw cropping markers at click position
        if click_pos is not None:
            painter.drawLine(event.rect().left(), click_pos.y(),
                             event.rect().right(), click_pos.y())
            painter.drawLine(click_pos.x(), event.rect().top(),
                             click_pos.x(), event.rect().bottom())

        # Draw cropping markers at current mouse position
        painter.drawLine(event.rect().left(), mouse_pos.y(),
                         event.rect().right(), mouse_pos.y())
        painter.drawLine(mouse_pos.x(), event.rect().top(),
                         mouse_pos.x(), event.rect().bottom())

    def keyPressEvent(self, event):
        """
        Key press event
        """
        # for some reason I am not totally sure about, it looks like
        # pressing escape while this dialog is active crashes Maya.
        # I tried subclassing closeEvent, but it looks like the crashing
        # is triggered before the code reaches this point.
        # by sealing the keypress event and not allowing any further processing
        # of the escape key (or any other key for that matter), the
        # behaviour can be successfully avoided.

        # TODO: See if we can get the behacior with hitting escape back
        # maybe by manually handling the closing of the window? I tried
        # some obvious things and weren't successful, but didn't dig very
        # deep as it felt like a nice-to-have and not a massive priority.
        pass

    def mousePressEvent(self, event):
        """
        Mouse click event
        """
        if event.button() == Qt.LeftButton:
            # Begin click drag operation
            self._click_pos = event.globalPos()

    def mouseReleaseEvent(self, event):
        """
        Mouse release event
        """
        if event.button() == Qt.LeftButton and self._click_pos is not None:
            # End click drag operation and commit the current capture rect
            self._capture_rect = QRect(self._click_pos,
                                       event.globalPos()).normalized()
            self._click_pos = None
        self.close()

    def mouseMoveEvent(self, event):
        """
        Mouse move event
        """
        self.repaint()

    def showEvent(self, event):
        """
        Show event
        """
        self._fit_screen_geometry()
        # Start fade in animation
        fade_anim = QPropertyAnimation(self, "_opacity_anim_prop", self)
        fade_anim.setStartValue(self._opacity)
        fade_anim.setEndValue(127)
        fade_anim.setDuration(300)
        fade_anim.setEasingCurve(QEasingCurve.OutCubic)
        fade_anim.start(QAbstractAnimation.DeleteWhenStopped)

    def _set_opacity(self, value):
        """
        Animation callback for opacity
        """
        self._opacity = value
        self.repaint()

    def _get_opacity(self):
        """
        Animation callback for opacity
        """
        return self._opacity

    _opacity_anim_prop = Property(int, _get_opacity, _set_opacity)

    def _fit_screen_geometry(self):
        # Compute the union of all screen geometries, and resize to fit.
        desktop = QApplication.instance().desktop()
        workspace_rect = QRect()
        for i in range(desktop.screenCount()):
            workspace_rect = workspace_rect.united(desktop.screenGeometry(i))
        self.setGeometry(workspace_rect)


class ExternalCaptureThread(QThread):
    """
    Wrap external screenshot call in a thread just to be on the safe side!
    This helps avoid the os thinking the application has hung for
    certain applications (e.g. Softimage on Windows)
    """
    def __init__(self, path):
        """
        :param path: Path to write the screenshot to
        """
        QThread.__init__(self)
        self._path = path
        self._error = None

    @property
    def error_message(self):
        """
        Error message generated during capture, None if success
        """
        return self._error

    def run(self):
        try:
            if sys.platform == "darwin":
                # use built-in screenshot command on the mac
                ret_code = os.system("screencapture -m -i -s %s" % self._path)
                if ret_code != 0:
                    raise Exception("Screen capture tool returned error code %s" % ret_code)

            elif sys.platform == "linux2":
                # use image magick
                ret_code = os.system("import %s" % self._path)
                if ret_code != 0:
                    raise Exception("Screen capture tool returned error code %s. "
                                         "For screen capture to work on Linux, you need to have "
                                         "the imagemagick 'import' executable installed and "
                                         "in your PATH." % ret_code)

            else:
                raise Exception("Unsupported platform.")
        except Exception, e:
            self._error = str(e)


def _external_screenshot():
    """
    Use an external approach for grabbing a screenshot.
    Linux and macosx support only.

    :returns: Captured image
    :rtype: :class:`~PySide.QPixmap`
    """
    output_path = tempfile.NamedTemporaryFile(suffix=".png",
                                              prefix="screencapture_",
                                              delete=False).name

    pm = None
    try:
        # do screenshot with thread so we don't block anything
        screenshot_thread = ExternalCaptureThread(output_path)
        screenshot_thread.start()
        while not screenshot_thread.isFinished():
            screenshot_thread.wait(100)
            QApplication.processEvents()

        if screenshot_thread.error_message:
            raise Exception("Failed to capture "
                                 "screenshot: %s" % screenshot_thread.error_message)

        # load into pixmap:
        pm = QPixmap(output_path)
    finally:
        # remove the temporary file
        if output_path and os.path.exists(output_path):
            os.remove(output_path)

    return pm


def get_desktop_pixmap(rect):
    """
    Performs a screen capture on the specified rectangle.

    :param rect: Rectangle to capture
    :type rect: :class:`~PySide.QRect`
    :returns: Captured image
    :rtype: :class:`~PySide.QPixmap`
    """
    desktop = QApplication.instance().desktop()
    return QPixmap.grabWindow(desktop.winId(), rect.x(), rect.y(),
                                    rect.width(), rect.height())


def screen_capture():
    """
    Modally displays the screen capture tool.

    :returns: Captured screen
    :rtype: :class:`~PySide.QPixmap`
    """

    if sys.platform in ["linux2", "darwin"]:
        # there are known issues with the QT based screen grabbing
        # on linux - some distros don't have a X11 compositing manager
        # so transparent windows aren't supported. With macosx there
        # are known issues with some multi-diplay setups. In both
        # these cases, fall back onto a traditional approach where
        # an external application is used to grab the screenshot.
        return _external_screenshot()
    else:
        tool = ScreenGrabber()
        tool.exec_()
        return get_desktop_pixmap(tool.capture_rect)


def screen_capture_file(output_path=None):
    """
    Modally display the screen capture tool, saving to a file.

    :param output_path: Path to save to. If no path is specified,
                        a temp path is generated.
    :returns: path where screenshot was saved.
    """

    if output_path is None:
        output_path = tempfile.NamedTemporaryFile(suffix=".png",
                                                  prefix="screencapture_",
                                                  delete=False).name
    pixmap = screen_capture()
    pixmap.save(output_path)
    return output_path


if __name__ == "__main__":
    pass
