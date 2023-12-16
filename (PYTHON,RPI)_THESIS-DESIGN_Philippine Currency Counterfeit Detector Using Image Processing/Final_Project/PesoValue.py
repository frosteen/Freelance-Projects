import cv2
import numpy as np
import matplotlib.pyplot as plt


centers = {
    "TWENTY PESOS": np.array([[49, 51, 84], [84, 90, 117], [135, 134, 144]]),
    "FIFTHY PESOS": np.array([[80, 55, 104], [115, 85, 122], [163, 135, 146]]),
    "ONE HUNDRED PESOS": np.array([[91, 51, 58], [138, 83, 91], [177, 139, 139]]),
    "TWO HUNDRED PESOS": np.array([[45, 51, 46], [73, 87, 82], [128, 136, 139]]),
    "FIVE HUNDRED PESOS": np.array([[48, 59, 67], [69, 87, 92], [125, 129, 129]]),
    "ONE THOUSAND PESOS": np.array([[72, 51, 35], [121, 92, 59], [168, 141, 107]]),
}


def graph_kmeans(title, data, label, center):
    # Graph Kmeans
    label = label.flatten()
    u_labels = np.unique(label)
    for i in u_labels:
        plt.scatter(
            data[label == i, 0],
            data[label == i, 1],
            label=str(center[i]),
            color=(np.float32(np.flip(center, 1)) / 255)[i],
        )
    plt.scatter(center[:, 0], center[:, 1], s=80, color="k")
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.show()


def color_quantization(image, clusters=3):
    """Performs color quantization using K-means clustering algorithm"""

    # Transform image into 'data':
    data = np.float32(image).reshape((-1, 3))

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
    return result, data, label, center


def calculate_peso_value(image, rtol=0.1):
    """
    Calculate peso value using color_quantization
    then check if image centers are close with reference centers
    """
    result, _, _, center = color_quantization(image, clusters=3)

    for peso_value, center_value in centers.items():

        center = np.sort(center, axis=0)
        center_value = np.sort(center_value, axis=0)

        is_close = np.allclose(center, center_value, rtol=rtol)

        if is_close:
            return peso_value


# For testing purposes no need to know
if __name__ == "__main__":
    import os

    path = os.path.join("Reference_Pictures")

    for fname in os.listdir(path):
        image = cv2.imread(os.path.join(path, fname))
        get_peso_value = calculate_peso_value(image, rtol=0.20)
        result, data, label, center = color_quantization(image, clusters=3)
        print(fname, np.sort(center, axis=0).tolist())
        print(fname, get_peso_value)
        graph_kmeans(get_peso_value, data, label, center)
        cv2.namedWindow("Result", cv2.WINDOW_NORMAL)
        cv2.imshow("Result", result)
