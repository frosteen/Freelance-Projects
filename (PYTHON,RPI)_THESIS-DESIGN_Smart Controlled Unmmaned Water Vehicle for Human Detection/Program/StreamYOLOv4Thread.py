# import the necessary packages
from threading import Thread

import cv2


class StreamYOLOv4:
    def __init__(
        self,
        stream,
        yolo_cfg="YOLOv4_Models/yolov4.cfg",
        yolo_weights="YOLOv4_Models/yolov4.weights",
        yolo_size=(416, 416),
        CONFIDENCE_THRESHOLD=0.6,
        NMS_THRESHOLD=0.4,
        name="StreamYOLOv4",
    ):
        # get the passed stream
        self.stream = stream
        self.frame = None

        # initialize the thread name
        self.name = name

        # initialize the variable used to indicate if the thread should
        # be stopped
        self.stopped = False

        # YOLOv4 cfg and weights
        self.net = cv2.dnn.readNetFromDarknet(yolo_cfg, yolo_weights)

        # create model
        self.model = cv2.dnn_DetectionModel(self.net)

        # input parameters
        self.model.setInputParams(scale=1 / 255, size=yolo_size, swapRB=True)

        # YOLOv4 confidence and nms thresholds
        self.CONFIDENCE_THRESHOLD = CONFIDENCE_THRESHOLD
        self.NMS_THRESHOLD = NMS_THRESHOLD

        # initialize detections
        self.classes, self.scores, self.boxes = None, None, None

    def start(self):
        # start the thread to read frames from the video stream
        t = Thread(target=self.update, name=self.name, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        while True:
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                return

            # check if frame exist else continue
            if not self.stream.grabbed:
                continue

            # otherwise, read the next frame from the stream
            self.frame = self.stream.read()

            # detect using yolov4
            self.classes, self.scores, self.boxes = self.model.detect(
                self.frame,
                confThreshold=self.CONFIDENCE_THRESHOLD,
                nmsThreshold=self.NMS_THRESHOLD,
            )

    def read(self):
        return self.frame

    def detect(self):
        return (self.classes, self.scores, self.boxes)

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True
