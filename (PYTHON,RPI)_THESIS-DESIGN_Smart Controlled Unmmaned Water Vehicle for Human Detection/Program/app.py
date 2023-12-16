# This program needs coco.names, yolov4.cfg and yolov4.weights
import time

import cv2
from flask import Flask, Response, render_template

from ResizeWithAspectRatio import ResizeWithAspectRatio
from RunEvery import RunEvery

from SendLocationThread import SendLocation
from StreamYOLOv4Thread import StreamYOLOv4
from WebcamVideoStream import WebcamVideoStream
from ReadWriteCSV import write_csv_dict
import time
import datetime

app = Flask(__name__)

capture = None
StreamYOLOv4_Obj = None
SendLocation_Obj = None
is_notif = None


def csv_log(date, name, processing_time):
    write_csv_dict(
        "Logs.csv",
        {
            "Date": date,
            "Name": name,
            "Processing Time": processing_time,
        },
    )


def gen_frames():
    global capture, StreamYOLOv4_Obj, SendLocation_Obj, is_notif

    if capture is None:
        # Using VideoStream from imutils (fast because of threading)
        capture = WebcamVideoStream(src=0, width=320, height=320).start()

        # initialize YOLOv4 in a another thread
        StreamYOLOv4_Obj = StreamYOLOv4(
            capture,
            yolo_cfg="YOLOv4_Models/yolov4-fastest.cfg",
            yolo_weights="YOLOv4_Models/yolov4-fastest.weights",
            yolo_size=(320, 320),
        ).start()

        # initialize SendLocation in a another thread
        SendLocation_Obj = SendLocation(
            port_GPS="/dev/ttyS0",
            port_SIM800L="/dev/ttyUSB0",
            cellphone_number="+639151798366",
            # cellphone_number="+639476207065",
            email_username="unmanned.vehicle.2022@gmail.com",
            email_password="czkswzrvulvmkhvu",
        )

        # wait for the GPS to initialize before detecting
        SendLocation_Obj.wait_to_initialize()

        # initialize notification interval
        is_notif = RunEvery(2)

    while True:
        if is_notif is None:
            continue

        # get properties from StreamYOLOv4
        frame = StreamYOLOv4_Obj.read()
        detect_time_start = time.time()
        detect_time_total_start = time.time()
        classes, scores, boxes = StreamYOLOv4_Obj.detect()

        # continue loop if frame does not exist
        if frame is None:
            continue

        # draw
        if boxes is not None:
            num_people = 0
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
                num_people += 1
                if time.time() - is_notif.previous_time >= is_notif.interval:
                    csv_log(
                        datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                        f"Person Detected {num_people}",
                        time.time() - detect_time_start,
                    )

            if is_notif.check() and num_people > 0:
                csv_log(
                    datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                    f"All People Detected Total: {num_people}",
                    time.time() - detect_time_total_start,
                )
                print("Sending...", num_people)
                file_path = "Captured/Captured.jpg"

                # save image
                capture_time_start = time.time()
                cv2.imwrite(file_path, frame)
                csv_log(
                    datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                    f"Capture Time",
                    time.time() - capture_time_start,
                )

                # initialize send location thread
                SendLocation_Obj.start(file_path, num_people)

                is_notif.previous_time = time.time()

        # resize frame for good display
        resized_frame = ResizeWithAspectRatio(
            frame,
            width=720,
            inter=cv2.INTER_LINEAR,
        )

        # convert frame to buffer
        _, buffer = cv2.imencode(".jpg", resized_frame)
        frame = buffer.tobytes()

        # concat frame one by one and show result
        yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/video_feed")
def video_feed():
    return Response(gen_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
