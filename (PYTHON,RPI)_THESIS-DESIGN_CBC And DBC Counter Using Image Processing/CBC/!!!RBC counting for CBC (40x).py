import cv2
import numpy as np



markShape = 0
markerColor = (0,255,0)


raw_image = cv2.imread('sample1.png')
#cv2.imshow("raw",raw_image)
#img = cv2.imread('sample1.png')

img = raw_image[200:200+400, 220:220+400]
#cv2.imshow("cropped",img)



hsv_conv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
#cv2.imshow('hsv',hsv_conv)

#HSV array for thresholding
rbc_low = np.array([ 114, 19, 12])
rbc_high = np.array([255 ,104 , 255])

#HSV thresholding
mask = cv2.inRange(hsv_conv,rbc_low,rbc_high)
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
            if  691200 > contourArea >= 1:
                area += contourArea
                count += 1
                """
                if markShape == 0:
                    (x, y, w, h) = cv2.boundingRect(contour)
                    cv2.rectangle(markedImage, (x, y), (x + w, y + h), markerColor, 2)
                else:
                    ((x, y), radius) = cv2.minEnclosingCircle(contour)
                    cv2.circle(markedImage, (int(x), int(y)), int(radius + 2), markerColor, 2)
                """

output["markedImage"] = markedImage
output["area"] = ((area / 484)/160000)*10000
output["count"] = count

#cv2.imshow("raw",output["markedImage"])
cv2.imshow("Thresh",output["foreground_dilated"])
cv2.imshow("BGS",output["bgs"])


output["rbc"] = output["count"]

cv2.putText(output["markedImage"], "RBC: {0}".format(output["area"]), (0, 50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.5, (255, 255, 255), 2, cv2.LINE_AA)
output["rbc_proc"] = output["markedImage"]

cv2.imshow("RBC count",output["rbc_proc"])


if cv2.waitKey(0) == 27:
    cv2.destroyAllWindows()

