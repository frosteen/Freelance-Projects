import cv2


def draw_rectangle_hand(image, results, spacing=100):
    if results is not None and results.right_hand_landmarks is not None:
        h, w = image.shape[:2]
        right_hand_center = results.right_hand_landmarks.landmark[9]
        cv2.rectangle(
            image,
            (
                int(right_hand_center.x * w) - spacing,
                int(right_hand_center.y * h) - spacing,
            ),
            (
                int(right_hand_center.x * w) + spacing,
                int(right_hand_center.y * h) + spacing,
            ),
            (0, 255, 0),
            thickness=2,
        )
