import cv2
import picamera
from picamera.array import PiRGBArray
from firebase import firebase
import threading

bird2_cascade = cv2.CascadeClassifier('bird2-cascade.xml')
camera = picamera.PiCamera()
firebase = firebase.FirebaseApplication(
    'https://thesisbirdsystem.firebaseio.com', None)

birds2 = []

# Two loops run independently


def runFirebase():
    while True:
        if len(birds2) > 0:
            firebase.patch("/", {"IsThereBird": "true"})
            print("Bird detected!")
        else:
            firebase.patch("/", {"IsThereBird": "false"})


x = threading.Thread(target=runFirebase, daemon=True)
x.start()

while True:
    rawCapture = PiRGBArray(camera)
    camera.capture(rawCapture, format="rgb")
    img = rawCapture.array
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    birds2 = bird2_cascade.detectMultiScale(gray, 1.3, 1)

    for (x, y, w, h) in birds2:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 2)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, 'Bird', (x - w, y - h), font,
                    0.5, (0, 255, 255), 2, cv2.LINE_AA)

    cv2.imshow('img', img)

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
