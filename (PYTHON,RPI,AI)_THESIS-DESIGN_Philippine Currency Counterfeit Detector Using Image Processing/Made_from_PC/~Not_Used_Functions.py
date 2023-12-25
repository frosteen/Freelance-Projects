    # def WaterMark(self):
    #     "Check if WaterMark can be identified"
    #     image_crop = self.image.copy()[130:self.h-200, 1200:self.w-80]
    #     image_gray = cv2.cvtColor(image_crop, cv2.COLOR_BGR2GRAY)
    #     image_denoise = cv2.fastNlMeansDenoising(image_gray, None, 10, 7, 21)
    #     image_blur = cv2.medianBlur(image_denoise, 5)
    #     image_threshold = cv2.adaptiveThreshold(
    #         image_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    #     white_pixels = np.sum(image_threshold == 255)
    #     black_pixels = np.sum(image_threshold == 0)
    #     r = black_pixels/white_pixels
    #     if r > 0.05:
    #         return image_threshold, True
    #     return image_threshold, False

    
    # def SeeThroughPrint(self):
    #     "Check if see-through print baybayin text exist"
    #     image_crop = self.image.copy()[410:self.h-110, 1180:self.w-40]
    #     image_gray = cv2.cvtColor(image_crop, cv2.COLOR_BGR2GRAY)
    #     image_denoise = cv2.fastNlMeansDenoising(image_gray, None, 10, 7, 21)
    #     image_blur = cv2.medianBlur(image_denoise, 5)
    #     image_threshold = cv2.adaptiveThreshold(
    #         image_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    #     white_pixels = np.sum(image_threshold == 255)
    #     black_pixels = np.sum(image_threshold == 0)
    #     r = black_pixels/white_pixels
    #     if r > 0.20:
    #         return image_threshold, True
    #     return image_threshold, False
