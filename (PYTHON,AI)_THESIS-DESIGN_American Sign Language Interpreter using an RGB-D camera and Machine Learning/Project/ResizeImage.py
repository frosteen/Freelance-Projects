import cv2
import numpy as np


def resize_image(img, size=(28, 28)):
    # crop_square
    h, w = img.shape[:2]
    min_size = np.amin([h, w])

    # Centralize and crop
    crop_img = img[
        int(h / 2 - min_size / 2) : int(h / 2 + min_size / 2),
        int(w / 2 - min_size / 2) : int(w / 2 + min_size / 2),
    ]
    resized = cv2.resize(crop_img, size, interpolation=cv2.INTER_AREA)

    return resized


if __name__ == "__main__":
    import os

    primary_path = "DS_SAMPLE3/DS"

    for path in os.listdir(primary_path):
        ASL_path = os.path.join(primary_path, path)

        for video_path in os.listdir(ASL_path):
            cap = cv2.VideoCapture(os.path.join(ASL_path, video_path))
            print(os.path.join(ASL_path, video_path))
            print("WIDTH", cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            print("HEIGHT", cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            res, frame = cap.read()
            frame = resize_image(frame, (1000, 1000))
            cv2.putText(
                frame,
                os.path.join(ASL_path, video_path),
                (10, 30),
                cv2.FONT_HERSHEY_PLAIN,
                2,
                (0, 0, 0),
                3,
                cv2.LINE_AA,
            )
            cv2.putText(
                frame,
                os.path.join(ASL_path, video_path),
                (10, 30),
                cv2.FONT_HERSHEY_PLAIN,
                2,
                (0, 255, 0),
                2,
                cv2.LINE_AA,
            )
            cv2.namedWindow("FRAME", cv2.WINDOW_NORMAL)
            cv2.resizeWindow("FRAME", (720, 720))
            cv2.imshow("FRAME", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == 27:
                break

    cv2.destroyAllWindows()
