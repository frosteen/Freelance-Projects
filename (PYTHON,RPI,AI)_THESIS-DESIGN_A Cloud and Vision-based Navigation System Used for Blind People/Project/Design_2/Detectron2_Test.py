from collections import Counter

import cv2
import num2words

from CheckLocation import check_location
from Detector import *


def create_sentence(class_names_od, class_names_ps):
    sentence = "I see"

    for value in class_names_ps:
        sentence += f" {value}"

    for key, value in class_names_od.items():
        sentence += f" {num2words.num2words(value)} {key}"

    return sentence


detector_od = Detector(model_type="OD")
detector_ps = Detector(model_type="PS")
image = cv2.imread("1.jpg")
output, class_names_od = detector_od.on_image(image)
output, class_names_ps = detector_ps.on_image(image)

class_name_location = []

for item in class_names_od:
    class_name_location.append(
        "-".join(check_location(image, item["center"]) + [item["class_name"]])
    )

print(create_sentence(dict(Counter(class_name_location)), class_names_ps))

cv2.imshow("Result", output)
cv2.waitKey(0)
