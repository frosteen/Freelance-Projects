# YOLOV5 Dependencies
import cv2
import torch

# numpy
import numpy as np

# Tello
from djitellopy import Tello

# pygame
import pygame

# os
import os

# datetime
from datetime import datetime

# time
import time

# Speed of the drone
S = 60

# Create model for yolov5s
model = torch.hub.load("yolov5", "custom", path="yolov5s.pt", source="local")

model.device = "cpu"

# Confidence of Model
model.conf = 0.25

# Classes of objects
classes = {
    "person": 0,
    # "bird": 14,
    # "cat": 15,
    "dog": 16,
    # "horse": 17,
    # "sheep": 18,
    # "cow": 19,
    # "elephant": 20,
    # "bear": 21,
    # "zebra": 22,
    # "giraffe": 23,
}

# Convert to classes to list then pass to model
model.classes = list(classes.values())


class FrontEnd(object):
    """Maintains the Tello display and moves it through the keyboard keys.
    Press escape key to quit.
    The controls are:
        - T: Takeoff
        - L: Land
        - Arrow keys: Forward, backward, left and right.
        - A and D: Counter clockwise and clockwise rotations (yaw)
        - W and S: Up and down.
        - R: Record
        - F: Stop Record
        - C: Capture
    """

    def __init__(self):
        # Init pygame
        pygame.init()

        # Creat pygame window
        pygame.display.set_caption("YOLOV5 Tello Video Stream")
        self.screen = pygame.display.set_mode([960, 720])

        # Init Tello object that interacts with the Tello drone
        self.tello = Tello()

        # Drone velocities between -100~100
        self.for_back_velocity = 0
        self.left_right_velocity = 0
        self.up_down_velocity = 0
        self.yaw_velocity = 0
        self.speed = 10

        self.person_count_prev_time = 0
        self.person_count_prev = 0
        self.person_count = 0
        self.person_count_total = 0

        self.dog_count_prev_time = 0
        self.dog_count_prev = 0
        self.dog_count = 0
        self.dog_count_total = 0

        self.threshold_time = 2

        self.send_rc_control = False

        self.frame_reference = None
        self.is_video_record = False
        self.video_writer = False
        self.record_fps = 10  # fps of output video

        # create update timer
        pygame.time.set_timer(pygame.USEREVENT + 1, 10)

    def run(self):
        """Main program"""
        self.tello.connect()
        self.tello.set_speed(self.speed)

        # In case streaming is on. This happens when we quit this program without the escape key.
        self.tello.streamoff()
        self.tello.streamon()

        frame_read = self.tello.get_frame_read()

        should_stop = False
        while not should_stop:

            for event in pygame.event.get():
                if event.type == pygame.USEREVENT + 1:
                    self.update()
                elif event.type == pygame.QUIT:
                    should_stop = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        should_stop = True
                    else:
                        self.keydown(event.key)
                elif event.type == pygame.KEYUP:
                    self.keyup(event.key)

            if frame_read.stopped:
                break

            self.screen.fill([0, 0, 0])

            frame = frame_read.frame

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            ## YOLOV5 START ##
            results = model(frame)
            pandas_df = results.pandas().xyxy[0]
            names = pandas_df.name.value_counts()

            # PERSON START
            self.person_now_time = time.time()

            if "person" in names:
                self.person_count = names["person"]
                if (
                    self.person_count > self.person_count_prev
                    and (self.person_now_time - self.person_count_prev_time)
                    > self.threshold_time
                ):
                    self.person_count_total = (
                        self.person_count_total
                        + self.person_count
                        - self.person_count_prev
                    )
                    self.person_count_prev_time = self.person_now_time
                elif (
                    self.person_count > self.person_count_prev
                    and (self.person_now_time - self.person_count_prev_time)
                    <= self.threshold_time
                ):
                    self.person_count_prev_time = self.person_now_time
            elif "person" not in names:
                self.person_count = 0

            self.person_count_prev = self.person_count
            # PERSON END

            # DOG START
            self.dog_now_time = time.time()

            if "dog" in names:
                self.dog_count = names["dog"]
                if (
                    self.dog_count > self.dog_count_prev
                    and (self.dog_now_time - self.dog_count_prev_time)
                    > self.threshold_time
                ):
                    self.dog_count_total = (
                        self.dog_count_total + self.dog_count - self.dog_count_prev
                    )
                    self.dog_count_prev_time = self.dog_now_time
                elif (
                    self.dog_count > self.dog_count_prev
                    and (self.dog_now_time - self.dog_count_prev_time)
                    <= self.threshold_time
                ):
                    self.dog_count_prev_time = self.dog_now_time
            elif "dog" not in names:
                self.dog_count = 0

            self.dog_count_prev = self.dog_count
            # DOG END

            # SAVE TO CSV START
            with open(os.getcwd() + "/Data.csv", "a+") as file:
                dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

                output = "Live Persons,{},Overall Persons,{},Live Dogs,{},Overall Dogs,{},Timestamp,{}".format(
                    self.person_count,
                    self.person_count_total,
                    self.dog_count,
                    self.dog_count_total,
                    dt_string,
                )

                file.write(output + "\n")
                print(output)
            # SAVE TO CSV END

            frame = results.render()[0]
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            ## YOLOV5 END ##

            texts = [
                "Battery: {}%".format(self.tello.get_battery()),
                "Height: {}m".format(int(self.tello.get_height()) / 1000),
                "Temperature: {}C".format(self.tello.get_temperature()),
                "Overall Persons: {}".format(
                    self.person_count_total,
                ),
                "Live Persons: {}".format(
                    self.person_count,
                ),
                "Overall Dogs: {}".format(self.dog_count_total),
                "Live Dogs: {}".format(self.dog_count),
            ]

            for text in texts:
                index = texts.index(text)
                cv2.putText(
                    frame,
                    text,
                    (5, 720 - 5 - 20 * index),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    2,
                )

            self.frame_reference = frame

            if (
                self.is_video_record
                and self.frame_reference is not None
                and self.video_writer is not None
            ):
                print("recording...")
                cv2.putText(
                    frame,
                    "Recording...",
                    (5, 5),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    2,
                )
                self.video_writer.write(self.frame_reference)

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = np.rot90(frame)
            frame = np.flipud(frame)

            frame = pygame.surfarray.make_surface(frame)
            self.screen.blit(frame, (0, 0))
            pygame.display.update()

        # Call it always before finishing. To deallocate resources.
        pygame.quit()
        self.tello.end()

    def keydown(self, key):
        """Update velocities based on key pressed
        Arguments:
            key: pygame key
        """
        if key == pygame.K_UP:  # set forward velocity
            self.for_back_velocity = S
        elif key == pygame.K_DOWN:  # set backward velocity
            self.for_back_velocity = -S
        elif key == pygame.K_LEFT:  # set left velocity
            self.left_right_velocity = -S
        elif key == pygame.K_RIGHT:  # set right velocity
            self.left_right_velocity = S
        elif key == pygame.K_w:  # set up velocity
            self.up_down_velocity = S
        elif key == pygame.K_s:  # set down velocity
            self.up_down_velocity = -S
        elif key == pygame.K_a:  # set yaw counter clockwise velocity
            self.yaw_velocity = -S
        elif key == pygame.K_d:  # set yaw clockwise velocity
            self.yaw_velocity = S

    def keyup(self, key):
        """Update velocities based on key released
        Arguments:
            key: pygame key
        """
        if (
            key == pygame.K_UP or key == pygame.K_DOWN
        ):  # set zero forward/backward velocity
            self.for_back_velocity = 0
        elif (
            key == pygame.K_LEFT or key == pygame.K_RIGHT
        ):  # set zero left/right velocity
            self.left_right_velocity = 0
        elif key == pygame.K_w or key == pygame.K_s:  # set zero up/down velocity
            self.up_down_velocity = 0
        elif key == pygame.K_a or key == pygame.K_d:  # set zero yaw velocity
            self.yaw_velocity = 0
        elif key == pygame.K_t:  # takeoff
            self.tello.takeoff()
            self.send_rc_control = True
        elif key == pygame.K_l:  # land
            not self.tello.land()
            self.send_rc_control = False
        elif key == pygame.K_c:  # capture
            dt_string_capture = datetime.now().strftime("%d.%m.%Y %H_%M_%S")
            image_path = f"Captured-{dt_string_capture}.jpg"
            print(f"captured: {image_path}")
            cv2.imwrite(image_path, self.frame_reference)
        elif key == pygame.K_r:  # record
            dt_string_record = datetime.now().strftime("%d.%m.%Y %H_%M_%S")
            self.record_path = f"Record-{dt_string_record}.avi"
            print(f"record: {self.record_path}")
            h, w = self.frame_reference.shape
            fourcc = cv2.VideoWriter_fourcc(*"XVID")
            self.video_writer = cv2.VideoWriter(
                self.record_path, fourcc, self.record_fps, (w, h)
            )
            self.is_video_record = True
        elif key == pygame.K_f and self.video_writer is not None:  # record stop
            print(f"record stopped: {self.record_path}")
            self.video_writer.release()
            self.is_video_record = False

    def update(self):
        """Update routine. Send velocities to Tello."""
        if self.send_rc_control:
            self.tello.send_rc_control(
                self.left_right_velocity,
                self.for_back_velocity,
                self.up_down_velocity,
                self.yaw_velocity,
            )


def main():
    # create frontend object
    frontend = FrontEnd()

    # run frontend object
    frontend.run()


if __name__ == "__main__":
    main()
