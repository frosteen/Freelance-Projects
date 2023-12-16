import pyrebase
import torch
import cv2
import num2words
from collections import Counter
from datetime import datetime
import os

config = {
    "apiKey": "AIzaSyBz6KVh7zrUWtXKXh9RtR-mLBU5EPIv0qY",
    "authDomain": "guide-blind-people.firebaseapp.com",
    "databaseURL": "https://guide-blind-people-default-rtdb.firebaseio.com",
    "storageBucket": "guide-blind-people.appspot.com",
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()
storage = firebase.storage()


db.child("Execute").set(False)
model = torch.hub.load("ultralytics/yolov5", "yolov5x", force_reload=True)
model.conf = 0.5  # set threshold
if torch.cuda.is_available():
    model.cuda()

def capture(frame, directory, name):
    dt_string = datetime.now().strftime("%d.%m.%Y %H.%M.%S")
    image_path = os.path.join(directory, f"Captured-{name}-{dt_string}.jpg")
    cv2.imwrite(image_path, frame)


def check_location(image, center):
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

def create_sentence(class_name_location):
    dt_string = datetime.now().strftime("%d.%m.%Y %H.%M.%S")
    print(f"\n{dt_string}")
    sentence = "I see"
    for key, value in class_name_location.items():
        sentence += f" {num2words.num2words(value)} {key}"

    print(sentence)
    print("____________________________________")
    return sentence


def main():
    while True:
        execute_status = db.child("Execute").get().val()
        if execute_status == True:
            db.child("is_processing").set(True)
            storage.child("cur_image.png").download("cur_image.png", "cur_image.png")
            frame = cv2.imread("cur_image.png")
            
            frame_to_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = model(frame_to_rgb)
            results_df = results.pandas().xyxy[0]
            frame = cv2.cvtColor(results.render()[0], cv2.COLOR_RGB2BGR)

            class_name_location = []
            for _, values in results_df.iterrows():
                center = (
                    int((values[0] + values[2]) / 2),
                    int((values[1] + values[3]) / 2),
                )
                class_name_location.append(
                    "-".join(check_location(frame, center) + [values[6]])
                )

            db.child("Sentence").set(create_sentence(dict(Counter(class_name_location))))
            db.child("Execute").set(False)

            capture(frame, "Capture", "YOLOv5")

if __name__ == "__main__":
    main()



