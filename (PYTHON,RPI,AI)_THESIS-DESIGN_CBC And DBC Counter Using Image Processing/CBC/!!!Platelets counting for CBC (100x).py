import cv2
import numpy as np



markShape = 0
markerColor = (0,255,0)


img = cv2.imread('sample100.png')

"""
rgb_conv = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #BGR TO RGB

image_blur = cv2.GaussianBlur(rgb_conv, (7, 7), 0)  #Gaussian Blur
"""

hsv_conv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
#cv2.imshow('hsv',hsv_conv)

#HSV array for thresholding
platelet_low = np.array([ 75, 0 , 16])
platelet_high = np.array([117 ,190 , 194])

#HSV thresholding
mask = cv2.inRange(hsv_conv,platelet_low,platelet_high)
#cv2.imshow("mask",mask)


#Morphological Transformation
foreground_eroded = cv2.erode(mask,None,iterations = 2)
foreground_dilated = cv2.dilate(foreground_eroded,None,iterations = 2)
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


for contour in contours:
            contourArea = cv2.contourArea(contour)
            if  100 > contourArea >= 1:
                area += contourArea
                count += 1
                if markShape == 0:
                    (x, y, w, h) = cv2.boundingRect(contour)
                    cv2.rectangle(markedImage, (x, y), (x + w, y + h), markerColor, 2)
                else:
                    ((x, y), radius) = cv2.minEnclosingCircle(contour)
                    cv2.circle(markedImage, (int(x), int(y)), int(radius + 2), markerColor, 2)

output["markedImage"] = markedImage
output["area"] = area
output["count"] = count

#cv2.imshow("raw",output["markedImage"])
#cv2.imshow("Thresh",output["foreground_dilated"])
#cv2.imshow("BGS",output["bgs"])


output["platelet"] = output["count"]
cv2.putText(output["markedImage"], "Platelets: {0}".format(output["count"]), (0, 50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.5, (255, 255, 255), 2, cv2.LINE_AA)
output["platelet_proc"] = output["markedImage"]

cv2.imshow("Platelet count",output["platelet_proc"])


if cv2.waitKey(0) == 27:
    cv2.destroyAllWindows()

