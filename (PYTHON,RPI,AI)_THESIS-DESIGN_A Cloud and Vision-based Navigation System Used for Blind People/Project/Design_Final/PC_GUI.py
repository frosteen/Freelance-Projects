import os
import sys

from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5_Dependencies.QTThreading import DoThreading
from PyQt5_Dependencies.CustomQtWidgets import CustomQtWidgets

import pyrebase
import torch
import cv2
import num2words
from collections import Counter
from datetime import datetime

main_path = "PyQt5_Dependencies"


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

    def closeEvent(self, event):
        is_close = CustomQtWidgets.do_get_question(
            self, "Quit", "Are you sure want to quit?"
        )

        if is_close:
            event.accept()
        else:
            event.ignore()

    def center(self):
        qtRectangle = self.frameGeometry()
        centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())


class MainWindow(Window):
    def __init__(self, ui_path, db, storage, model):
        super().__init__()
        uic.loadUi(os.path.join(main_path, ui_path), self)
        self.setFixedSize(self.size())
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.center()
        self.show()
        self.db = db
        self.storage = storage
        self.model = model
        self.main_thread = DoThreading(self.main)
        self.main_thread.start()
        self.last_distance = None
        self.messages = []

    def capture(self, frame, directory, name):
        dt_string = datetime.now().strftime("%d.%m.%Y %H.%M.%S")
        image_path = os.path.join(directory, f"Captured-{name}-{dt_string}.jpg")
        cv2.imwrite(image_path, frame)

    def check_location(self, image, center):
        h, w, _ = image.shape
        positions = []
        if center[1] > int(h * 0.75):
            positions.append("bottom")
        if center[1] < int(h * 0.25):
            positions.append("top")
        if center[0] > int(w * 0.75):
            positions.append("right")
        if center[0] < int(w * 0.25):
            positions.append("left")
        if (
            center[1] < int(h * 0.75)
            and center[1] > int(h * 0.25)
            and center[0] < int(w * 0.75)
            and center[0] > int(w * 0.25)
        ):
            positions.append("center")
        return positions

    def create_sentence(self, class_name_location):
        dt_string = datetime.now().strftime("%d.%m.%Y %H.%M.%S")
        print(f"\n{dt_string}")
        sentence = "I see"
        for key, value in class_name_location.items():
            sentence += f" {num2words.num2words(value)} {key}"

        print(sentence)
        print("____________________________________")

        return sentence

    def format_text_distance(self, get_distance):
        dt_string = datetime.now().strftime("%d.%m.%Y %H.%M.%S")
        message = f"{dt_string}\nIn {get_distance} cm Object detected."
        print(message)
        return message

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

    def stream_handler(self, message):
        get_distance = message["data"]
        distance_message = self.format_text_distance(get_distance)
        if self.last_distance != get_distance:
            if len(self.messages) >= 4:
                self.messages.pop(0)
            self.messages.append(distance_message)

        self.Distance_Label.setText("\n".join(self.messages))
        self.last_distance = get_distance

    def main(self):
        self.db.child("distance").stream(self.stream_handler)
        while True:
            execute_status = self.db.child("Execute").get().val()
            if execute_status == True:
                self.db.child("is_processing").set(True)
                self.storage.child("cur_image.png").download(
                    "cur_image.png", "cur_image.png"
                )
                frame = cv2.imread("cur_image.png")

                frame_to_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = self.model(frame_to_rgb)
                results_df = results.pandas().xyxy[0]
                frame = cv2.cvtColor(results.render()[0], cv2.COLOR_RGB2BGR)

                class_name_location = []
                for _, values in results_df.iterrows():
                    center = (
                        int((values[0] + values[2]) / 2),
                        int((values[1] + values[3]) / 2),
                    )
                    class_name_location.append(
                        "-".join(self.check_location(frame, center) + [values[6]])
                    )

                output_sentence = self.create_sentence(
                    dict(Counter(class_name_location))
                )

                self.db.child("Sentence").set(output_sentence)
                self.db.child("Execute").set(False)

                self.__display_frames(frame, label_name="Image")
                self.Sentence_Label.setText(output_sentence)
                self.capture(frame, "Capture", "YOLOv5")


if __name__ == "__main__":
    config = {
        "apiKey": "AIzaSyBz6KVh7zrUWtXKXh9RtR-mLBU5EPIv0qY",
        "authDomain": "guide-blind-people.firebaseapp.com",
        "databaseURL": "https://guide-blind-people-default-rtdb.firebaseio.com",
        "storageBucket": "guide-blind-people.appspot.com",
    }
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    storage = firebase.storage()
    db.child("Execute").set(True)
    model = torch.hub.load("ultralytics/yolov5", "yolov5x", force_reload=True)
    model.conf = 0.5  # set threshold
    if torch.cuda.is_available():
        model.cuda()
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow("MainWindow.ui", db, storage, model)
    app.exec_()
