from collections import Counter

import cv2
import num2words
from imutils.video import VideoStream

import Firebase
from Capture import capture
from CheckLocation import check_location
from RetinaNet.detect_images import RetinaNet


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

    retina_net = RetinaNet(min_size=5000, threshold=0.5)

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

            boxes, classes, frame = retina_net.detect_image(frame)

            class_name_location = []
            for box, class_name in zip(boxes, classes):
                center = (
                    int((box[0] + box[2]) / 2),
                    int((box[1] + box[3]) / 2),
                )
                class_name_location.append(
                    "-".join(check_location(frame, center) + [class_name])
                )

            Firebase.update(
                "/",
                {
                    "Sentence": create_sentence(dict(Counter(class_name_location))),
                    "Execute": False,
                },
            )

            capture(frame, "Capture", "RetinaNet")

        cv2.imshow("frame", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.stop()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
