import os
import time
from datetime import datetime
from threading import Thread

import cv2
import torch

from CVUtils import centroid, transparent_rectangle
from ReadWriteCSV import write_csv_dict
from RunEvery import RunEvery
from ThingsSpeak import write_data

# Editable Settings Start
schedule_counter = RunEvery(0.5, 0)
schedule_logging = RunEvery(30)
schedule_thingspeak = RunEvery(30)  # Preferred same time w/ schedule_logging
# Editdable Settings End

# Detect only vehicles
classes = {
    "car": {
        "total": 0,
        "class-no": 2,
    },
    "motorcycle": {
        "total": 0,
        "class-no": 3,
    },
    "bus": {
        "total": 0,
        "class-no": 5,
    },
    "truck": {
        "total": 0,
        "class-no": 7,
    },
    "bicycle": {
        "total": 0,
        "class-no": 1,
    },
}

# Create yolov5 model
model = torch.hub.load("ultralytics/yolov5", "yolov5s")  # , force_reload=True)
model.classes = [x["class-no"] for x in list(classes.values())]
model.cuda()
# model.conf = 0.5  # NMS confidence threshold
# model.iou = 0.5  # NMS IoU threshold

total_vehicles = 0

# Create logs directory
now = datetime.now()
path = os.path.join("Logs", now.strftime("%m.%d.%Y"))
if not os.path.isdir(path):
    os.makedirs(path)

# Capture via TCP Stream
cap = cv2.VideoCapture("tcp://6.tcp.ngrok.io:19023")

# For testing purposes
# cap = cv2.VideoCapture("Samples/From_Github/cars.avi")

# get height of frame
max_y = 0
while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        max_y = frame.shape[0]
        break

# create trackbars for easy customization
cv2.namedWindow("frame", cv2.WINDOW_NORMAL)
cv2.createTrackbar("line_y", "frame", int(max_y / 2), max_y, lambda x: x)
cv2.createTrackbar("offset_y", "frame", 10, 30, lambda x: x)

while cap.isOpened():
    start_time = time.time()

    ret, frame = cap.read()

    line_y = cv2.getTrackbarPos("line_y", "frame")
    offset_y = cv2.getTrackbarPos("offset_y", "frame")

    if not ret:
        break

    frame_to_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # YOLOV5 uses RGB
    results = model(frame_to_rgb, size=320)  # preferred size for fast results
    results_frame = results.render()[0]  # get frame result
    results_to_bgr = cv2.cvtColor(results_frame, cv2.COLOR_RGB2BGR)  # Revert to BGR
    results_df = results.pandas().xyxy[0]  # get dataframe result

    # create transparent boundary rectangle for vehicle counting
    results_to_bgr = transparent_rectangle(
        results_to_bgr,
        0.2,
        (0, line_y - offset_y),
        (frame.shape[1], line_y + offset_y),
        (0, 255, 0),
        -1,
    )

    for item in results_df.values:
        classname = item[6]
        if classname in classes.keys():
            # xmin, ymin, xmax-xmin, ymax-ymin
            x, y, w, h = item[0], item[1], item[2] - item[0], item[3] - item[1]

            get_center = centroid(x, y, w, h)
            cy = get_center[1]

            cv2.circle(
                results_to_bgr, get_center, 4, (0, 0, 255), -1
            )  # draw a point on the calculated centroid

            if (
                cy < (line_y + offset_y)
                and cy > (line_y - offset_y)
                and schedule_counter.check()
            ):
                # create transparent boundary rectangle again for effects
                results_to_bgr = transparent_rectangle(
                    results_to_bgr,
                    1,
                    (0, line_y - offset_y),
                    (frame.shape[1], line_y + offset_y),
                    (0, 255, 0),
                    -1,
                )

                classes[classname]["total"] += 1

                # reset total vehicles counting to avoid overlapping
                total_vehicles = 0
                for key, value in classes.items():
                    total_vehicles += value["total"]

    # ThingsSpeak Logging
    if schedule_thingspeak.check():
        fields = ""

        for key, value in classes.items():
            index = list(classes.keys()).index(key)
            fields += "field{}={}&".format(index + 1, value["total"])

        fields = fields[:-1]  # field1=0&field2=0&field3=0&...

        Thread(
            target=lambda: write_data(
                "https://api.thingspeak.com/update?api_key=YV5M6ZT24TLO51TR&" + fields
            )
        ).start()  # run it as a thread to avoid blocking

    # CSV Logging
    if schedule_logging.check():
        logging_time = datetime.now().strftime("%m/%d/%Y %H:%M:%S")

        # create dictwriter format for csv writing
        # convert classes where key is classname and value is total. ex: { "Car": 2, "Motorcycle": 3, ... }
        logs = {key.capitalize(): value["total"] for key, value in classes.items()}
        logs["Total Vehicles"] = total_vehicles  # add total vehicles in the dictionary
        logs["Timestamp"] = logging_time  # add timestamp in the dictionary

        write_csv_dict(
            os.path.join(path, now.strftime("%m.%d.%Y_%H.%M.%S") + ".csv"),
            [logs],
            list(logs.keys()),
        )

        print(logs)  # print logs for visibility

        # reset all to 0 upon finish logging
        for key, value in classes.items():
            value["total"] = 0

    fps = 1.0 / (time.time() - start_time)  # frames per second

    cv2.putText(
        results_to_bgr, str(fps), (5, 35), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 2
    )  # put fps in the frame for easy visibility (for checking if it drops)

    cv2.resizeWindow("frame", 1152, 648)
    cv2.imshow("frame", results_to_bgr)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
