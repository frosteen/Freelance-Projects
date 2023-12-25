import cv2
import numpy as np
import os
import re
import easyocr


class PesoImage:
    def __init__(self, image, water_mark_path, baybayin_path):
        "Must be a BGR image"
        self.image = image.copy()
        self.h, self.w, self.c = self.image.shape
        self.water_mark_path = water_mark_path
        self.baybayin_path = baybayin_path
        self.reader = easyocr.Reader(["ch_sim", "en"])

    def CalculateR(self):
        "Calculate, r = black_pixels/white_pixels"
        image_gray = cv2.cvtColor(self.image.copy(), cv2.COLOR_BGR2GRAY)
        # image_denoise = cv2.fastNlMeansDenoising(image_gray, None, 10, 7, 21)
        # image_blur = cv2.medianBlur(image_denoise, 5)
        # image_threshold = cv2.adaptiveThreshold(
        #     image_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        # )
        image_threshold = cv2.threshold(
            image_gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU
        )[1]

        white_pixels = np.sum(image_threshold == 255)
        black_pixels = np.sum(image_threshold == 0)
        r = black_pixels / white_pixels

        if r < 4.1:
            return r, True

        return r, False

    def SerialNumber(self):
        "Check if SerialNumber exists"

        image_crop = self.image.copy()[
            int(self.h * 0.700) : int(self.h * 0.90),
            int(self.w * 0.025) : int(self.w * 0.225),
        ]
        image_gray = cv2.cvtColor(image_crop, cv2.COLOR_BGR2GRAY)
        # image_denoise = cv2.fastNlMeansDenoising(image_gray, None, 10, 7, 21)
        # image_blur = cv2.GaussianBlur(image_denoise, (5, 5), 0)
        # image_canny_edge = cv2.Canny(image_blur, 5, 60)
        # image_thresh = cv2.threshold(image_canny_edge, 0, 255, cv2.THRESH_BINARY)[1]

        data = "".join(self.reader.readtext(image_gray, detail=0))

        filtered_SN = re.sub(r"\W+", "", data)

        print("SN:", filtered_SN)

        len_filtered_SN = len(filtered_SN)

        if len_filtered_SN > 5:
            return image_gray, True

        return image_gray, False

    def WaterMark(self):
        "Check if WaterMark can be identified"
        results = {}
        locations = {}
        water_marks = os.listdir(self.water_mark_path)
        image = self.image.copy()
        image_copy = image.copy()

        for water_mark in water_marks:
            template = cv2.imread(self.water_mark_path + "/" + water_mark)
            TemplateMatch = PesoImage.TemplateMatch(image, template)

            results[water_mark] = TemplateMatch[1]
            locations[water_mark] = TemplateMatch[3]

            image = image_copy.copy()

        key_best_result = max(results, key=results.get)
        value_best_result = results[key_best_result]

        value_best_location = locations[key_best_result]
        (startX, startY) = value_best_location

        # print("WaterMarkLoc:", startX, startY)
        # print("WaterMark:", key_best_result, value_best_result)

        if value_best_result > 0.90 and startX > (self.w * 0.70):
            PesoImage.TemplateMatch(image, template)
            return image, True

        return image, False

    def SeeThroughPrint(self):
        "Check if see-through print baybayin text exist"
        results = {}
        locations = {}
        water_marks = os.listdir(self.baybayin_path)
        image = self.image.copy()
        image_copy = image.copy()

        for water_mark in water_marks:
            template = cv2.imread(self.baybayin_path + "/" + water_mark)
            TemplateMatch = PesoImage.TemplateMatch(image, template)

            results[water_mark] = TemplateMatch[1]
            locations[water_mark] = TemplateMatch[3]

            image = image_copy.copy()

        key_best_result = max(results, key=results.get)
        value_best_result = results[key_best_result]

        value_best_location = locations[key_best_result]
        (startX, startY) = value_best_location

        # print("SeeThroughPrintLoc:", startX, startY)
        # print("SeeThroughPrint:", key_best_result, value_best_result)

        if (
            value_best_result > 0.90
            and startX > (self.w * 0.70)
            and startY > (self.h * 0.50)
        ):
            PesoImage.TemplateMatch(image, template)
            return image, True

        return image, False

    def SecurityThread(self):
        "Check if security thread exist"
        image_crop = self.image.copy()[
            int(self.h * 0.20) : int(self.h * 0.98),
            int(self.w * 0.45) : int(self.w * 0.80),
        ]
        image_gray = cv2.cvtColor(image_crop, cv2.COLOR_BGR2GRAY)
        image_denoise = cv2.fastNlMeansDenoising(image_gray, None, 10, 7, 21)
        image_blur = cv2.GaussianBlur(image_denoise, (5, 5), 0)
        image_canny_edge = cv2.Canny(image_blur, 50, 100)

        lines = cv2.HoughLines(image_canny_edge, 1, np.pi / 180, 100)

        if lines is not None:
            for rho, theta in lines[0]:
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a * rho
                y0 = b * rho
                x1 = int(x0 + 1000 * (-b))
                y1 = int(y0 + 1000 * (a))
                x2 = int(x0 - 1000 * (-b))
                y2 = int(y0 - 1000 * (a))

            cv2.line(image_crop, (x1, y1), (x2, y2), (0, 255, 0), 2)

            if len(lines[0]) >= 1 and np.abs(x1 - x2) < 50 and np.abs(y1 - y2) > 50:
                return image_crop, True

        return image_crop, False

    @staticmethod
    def TemplateMatch(image, template):
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

        result = cv2.matchTemplate(image_gray, template_gray, cv2.TM_CCORR_NORMED)

        (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(result)
        (startX, startY) = maxLoc

        endX = startX + template.shape[1]
        endY = startY + template.shape[0]

        cv2.rectangle(image, (startX, startY), (endX, endY), (0, 255, 0), 3)

        return minVal, maxVal, minLoc, maxLoc

    @staticmethod
    def ShowImage(label, image):
        cv2.namedWindow(label, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(label, int(image.shape[1] * 0.75), int(image.shape[0] * 0.75))
        cv2.imshow(label, image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    @staticmethod
    def ResizeWithAspectRatio(image, width=None, height=None, inter=cv2.INTER_AREA):
        dim = None
        (h, w) = image.shape[:2]

        if width is None and height is None:
            return image
        if width is None:
            r = height / float(h)
            dim = (int(w * r), height)
        else:
            r = width / float(w)
            dim = (width, int(h * r))

        return cv2.resize(image, dim, interpolation=inter)


if __name__ == "__main__":
    Image = PesoImage(
        cv2.imread("./Original.jpg"),
        water_mark_path="./Pictures/WaterMark",
        baybayin_path="./Pictures/Baybayin",
    )

    image, is_detected = Image.WaterMark()
    print(is_detected)
    Image.ShowImage("WaterMark", image)

    image, is_detected = Image.SecurityThread()
    print(is_detected)
    Image.ShowImage("SecurityThread", image)

    image, is_detected = Image.SeeThroughPrint()
    print(is_detected)
    Image.ShowImage("SeeThroughPrint", image)

    image, is_detected = Image.SerialNumber()
    print(is_detected)
    Image.ShowImage("SerialNumber", image)

    print(Image.CalculateR())
