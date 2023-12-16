import cv2
from datetime import datetime
import os


def capture(frame, directory, name):
    dt_string = datetime.now().strftime("%d.%m.%Y %H.%M.%S")
    image_path = os.path.join(directory, f"Captured-{name}-{dt_string}.jpg")
    cv2.imwrite(image_path, frame)
