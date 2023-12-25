import sys
import os
import cv2
import numpy as np
from PyQt5 import QtWidgets, QtGui, QtCore, uic

directory = os.getcwd()


class DoThreading(QtCore.QThread):
    def __init__(self, _func, _finished_func=None):
        QtCore.QThread.__init__(self)
        self.func = _func
        self.daemon = True
        self.finished_func = _finished_func
        if self.finished_func is not None:
            self.finished.connect(_finished_func)

    def __del__(self):
        self.wait()

    def run(self):
        self.func()


class VideoThread(QtCore.QThread):
    change_pixmap_signal = QtCore.pyqtSignal(np.ndarray)

    def __init__(self, label):
        super().__init__()
        self.label = label
        self._run_flag = True
        self.cv_img = None
        self.rgb_image = None
        self.qt_img = None
        self.change_pixmap_signal.connect(self.update_image)

    def run(self):
        # capture from web cam
        cap = cv2.VideoCapture(0)
        while self._run_flag:
            ret, self.cv_img = cap.read()
            if ret:
                self.cv_img = cv2.flip(self.cv_img, 1)
                self.change_pixmap_signal.emit(self.cv_img)
        # shut down capture system
        cap.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()

    @QtCore.pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        self.qt_img = self.convert_cv_qt(cv_img)
        self.label.setPixmap(self.qt_img)

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        self.rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = self.rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(
            self.rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888
        )
        return QtGui.QPixmap.fromImage(convert_to_Qt_format)


class Window(QtWidgets.QMainWindow):
    def __init__(self, ui):
        super().__init__()
        uic.loadUi(directory + "/" + ui, self)

    # def closeEvent(self, event):
    #     close = QtWidgets.QMessageBox.question(self,
    #                                            "QUIT",
    #                                            "Are you sure want to quit?",
    #                                            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
    #     if close == QtWidgets.QMessageBox.Yes:
    #         event.accept()
    #     else:
    #         event.ignore()

    def center(self):
        frame_gm = self.frameGeometry()
        screen = QtWidgets.QApplication.desktop().screenNumber(
            QtWidgets.QApplication.desktop().cursor().pos()
        )
        center_point = QtWidgets.QApplication.desktop().screenGeometry(screen).center()
        frame_gm.moveCenter(center_point)
        self.move(frame_gm.topLeft())


class MainWindow(Window):
    def __init__(self):
        super().__init__("MainWindow.ui")
        self.setFixedSize(self.size())
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.center()
        self.show()

        self.red_rectangle.hide()

        self.pushButtonCapture.clicked.connect(self.pushButtonCapture_clicked)

        # create the video capture thread
        self.VideoThread = VideoThread(self.Image)
        # start the thread
        self.VideoThread.start()

    def image_process(self, image):
        self.captured_imge = image

        # Image Processing

    def pushButtonCapture_clicked(self):
        self.rgb_image = self.VideoThread.rgb_image
        self.qt_img = self.VideoThread.qt_img
        if self.rgb_image is not None and self.qt_img is not None:
            self.CapturedImage.setPixmap(self.qt_img)
            self.image_process(self.rgb_image)


class Tools:
    @staticmethod
    def do_message(object, title="Info", text=None):
        msg = QtWidgets.QMessageBox(object)
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.show()
        return msg

    @staticmethod
    def do_get_question(object, title="Question", text=None):
        return QtWidgets.QMessageBox.question(
            object,
            title,
            text,
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No,
        )

    @staticmethod
    def do_get_item(object, title="Input", label=None, items=None):
        inputted, ok_pressed = QtWidgets.QInputDialog.getItem(
            object, title, label, items, 0, False
        )
        index = items.index(inputted)
        if inputted and ok_pressed:
            return inputted, index
        else:
            return None, None


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    app.exec_()
