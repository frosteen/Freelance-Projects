import os
import shutil

import cv2
import numpy as np

from MediapipeHands import draw_styled_landmarks, mediapipe_detection, mp_holistic
from ResizeImage import resize_image

gestures_path = os.path.join("DS_SAMPLE3", "DS")
no_sequences = 570  # videos per sign language
sequence_length = 30  # fps
image_size = (32, 32)


def extract_feature(gestures_path, gestures, no_sequences, sequence_length):
    try:
        shutil.rmtree(os.path.join("ASL_DATA"))
    except Exception as e:
        pass

    try:
        os.mkdir(os.path.join("ASL_DATA"))
    except Exception as e:
        pass

    # Create directory for each sequences inside each gestures
    for gesture in gestures:
        for sequence in range(0, no_sequences):
            try:
                os.makedirs(
                    os.path.join(
                        "ASL_DATA",
                        gesture,
                        str(sequence),
                    )
                )
            except OSError as e:
                pass

    # Using mediapipe holistic library for hand tracking
    with mp_holistic.Holistic(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    ) as holistic:

        for gesture in gestures:

            gesture_path = os.path.join(gestures_path, gesture)
            sequences = os.listdir(os.path.join(gesture_path))

            for seq_index, sequence in enumerate(sequences):

                print("Processing:", gesture, "-", seq_index)

                if seq_index >= no_sequences:
                    break

                cap = cv2.VideoCapture(os.path.join(gesture_path, sequence))

                fps = cap.get(cv2.CAP_PROP_FRAME_COUNT)  # get fps

                # sampled frames to have consistent 30fps for each video
                frames = [x * fps / sequence_length for x in range(sequence_length)]

                for frame_num in range(sequence_length):

                    cap.set(cv2.CAP_PROP_POS_FRAMES, frames[frame_num])

                    ret, frame = cap.read()

                    image, results = mediapipe_detection(frame, holistic)

                    black_image = np.zeros(
                        image.shape, dtype=np.uint8
                    )  # black background

                    large_black_image = np.zeros(
                        image.shape, dtype=np.uint8
                    )  # black background

                    draw_styled_landmarks(black_image, results)

                    draw_styled_landmarks(large_black_image, results)

                    black_image_with_hand = cv2.flip(black_image, 1)

                    large_black_image_with_hand = cv2.flip(large_black_image, 1)

                    black_image_with_hand = resize_image(
                        black_image_with_hand, image_size
                    )

                    large_black_image_with_hand = resize_image(
                        large_black_image_with_hand, (64, 64)
                    )

                    npy_path = os.path.join(
                        "ASL_DATA",
                        gesture,
                        str(seq_index),
                        "3DCNN_" + str(frame_num),
                    )

                    np.save(
                        npy_path, black_image_with_hand.astype("float32") / 255
                    )  # save the normalized image array

                    npy_path = os.path.join(
                        "ASL_DATA",
                        gesture,
                        str(seq_index),
                        "3DCNN_{}x{}_".format(*large_black_image_with_hand.shape)
                        + str(frame_num),
                    )

                    np.save(
                        npy_path, large_black_image_with_hand.astype("float32") / 255
                    )  # save the normalized image array

                    cv2.namedWindow("OpenCV Feed", cv2.WINDOW_NORMAL)
                    cv2.resizeWindow("OpenCV Feed", 720, 720)
                    cv2.imshow("OpenCV Feed", large_black_image_with_hand)

                    if cv2.waitKey(1) & 0xFF == 27:
                        break

                cap.release()
                cv2.destroyAllWindows()


def preprocess(gestures, sequence_length):
    print("Preprocessing...")

    try:
        shutil.rmtree(os.path.join("ASL_PREPROCESS"))
    except Exception as e:
        pass

    try:
        os.makedirs(os.path.join("ASL_PREPROCESS", "DATA"))
    except Exception as e:
        pass

    try:
        os.makedirs(os.path.join("ASL_PREPROCESS", "DATA", "TRAINING"))
    except Exception as e:
        pass

    try:
        os.makedirs(os.path.join("ASL_PREPROCESS", "DATA", "VALIDATION"))
    except Exception as e:
        pass

    try:
        os.makedirs(os.path.join("ASL_PREPROCESS", "DATA", "TESTING"))
    except Exception as e:
        pass

    try:
        os.makedirs(os.path.join("ASL_PREPROCESS", "LABELS"))
    except Exception as e:
        pass

    label_map = {
        label: num for num, label in enumerate(gestures)
    }  # map gestures to their respective number

    id_counter = 1

    for gesture in gestures:
        for sequence in np.array(
            os.listdir(
                os.path.join(
                    "ASL_DATA",
                    gesture,
                )
            )
        ).astype(int):
            window = []
            for frame_num in range(sequence_length):
                res = np.load(
                    os.path.join(
                        "ASL_DATA",
                        gesture,
                        str(sequence),
                        "3DCNN_{}.npy".format(frame_num),
                    )  # load numpy array from each sequence directories
                )
                window.append(res)

            np.save(
                os.path.join("ASL_PREPROCESS", "DATA", str(id_counter)),
                np.array(window),
            )

            np.save(
                os.path.join("ASL_PREPROCESS", "LABELS", str(id_counter)),
                np.array(label_map[gesture]),
            )

            id_counter += 1

    id_list = [x for x in range(1, id_counter)]

    length = len(id_list)

    np.random.shuffle(id_list)

    datasets = {
        "TRAINING": id_list[: int(length * 0.7)],  # 70% of Original Data
        "TESTING": id_list[
            int(length * 0.7) : int(length * 0.9)
        ],  # 20% of Original Data
        "VALIDATION": id_list[int(length * 0.9) :],  # 10% of Original Data
    }

    for dataset, id_list in datasets.items():
        for id in id_list:
            shutil.move(
                os.path.join(
                    "ASL_PREPROCESS",
                    "DATA",
                    "{}.npy".format(str(id)),
                ),
                os.path.join(
                    "ASL_PREPROCESS",
                    "DATA",
                    str(dataset),
                    "{}.npy".format(str(id)),
                ),
            )

    print("Successful!")


if __name__ == "__main__":
    gestures_path = os.path.join(gestures_path)

    gestures = np.array([gesture for gesture in os.listdir(gestures_path)])

    no_sequences = no_sequences

    sequence_length = sequence_length

    extract_feature(gestures_path, gestures, no_sequences, sequence_length)

    preprocess(gestures, sequence_length)
