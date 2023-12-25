import os

import cv2
import numpy as np
from tensorflow.keras.models import load_model

from WebcamThreading_Fast import WebcamVideoStream

# gestures_path = "ASL_DATA"
sequence_length = 30  # fps
image_size = (32, 32)
batch_size = 32
# threshold for each gesture; 0 is the lowest and 1 is the highest
prediction_threshold = 0.90

# gestures_path = os.path.join(gestures_path)
# gestures = np.array([gesture for gesture in os.listdir(gestures_path)])
gestures = [
    "Abstain",
    "Accident",
    "Airplane",
    "Badger",
    "Commute",
    "Daily",
    "Dart",
    "Glad",
    "Glance",
    "Police",
    "Reason",
]
model = load_model(os.path.join("MODELS", "gesture_ensemble.h5"))


def prob_viz(result, gestures, input_frame):
    output_frame = input_frame.copy()
    spacing = 25
    for num, prob in enumerate(result):
        # visualize probability distribution
        cv2.rectangle(
            output_frame,
            (0, 20 + num * spacing),
            (int(prob * 100), 40 + num * spacing),
            (0, 0, 255),
            -1,
        )

        cv2.putText(
            output_frame,
            gestures[num] + " " + str(round(float(prob * 100), 2)) + "%",
            (0, 35 + num * spacing),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 255),
            1,
            cv2.LINE_AA,
        )

    return output_frame


def list_words(sentence, input_frame):
    spacing = 45
    for num, word in enumerate(sentence):
        text_size = cv2.getTextSize(word, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
        cv2.putText(
            input_frame,
            word,
            (
                int(input_frame.shape[1] - text_size[0]),
                35 + num * spacing,
            ),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 255),
            2,
            cv2.LINE_AA,
        )


sequence = []
sentence = []
predictions = []
sentences = 0
result = np.zeros(len(gestures))

# fast video processing
cap = WebcamVideoStream(
    src=0,
    width=1920,
    height=1080,
    image_size=(32, 32),
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
    show_original_frame=True,  # show what the camera sees
).start()

while True:
    frame_non_resized, frame_resized = cap.read()

    if frame_non_resized is None or frame_resized is None:
        continue

    sequence.append(
        frame_resized.astype("float32") / 255
    )  # append the normalized image array

    sequence = sequence[
        -sequence_length:
    ]  # get always the last "sequence_length" frames

    if len(sequence) == sequence_length:
        # check if all frames are non-zeros
        # else return a result of zero, clear predictions,
        # and clear sequences
        if np.any(np.array(sequence)):
            # predict after getting the last sequence_length frames
            expand = np.expand_dims(sequence, axis=0)  # (1, *sequence)
            # model.predict returns a list so need to get the first one
            result = model.predict(expand, batch_size=batch_size)[0]
            predictions.append(np.argmax(result))  # append the result
            predictions = predictions[-20:]  # get always the last 20 predictions
            # check if last 20 predictions are all same (for stability)
            if (
                np.unique(predictions)[0] == np.argmax(result)
                and len(np.unique(predictions)) == 1
                and len(predictions) == 20
            ):
                # check if prediction is above threshold
                if result[np.argmax(result)] > prediction_threshold:
                    if len(sentence) > 0:
                        # append if gesture is not the same
                        if gestures[np.argmax(result)] != sentence[-1].split("-")[1]:
                            sentence.append(
                                "{}-{}".format(sentences, gestures[np.argmax(result)])
                            )
                            sentences += 1
                    else:
                        sentence.append(
                            "{}-{}".format(sentences, gestures[np.argmax(result)])
                        )
                        sentences += 1
                    predictions.clear()
        else:
            result = np.zeros(len(gestures))
            predictions.clear()
            sequence.clear()

    sentence = sentence[-6:]  # get always the last 11 sentences

    # visualize the prediction
    frame_non_resized = prob_viz(result, gestures, frame_non_resized)

    # put rectangle on the center of frame
    # to indicate only predict on that area
    h, w = frame_non_resized.shape[:2]
    min_size = np.amin([h, w])
    cv2.rectangle(
        frame_non_resized,
        (int(w / 2 - min_size / 2), int(h / 2 - min_size / 2)),
        (int(w / 2 + min_size / 2), int(h / 2 + min_size / 2)),
        (0, 255, 0),
        1,
        cv2.LINE_AA,
    )

    # enumerate each word at the right side of the frame
    list_words(sentence, frame_non_resized)

    cv2.namedWindow("OpenCV Feed", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("OpenCV Feed", 1280, 720)
    cv2.imshow("OpenCV Feed", frame_non_resized)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.stop()
cv2.destroyAllWindows()
