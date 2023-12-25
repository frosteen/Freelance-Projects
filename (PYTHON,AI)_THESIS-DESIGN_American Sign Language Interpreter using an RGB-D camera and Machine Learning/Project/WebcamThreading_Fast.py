# import the necessary packages
from threading import Thread

import cv2
import numpy as np

from MediapipeHands import draw_styled_landmarks, mediapipe_detection, mp_holistic
from ResizeImage import resize_image
from DrawRectangleHand import draw_rectangle_hand


class WebcamVideoStream:
    def __init__(
        self,
        src=0,
        width=1920,
        height=1080,
        image_size=(32, 32),
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
        show_original_frame=True,
    ):
        # initialize properties
        self.results = None
        self.black_image_with_hand_non_resized = None
        self.black_image_with_hand_resized = None
        self.frame = None
        self.image_size = image_size
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence
        self.show_original_frame = show_original_frame

        # initialize the video camera stream and read the first frame
        # from the stream
        self.stream = cv2.VideoCapture(src, cv2.CAP_DSHOW)
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        (self.grabbed, self.frame) = self.stream.read()

        # initialize the variable used to indicate if the thread should
        # be stopped
        self.stopped = False

    def start(self):
        # start the thread to read frames from the video stream
        webcam_capture_thread = Thread(target=self.webcam_capture)
        webcam_capture_thread.daemon = True
        webcam_capture_thread.start()

        # start the thread to read frames from the webcam_capture thread
        mediapipe_processing_thread = Thread(target=self.mediapipe_processing)
        mediapipe_processing_thread.daemon = True
        mediapipe_processing_thread.start()
        return self

    def mediapipe_processing(self):
        # keep looping infinitely until the thread is stopped
        with mp_holistic.Holistic(
            min_detection_confidence=self.min_detection_confidence,
            min_tracking_confidence=self.min_tracking_confidence,
        ) as holistic:
            while not self.stopped:
                # if the thread indicator variable is set, stop the thread
                if self.stopped:
                    return

                # otherwise, read the next frame from the webcam_capture thread
                image, self.results = mediapipe_detection(self.frame, holistic)
                black_image = np.zeros(image.shape, dtype=np.uint8)
                draw_styled_landmarks(black_image, self.results)
                black_image_with_hand = cv2.flip(black_image, 1)
                self.black_image_with_hand_non_resized = black_image_with_hand.copy()
                self.black_image_with_hand_resized = resize_image(
                    black_image_with_hand, self.image_size
                )

    def webcam_capture(self):
        # keep looping infinitely until the thread is stopped
        while not self.stopped:
            # otherwise, read the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()

        self.stream.release()

    def read(self):
        # return the frame most recently read
        if self.show_original_frame:
            draw_rectangle_hand(self.frame, self.results)
            return cv2.flip(self.frame, 1), self.black_image_with_hand_resized
        return (
            self.black_image_with_hand_non_resized,
            self.black_image_with_hand_resized,
        )

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True
