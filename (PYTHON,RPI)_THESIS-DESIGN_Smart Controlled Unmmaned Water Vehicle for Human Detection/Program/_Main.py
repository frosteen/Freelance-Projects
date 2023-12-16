# This program needs coco.names, yolov4.cfg and yolov4.weights
import time

import cv2

from ResizeWithAspectRatio import ResizeWithAspectRatio
from RunEvery import RunEvery
from SendLocationThread import SendLocation
from StreamYOLOv4Thread import StreamYOLOv4
from WebcamVideoStream import WebcamVideoStream

# Using VideoStream from imutils (fast because of threading)
capture = WebcamVideoStream(src=0, width=320, height=320).start()

# initialize YOLOv4 in a another thread
StreamYOLOv4 = StreamYOLOv4(
    capture,
    yolo_cfg="YOLOv4_Models/yolov4-fastest.cfg",
    yolo_weights="YOLOv4_Models/yolov4-fastest.weights",
    yolo_size=(320, 320),
).start()

# initialize SendLocation in a another thread
SendLocation = SendLocation(
    port_GPS="/dev/ttyS0",
    port_SIM800L="/dev/ttyUSB0",
    cellphone_number="+639151798366",
    # cellphone_number="+639476207065",
    email_username="unmanned.vehicle.2022@gmail.com",
    email_password="unmannedvehicle@2022",
)

# wait for the GPS to initialize before detecting
SendLocation.wait_to_initialize()

# initialize notification interval
is_notif = RunEvery(2)

while True:
    # get properties from StreamYOLOv4
    frame = StreamYOLOv4.read()
    classes, scores, boxes = StreamYOLOv4.detect()

    # continue loop if frame does not exist
    if frame is None:
        continue

    # resize frame for good display
    resized_frame = ResizeWithAspectRatio(
        frame,
        width=720,
        inter=cv2.INTER_LINEAR,
    )

    # draw boxes
    if boxes is not None:
        for (classid, score, box) in zip(classes, scores, boxes):
            if classid != 0:  # check classid=0 only (person in coco.names)
                continue
            cv2.rectangle(
                frame,
                box,
                color=(0, 255, 0),
                thickness=2,
            )
            cv2.putText(
                frame,
                "%s: %.2f" % ("person", score),
                (box[0], box[1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                color=(0, 255, 0),
                thickness=2,
            )

            if is_notif.check():
                file_path = "Captured/Captured.jpg"

                # save image
                cv2.imwrite(file_path, resized_frame)

                # initialize send location thread
                SendLocation.start(file_path)

            is_notif.previous_time = time.time()

    # Display the resulting frame
    cv2.imshow("People Detection", resized_frame)

    # ESC to quit
    key = cv2.waitKey(1)
    if key & 0xFF == 27:
        break

# When everything done, stop the capture
StreamYOLOv4.stop()
capture.stop()
cv2.destroyAllWindows()
