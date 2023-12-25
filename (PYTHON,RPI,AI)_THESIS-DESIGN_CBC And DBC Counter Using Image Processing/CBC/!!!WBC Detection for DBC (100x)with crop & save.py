import cv2
import numpy as np


'''
def nothing(x):
    pass
'''


markShape = 0
markerColor = (0,255,0)


img = cv2.imread('S1 (7).jpg')

rgb_conv = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #BGR TO RGB

image_blur = cv2.GaussianBlur(rgb_conv, (7, 7), 0)  #Gaussian Blur

hsv_conv = cv2.cvtColor(image_blur,cv2.COLOR_RGB2HSV)
#cv2.imshow('hsv',hsv_conv)


#HSV array for thresholding
wbc_low = np.array([ 115, 79 , 14])
wbc_high = np.array([151, 255 , 225])

#HSV thresholding
mask = cv2.inRange(hsv_conv,wbc_low,wbc_high)
#cv2.imshow("mask",mask)


#Morphological Transformation
foreground_eroded = cv2.erode(mask,None,iterations = 4)
foreground_dilated = cv2.dilate(foreground_eroded,None,iterations = 8)
#cv2.imshow("morph",foreground_dilated)

output = {}
output["foreground_dilated"] = foreground_dilated

#contours
contours = cv2.findContours(foreground_dilated.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]

#background subtraction
bgs = cv2.bitwise_and(img,img,mask = foreground_dilated)
output["bgs"] = bgs

markedImage = img.copy()

count = 0
area = 0
i = 0

for contour in contours:
            contourArea = cv2.contourArea(contour)
            if  691200 > contourArea >= 1:
                area += contourArea
                count += 1
                i += 1
                if markShape == 0:
                    (x, y, w, h) = cv2.boundingRect(contour)
                    cv2.rectangle(markedImage, (x, y), (x + w, y + h), markerColor, 2)
                    cropped = img[y:y+h+10,x:x+w+10]
                    cv2.imwrite("CROPPPPPPED{}.png".format(i), cropped)

output["markedImage"] = markedImage
output["area"] = area
output["count"] = count

#cv2.imshow("raw",output["markedImage"])
#cv2.imshow("Thresh",output["foreground_dilated"])
#cv2.imshow("BGS",output["bgs"])


output["wbc"] = output["count"]
cv2.putText(output["markedImage"], "WBC: {0}".format(output["count"]), (0, 50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.5, (255, 255, 255), 2, cv2.LINE_AA)
output["wbc_proc"] = output["markedImage"]

cv2.imshow("WBC count",output["wbc_proc"])


if cv2.waitKey(0) == 27:
    cv2.destroyAllWindows()

"""
key = cv2.waitKey(1)
if key == 27:
    break
"""

