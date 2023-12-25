import torch
import cv2

# Model
model = torch.hub.load(
    "ultralytics/yolov5",
    "yolov5x",
)  # or yolov5m, yolov5l, yolov5x, custom

if torch.cuda.is_available():
    model.cuda()

# Images
img = "1.jpg"  # or file, Path, PIL, OpenCV, numpy, list

# Inference
results = model(img)

results_df = results.pandas().xyxy[0]


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


class_name_location = []
for index, values in results_df.iterrows():
    center = (
        int((values[0] + values[2]) / 2),
        int((values[1] + values[3]) / 2),
    )
    class_name_location.append(
        "-".join(check_location(results.render()[0], center) + [values[6]])
    )
from collections import Counter

print(dict(Counter(class_name_location)))

results.show()
