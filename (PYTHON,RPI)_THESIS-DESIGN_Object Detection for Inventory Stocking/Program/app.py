import os

import cv2
from flask import Flask, Response, jsonify, redirect, render_template, request, url_for
from imutils.video import VideoStream

from Capture import capture as frame_capture
from CherryDetect import Cherry_Detect_YOLOv5
from Record import Record

app = Flask(__name__)

vs = None
get_frame_detected = None
cherry_detect_yolov5 = Cherry_Detect_YOLOv5(
    custom_model_path="best_832x624_stretch.pt",
    logs_path="Logs",
    logging_interval=5,  # every seconds
    yolov5_force_reload=False,
)
Record = Record("Recorded")


def gen_frames():
    global vs, get_frame_detected

    while True:
        # Initialize VideoStream on first response
        if vs is None:
            if os.name == "nt":  # check if running on windows
                vs = VideoStream(usePiCamera=False).start()
            else:  # else run with pi camera
                vs = VideoStream(usePiCamera=True, resolution=(416, 416)).start()

        frame = vs.read()  # read the camera frame

        # frame = cv2.flip(frame, 0)  # flip camera vertically

        if frame is None:
            continue

        get_frame_detected = cherry_detect_yolov5.detect(frame)  # yolov5 detection

        # Check if record
        if get_frame_detected is not None:
            Record.record(get_frame_detected)

        # convert frame to buffer
        _, buffer = cv2.imencode(".jpg", get_frame_detected)
        frame = buffer.tobytes()

        yield (
            b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
        )  # concat frame one by one and show result


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/video_feed")
def video_feed():
    return Response(gen_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/capture")
def capture():
    if get_frame_detected is not None:
        frame_capture(get_frame_detected, "Captured")
    return redirect(url_for("index"))


@app.route("/record", methods=["GET", "POST"])
def record():
    if request.method == "POST":
        request_recording = request.form["request_recording"]

        # Check if Record.is_recording is false in the server upon Record request at the frontend
        if not Record.is_recording and request_recording == "True":
            if get_frame_detected is not None:
                Record.setup(*get_frame_detected.shape[:2], fps=5.0)
                return jsonify({"is_recording": "True"})

        # Check if Record.is_recording is true in the server upon Stop request at the frontend
        elif Record.is_recording and request_recording == "False":
            Record.stop()
            return jsonify({"is_recording": "False"})

        # Check if Record.is_recording is true in the server upon Record request at the frontend
        elif Record.is_recording and request_recording == "True":
            return jsonify({"is_recording": "False"})

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
