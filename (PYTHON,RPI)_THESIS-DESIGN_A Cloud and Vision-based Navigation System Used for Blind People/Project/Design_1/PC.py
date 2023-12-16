from collections import Counter

import cv2
import num2words
import torch
from imutils.video import VideoStream

import Firebase
from Capture import capture
from CheckLocation import check_location


def create_sentence(class_name_location):
    sentence = "I see"

    for key, value in class_name_location.items():
        sentence += f" {num2words.num2words(value)} {key}"

    print(sentence)
    return sentence


def firebase_get_TCP_URL(location="/"):
    print("Waiting for new TCP_URL.")
    prev = Firebase.get(location)
    while True:
        TCP_URL = Firebase.get(location)
        if prev != TCP_URL:
            return TCP_URL


def main():
    Firebase.update("/", {"Execute": False})

    model = torch.hub.load("ultralytics/yolov5", "yolov5x", force_reload=True)
    model.conf = 0.5  # set threshold
    if torch.cuda.is_available():
        model.cuda()

    TCP_URL = firebase_get_TCP_URL("/TCP_URL")
    print("TCP_URL:", TCP_URL)
    cap = VideoStream(src=TCP_URL, resolution=(1280, 960)).start()

    while True:
        frame = cap.read()

        if not cap.grabbed:
            continue

        # Must convert to RGB before inputting to the model
        if Firebase.get("Execute") == True:
            Firebase.update("/", {"is_processing": True})
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

            Firebase.update(
                "/",
                {
                    "Sentence": create_sentence(dict(Counter(class_name_location))),
                    "Execute": False,
                },
            )

            capture(frame, "Capture", "YOLOv5")

        cv2.imshow("frame", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.stop()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
