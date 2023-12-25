import os
import warnings
from datetime import datetime

import cv2
import torch

from Count import Count
from FrameLabel import frame_label
from ReadWriteCSV import write_csv_dict
from RunEvery import RunEvery


class Cherry_Detect_YOLOv5:
    def __init__(
        self,
        custom_model_path="best_640x480_stretch.pt",
        logs_path="Logs",
        logging_interval=5,
        yolov5_force_reload=True,
    ):
        warnings.filterwarnings(
            "ignore", category=UserWarning
        )  # supress annoying warnings

        # create custom yolov5 model
        self.model = torch.hub.load(
            "ultralytics/yolov5",
            "custom",
            path=custom_model_path,
            force_reload=yolov5_force_reload,
        )
        self.model.conf = 0.85

        # create cherry objects
        self.cherry_flare_s8 = Count("s8")
        self.cherry_aqua_s9 = Count("s9")

        # initiate logging
        if not os.path.isdir(logs_path):
            os.mkdir(logs_path)
        dt_string_log = datetime.now().strftime("%d%m%Y%H%M%S")
        self.log_path = os.path.join(logs_path, "Logs_{}.csv".format(dt_string_log))

        # logging interval
        self.logging_interval = RunEvery(logging_interval)  # seconds

    def __do_csv_logs(self):
        dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        logs = {
            "Overall Cherry Flare S8": self.cherry_flare_s8.total,
            "Cherry Flare S8": self.cherry_flare_s8.count,
            "Overall Cherry Aqua S9": self.cherry_aqua_s9.total,
            "Cherry Aqua S9": self.cherry_aqua_s9.count,
            "Timestamp": dt_string,
        }

        write_csv_dict(self.log_path, [logs], list(logs.keys()))

    def detect(self, frame):
        # detection
        frame_to_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.model(frame_to_rgb)  # detect cherry s8 and s9
        final_frame = results.render()[0]  # squeeze
        results_to_bgr = cv2.cvtColor(final_frame, cv2.COLOR_RGB2BGR)

        # get results from pandas dataframe
        results_df = results.pandas().xyxy[0]
        class_names = results_df.name.value_counts()

        self.cherry_flare_s8.update_total(class_names)
        self.cherry_aqua_s9.update_total(class_names)

        labels = [
            "Overall Cherry Flare S8: {}".format(
                self.cherry_flare_s8.total,
            ),
            "Cherry Flare S8: {}".format(
                self.cherry_flare_s8.count,
            ),
            "Overall Cherry Aqua S9: {}".format(
                self.cherry_aqua_s9.total,
            ),
            "Cherry Aqua S9: {}".format(
                self.cherry_aqua_s9.count,
            ),
        ]

        frame_label(results_to_bgr, labels, 0.5, 1, 25, (0, 255, 0))

        if self.logging_interval.check():
            self.__do_csv_logs()

        return results_to_bgr


if __name__ == "__main__":
    # Testing Purposes
    from imutils.video import VideoStream

    from Capture import capture
    from Record import Record

    cap = VideoStream().start()
    cherry_detect_yolov5 = Cherry_Detect_YOLOv5(
        custom_model_path="best_640x480_stretch.pt", logs_path="Logs"
    )
    record = Record("Recorded")

    while True:
        frame = cap.read()
        frame = cherry_detect_yolov5.detect(frame)

        cv2.imshow("frame", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == 27:
            break
        elif key == ord("c"):
            capture(frame, "Captured")
        elif key == ord("r"):
            record.setup(*frame.shape[:2], fps=10)
        elif key == ord("s"):
            record.stop()

        record.record(frame)
