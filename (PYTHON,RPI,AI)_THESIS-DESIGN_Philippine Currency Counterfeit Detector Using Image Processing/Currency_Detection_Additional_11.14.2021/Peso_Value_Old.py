import cv2
import numpy as np

centers = {
    "twenty pesos": np.array(
        [
            [84, 71, 101],
            [117, 103, 122],
            [168, 147, 148],
        ]
    ),
    "fifthy pesos": np.array(
        [
            [122, 97, 182],
            [164, 142, 203],
            [211, 206, 223],
        ]
    ),
    "one hundred pesos": np.array(
        [
            [111, 69, 96],
            [165, 124, 153],
            [209, 176, 203],
        ]
    ),
    "two hundred pesos": np.array(
        [
            [96, 100, 74],
            [141, 152, 123],
            [210, 206, 188],
        ]
    ),
    "five hundred pesos": np.array(
        [
            [55, 75, 82],
            [85, 117, 116],
            [161, 165, 151],
        ]
    ),
    "one thousand pesos": np.array(
        [
            [90, 63, 37],
            [147, 112, 62],
            [192, 167, 116],
        ]
    ),
}


def color_quantization(image, clusters=3):
    """Performs color quantization using K-means clustering algorithm"""

    # Transform image into 'data':
    data = np.float32(image).reshape((-1, 3))
    # print(data.shape)

    # Define the algorithm termination criteria (the maximum number of iterations and/or the desired accuracy):
    # In this case the maximum number of iterations is set to 20 and epsilon = 1.0
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)

    # Apply K-means clustering algorithm:
    ret, label, center = cv2.kmeans(
        data, clusters, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS
    )

    # At this point we can make the image with k colors
    # Convert center to uint8:
    center = np.uint8(center)
    # Replace pixel values with their center value:
    result = center[label.flatten()]
    result = result.reshape(image.shape)
    return result, center


def calculate_peso_value(image, rtol=0.1):
    """
    Calculate peso value using color_quantization
    then check if image centers are close with reference centers
    """
    image, center = color_quantization(image, clusters=3)

    for peso_value, center_value in centers.items():

        center = np.sort(center, axis=0)
        center_value = np.sort(center_value, axis=0)

        is_close = np.allclose(center, center_value, rtol=rtol)

        if is_close:
            return peso_value


# For testing purposes no need to know
if __name__ == "__main__":
    import os

    path = os.path.join("Test_Pictures")
    for fname in os.listdir(path):
        image = cv2.imread(os.path.join(path, fname))
        get_peso_value = calculate_peso_value(image, rtol=0.2)
        print(fname, get_peso_value)
