from collections import Counter

import cv2

from CheckLocation import check_location
from RetinaNet.detect_images import RetinaNet

retina_net = RetinaNet(min_size=5000, threshold=0.5)

frame = cv2.imread("1.jpg")

boxes, classes, result = retina_net.detect_image(frame)

class_name_location = []
for box, class_name in zip(boxes, classes):
    center = (
        int((box[0] + box[2]) / 2),
        int((box[1] + box[3]) / 2),
    )
    class_name_location.append("-".join(check_location(frame, center) + [class_name]))

print(dict(Counter(class_name_location)))

cv2.imshow("frame", result)
cv2.waitKey(0)
