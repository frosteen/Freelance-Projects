#!/usr/bin/python3

import io
import os
import sys
import time
from datetime import datetime

import cv2
import numpy as np
import pygame
import RPi.GPIO as GPIO
from picamera import PiCamera
from picamera.array import PiRGBArray
from PyQt5 import QtCore, QtGui, QtWidgets, uic

from ImageProcessing import PesoImage
from PesoScanner import peso_scanner
from PesoValue import calculate_peso_value

path = "/home/pi/Desktop/Project"


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

    def __init__(self, label, canny_edge_threshold1, canny_edge_threshold2):
        super().__init__()
        self.label = label
        self.canny_edge_threshold1 = canny_edge_threshold1
        self.canny_edge_threshold2 = canny_edge_threshold2
        self._run_flag = True
        self.orig_cv_img = None
        self.cv_img = None
        self.rgb_image = None
        self.qt_img = None
        self.change_pixmap_signal.connect(self.update_image)

    def run(self):
        # capture from picamera via io stream
        camera = PiCamera()
        camera.resolution = (820, 616)
        stream = io.BytesIO()  # stream via buffer to resolve memory issue
        while 1:
            for _ in camera.capture_continuous(
                stream, format="png"
            ):  # png is better than jpg
                if self._run_flag:
                    data = np.frombuffer(stream.getvalue(), dtype=np.uint8)

                    self.orig_cv_img = cv2.imdecode(data, 1)

                    X, Y = 160, 66  # Resolution of Philippine Peso

                    self.H, self.W = self.orig_cv_img.shape[:2]

                    # resize with same aspect ratio of red_rectangle
                    self.cv_img = peso_scanner(
                        self.orig_cv_img,
                        int(self.W),
                        int(Y * self.W / X),
                        int(self.canny_edge_threshold1.value()),
                        int(self.canny_edge_threshold2.value()),
                        0,
                    )

                    # print(int(self.canny_edge_threshold1.value()))
                    # print(int(self.canny_edge_threshold2.value()))

                    self.change_pixmap_signal.emit(self.cv_img)
                    stream.truncate()
                    stream.seek(0)

    def stop(self):
        self.wait()

    def pause(self):
        self._run_flag = False

    def go(self):
        self._run_flag = True

    @QtCore.pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        self.qt_img = self.convert_cv_qt(cv_img)
        self.qt_img = self.qt_img.scaled(
            self.label.width(), self.label.height(), QtCore.Qt.KeepAspectRatio
        )
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
        uic.loadUi(path + "/" + ui, self)

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

        # set value thresholds
        self.canny_edge_threshold1.setValue(120)
        self.canny_edge_threshold2.setValue(0)

        # hide red_rectangle
        self.red_rectangle.hide()

        # hide Image_2
        self.Image_2.hide()

        # Event handling
        self.pushButtonCapture.clicked.connect(self.pushButtonCapture_clicked)

        # initiate audio
        pygame.mixer.init()

        # GPIO setup
        self.button_pin = 21
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # create the video capture thread
        self.VideoThread = VideoThread(
            self.Image, self.canny_edge_threshold1, self.canny_edge_threshold2
        )
        self.VideoThread.start()

        # detect hardware button press
        self.check_hardware_button_thread = DoThreading(self.check_hardware_button)
        self.check_hardware_button_thread.start()

        self.next_counter = 0

    def check_hardware_button(self):
        try:
            while 1:
                pin = GPIO.input(self.button_pin)
                if pin == 0:
                    self.pushButtonCapture_clicked()

        finally:
            GPIO.cleanup()

    def closeEvent(self, event):
        self.VideoThread.stop()
        del self.check_hardware_button_thread

    def pushButtonCapture_clicked(self):
        if str(self.pushButtonCapture.text()) == "Capture":
            self.VideoThread.pause()
            self.cv_img = self.VideoThread.cv_img
            self.qt_img = self.VideoThread.qt_img
            self.date = datetime.now().strftime("%d.%m.%Y_%H.%M.%S")
            self.image_path = path + "/Pictures/Captured/" + self.date
            if self.cv_img is not None and self.qt_img is not None:
                os.mkdir(self.image_path)
                self.counterfeit_detection()
                self.pushButtonCapture.setText("Next")
                self.Image_2.show()
        elif str(self.pushButtonCapture.text()) == "Next":

            files = [
                self.image_path + "/WaterMark.png",
                self.image_path + "/SecurityThread.png",
                self.image_path + "/SeeThroughPrint.png",
                self.image_path + "/SerialNumber.png",
            ]

            if self.next_counter == len(files):
                self.pushButtonCapture.setText("Capture")
                self.Image_2.hide()
                self.VideoThread.go()
                self.next_counter = 0
            else:
                self.qt_img = QtGui.QPixmap(files[self.next_counter])
                self.qt_img = self.qt_img.scaled(
                    self.Image_2.width(),
                    self.Image_2.height(),
                    QtCore.Qt.KeepAspectRatio,
                )
                self.Image_2.setPixmap(self.qt_img)
                self.next_counter += 1

    def counterfeit_detection(self):

        cv2.imwrite(self.image_path + "/Original.png", self.cv_img)

        get_peso_value = calculate_peso_value(
            self.cv_img, rtol=0.20
        )  # get value using kmeans algorithm

        self.label_status.setText("Successfully captured. Processing Peso image...")

        if get_peso_value is not None:
            self.label_peso_value.setText("Peso Value: {}".format(get_peso_value))

        Image = PesoImage(
            self.cv_img,
            water_mark_path=path + "/Pictures/WaterMark",
            baybayin_path=path + "/Pictures/Baybayin",
        )

        image, is_detected_WaterMark, startX, startY, endX, endY = Image.WaterMark()
        cv2.imwrite(self.image_path + "/WaterMark.png", image)

        image, is_detected_SecurityThread = Image.SecurityThread()
        cv2.imwrite(self.image_path + "/SecurityThread.png", image)

        (
            image,
            is_detected_SeeThroughPrint,
            startX2,
            startY2,
            endX2,
            endY2,
        ) = Image.SeeThroughPrint()
        cv2.imwrite(self.image_path + "/SeeThroughPrint.png", image)

        image, is_detected_SerialNumber = Image.SerialNumber()
        cv2.imwrite(self.image_path + "/SerialNumber.png", image)

        r, is_peso = Image.CalculateR()

        if is_peso:
            print("PESO", r)

            # check the 4 features
            if (
                is_detected_WaterMark
                and is_detected_SecurityThread
                and is_detected_SeeThroughPrint
                and is_detected_SerialNumber
            ):
                print("AUTHENTIC")
                if get_peso_value is not None:
                    print("Peso Value: {}\n".format(get_peso_value))
                MainWindow.play_sound_peso_value(get_peso_value)
                time.sleep(2)
                MainWindow.play_sound_authentic()
                with open(self.image_path + "/Output.txt", "w+") as file:
                    file.write("Detected Water Mark: true\n")
                    file.write("Detected Security Thread: true\n")
                    file.write("Detected See Through Print: true\n")
                    file.write("Detected Serial Number: true\n")
                    if get_peso_value is not None:
                        file.write("Peso Value: {}\n".format(get_peso_value))
                    file.write("Final: Authentic\n")
            else:
                print("FAKE")
                if get_peso_value is not None:
                    print("Peso Value: {}\n".format(get_peso_value))
                MainWindow.play_sound_peso_value(get_peso_value)
                time.sleep(2)
                MainWindow.play_sound_fake()
                with open(self.image_path + "/Output.txt", "w+") as file:
                    if is_detected_WaterMark:
                        file.write("Detected Water Mark: true\n")
                    else:
                        file.write("Detected Water Mark: false\n")
                    if is_detected_SecurityThread:
                        file.write("Detected Security Thread: true\n")
                    else:
                        file.write("Detected Security Thread: false\n")
                    if is_detected_SeeThroughPrint:
                        file.write("Detected See Through Print: true\n")
                    else:
                        file.write("Detected See Through Print: false\n")
                    if is_detected_SerialNumber:
                        file.write("Detected Serial Number: true\n")
                    else:
                        file.write("Detected Serial Number: false\n")
                    if get_peso_value is not None:
                        file.write("Peso Value: {}\n".format(get_peso_value))
                    file.write("Final: Fake\n")

            self.h, self.w, self.c = self.cv_img.shape

            if is_detected_WaterMark:
                cv2.rectangle(
                    self.cv_img, (startX, startY), (endX, endY), (0, 255, 0), 3
                )

            if is_detected_SecurityThread:
                cv2.rectangle(
                    self.cv_img,
                    (int(self.w * 0.60), 0),
                    (int(self.w * 0.65), self.h),
                    (0, 255, 0),
                    3,
                )

            if is_detected_SeeThroughPrint:
                cv2.rectangle(
                    self.cv_img, (startX2, startY2), (endX2, endY2), (0, 255, 0), 3
                )

            if is_detected_SerialNumber:
                cv2.rectangle(
                    self.cv_img,
                    (int(self.w * 0.025), int(self.h * 0.700)),
                    (int(self.w * 0.225), int(self.h * 0.90)),
                    (0, 255, 0),
                    3,
                )

            self.qt_img = self.VideoThread.convert_cv_qt(self.cv_img)
            self.qt_img = self.qt_img.scaled(
                self.Image_2.width(), self.Image_2.height(), QtCore.Qt.KeepAspectRatio
            )
            self.Image_2.setPixmap(self.qt_img)

        else:
            print("Not PESO", r)

        self.show_Image_2(self.cv_img)

        self.label_status.setText("Place the Peso")

    def show_Image_2(self, image):
        self.qt_img = self.VideoThread.convert_cv_qt(image)
        self.qt_img = self.qt_img.scaled(
            self.Image_2.width(), self.Image_2.height(), QtCore.Qt.KeepAspectRatio
        )
        self.Image_2.setPixmap(self.qt_img)

    @staticmethod
    def play_sound_fake():
        pygame.mixer.music.load(path + "/Sounds/FAKE.mp3")
        pygame.mixer.music.play()

    @staticmethod
    def play_sound_authentic():
        pygame.mixer.music.load(path + "/Sounds/AUTHENTIC.mp3")
        pygame.mixer.music.play()

    @staticmethod
    def play_sound_peso_value(peso_value):
        if peso_value is not None:
            pygame.mixer.music.load(path + "/Sounds/{}.mp3".format(peso_value))
            pygame.mixer.music.play()


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
