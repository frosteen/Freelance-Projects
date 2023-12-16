from collections import Counter

import cv2
import num2words
from imutils.video import VideoStream

import Firebase
from Capture import capture
from CheckLocation import check_location
from Detector import *


def create_sentence(class_names_od, class_names_ps):
    sentence = "I see"

    for value in class_names_ps:
        sentence += f" {value}"

    for key, value in class_names_od.items():
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

    detector_od = Detector(model_type="OD")
    detector_ps = Detector(model_type="PS")

    TCP_URL = firebase_get_TCP_URL("/TCP_URL")
    # TCP_URL = Firebase.get("/TCP_URL")
    print("TCP_URL:", TCP_URL)
    cap = VideoStream(src=TCP_URL, resolution=(1280, 960)).start()

    while True:
        frame = cap.read()

        if not cap.grabbed:
            continue

        # Must convert to RGB before inputting to the model
        if Firebase.get("Execute") == True:
            Firebase.update("/", {"is_processing": True})

            frame_od, class_names_od = detector_od.on_image(frame)
            frame, class_names_ps = detector_ps.on_image(frame)

            class_name_location = []

            for item in class_names_od:
                class_name_location.append(
                    "-".join(
                        check_location(frame, item["center"]) + [item["class_name"]]
                    )
                )

            Firebase.update(
                "/",
                {
                    "Sentence": create_sentence(
                        dict(Counter(class_name_location)), class_names_ps
                    ),
                    "Execute": False,
                },
            )

            capture(frame_od, "Capture", "OD")
            capture(frame, "Capture", "PS")

        cv2.imshow("frame", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.stop()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
