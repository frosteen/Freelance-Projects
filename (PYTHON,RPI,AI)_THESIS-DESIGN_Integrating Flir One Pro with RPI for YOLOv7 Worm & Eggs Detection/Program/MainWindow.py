import os
import sys
from datetime import datetime

import cv2
from imutils.video import VideoStream
from PyQt5 import QtCore, QtGui, QtWidgets, uic


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
        self.Frame.setVisible(True)
        self.Captured.setVisible(False)
        self.Next.setVisible(False)
        self.Predict.setVisible(False)

        # capture button
        self.CaptureButton.clicked.connect(self.capture_button)
        self.Next.clicked.connect(self.next_clicked)
        self.Predict.clicked.connect(self.predict_clicked)

        # start camera
        self.start_camera("Frame")

    def capture_button(self):
        cap_button_text = str(self.CaptureButton.text())

        if cap_button_text == "CAPTURE":
            self.Frame.setVisible(False)
            self.Captured.setVisible(True)
            self.CaptureButton.setVisible(False)
            self.Next.setVisible(True)
            self.Predict.setVisible(True)

            self.dt_string = datetime.now().strftime("%d%m%Y%H%M%S")
            self.image_path = f"Captured/Captured-{self.dt_string}.png"

            # save image
            cv2.imwrite(self.image_path, self.frame)

            # display image
            self.__display_frames(self.frame, "Captured")
        else:
            self.next_clicked()

    def next_clicked(self):
        self.CaptureButton.setText("CAPTURE")
        self.Frame.setVisible(True)
        self.Captured.setVisible(False)
        self.CaptureButton.setVisible(True)
        self.Next.setVisible(False)
        self.Predict.setVisible(False)

    def predict_clicked(self):
        self.CaptureButton.setText("NEXT")
        self.Frame.setVisible(False)
        self.Captured.setVisible(True)
        self.CaptureButton.setVisible(True)
        self.Next.setVisible(False)
        self.Predict.setVisible(False)

        # detect YOLOv7
        os.system(
            f"cd /home/pi/yolov7 && python detect.py --weights /home/pi/Program/best.pt --source /home/pi/Program/{self.image_path} --conf 0.25 --name /home/pi/Program/Predicted/ --exist-ok --no-trace"
        )

        # display resulting image
        self.predicted_image = cv2.imread(f"Predicted/Captured-{self.dt_string}.png")
        self.__display_frames(self.predicted_image, "Captured")

    # Camera Start #

    def start_camera(self, label_name):
        self.capture = VideoStream(src=3, usePiCamera=False).start()
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
        new_height = int(self.frame.shape[0] * 0.75)
        self.frame = self.frame[0:new_height, 0 : self.frame.shape[1]]
        self.frame = cv2.resize(self.frame, (640, 480), interpolation=cv2.INTER_LINEAR)
        self.frame = cv2.flip(self.frame, 1)
        # self.frame = cv2.fastNlMeansDenoisingColored(self.frame,None,10,10,7,21) # remove noise (slow)
        self.__display_frames(self.frame, label_name)

    def __display_frames(self, frame, label_name=None):
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
