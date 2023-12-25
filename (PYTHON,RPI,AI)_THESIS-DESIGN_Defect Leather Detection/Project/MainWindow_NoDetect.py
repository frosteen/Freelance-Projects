import os
import sys
from datetime import datetime

import cv2
import torch
from imutils.video import VideoStream
from PyQt5 import QtCore, QtGui, QtWidgets, uic

# Model
model = torch.hub.load("yolov5", "custom", path="best.pt", source="local")  # local repo


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

    def center(self):
        qtRectangle = self.frameGeometry()
        centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())


class MainWindow(Window):
    def __init__(self, ui_path):
        super().__init__()
        uic.loadUi(ui_path, self)
        self.setFixedSize(self.size())
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.center()
        self.show()

        # capture button
        self.CaptureButton.clicked.connect(self.capture_button)

        # start camera
        self.start_camera("Frame")

    def capture_button(self):
        capture_button_txt = str(self.CaptureButton.text())

        if capture_button_txt == "CAPTURE":
            self.CaptureButton.setText("NEXT")
            self.stop_camera()

            dt_string = datetime.now().strftime("%d%m%Y%H%M%S")
            image_path = f"Captured/Captured-{dt_string}.png"

            # # detect
            # frame_to_rgb = cv2.cvtColor(
            #     self.frame, cv2.COLOR_BGR2RGB
            # )  # Must convert to RGB before inputting to the model
            # results = model(frame_to_rgb)
            # results_df = results.pandas().xyxy[0]
            # results_to_bgr = cv2.cvtColor(results.render()[0], cv2.COLOR_RGB2BGR)

            # # print results in terminal
            # print(results_df.name.value_counts())

            # show resulting image
            self.__display_frames(self.frame, 1, "Frame")

            # save image
            cv2.imwrite(image_path, self.frame)
        else:
            self.CaptureButton.setText("CAPTURE")
            self.start_camera("Frame")

    # Camera Start #

    def start_camera(self, label_name):
        if os.name == "nt":  # check if running on windows
            self.capture = VideoStream(usePiCamera=False).start()
        else:  # else run with pi camera
            self.capture = VideoStream(
                usePiCamera=True, resolution=(1000, 1000)
            ).start()
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(lambda: self.__update_frame(label_name))
        self.timer.start()

    def stop_camera(self):
        self.capture.stop()
        self.timer.stop()

    def __update_frame(self, label_name):
        self.frame = self.capture.read()
        if self.frame is None:
            return
        self.frame = cv2.flip(self.frame, 1)
        self.__display_frames(self.frame, 1, label_name)

    def __display_frames(self, frame, window=1, label_name=None):
        self.out_frame = QtGui.QImage(
            frame,
            frame.shape[1],
            frame.shape[0],
            frame.strides[0],
            QtGui.QImage.Format_RGB888,
        )
        self.out_frame = self.out_frame.rgbSwapped()
        self.out_frame = QtGui.QPixmap.fromImage(self.out_frame)
        lbl = self.findChild(QtWidgets.QLabel, label_name)
        self.out_frame = self.out_frame.scaled(
            lbl.width(), lbl.height(), QtCore.Qt.KeepAspectRatio
        )
        lbl.setPixmap(self.out_frame)

    # Camera end #


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow("MainWindow.ui")
    app.exec_()
