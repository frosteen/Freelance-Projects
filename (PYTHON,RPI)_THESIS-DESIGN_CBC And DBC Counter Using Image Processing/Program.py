#!/usr/bin/python3
import sys
from PyQt4 import QtGui, uic, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import os
import serial
import time
import picamera
import cv2
from picamera.array import PiRGBArray
from threading import Thread
from keras.models import load_model
from keras.preprocessing import image
import numpy as np

directory = "/home/pi/Desktop/PROGRAM/"

# Startup Variables
patientName = None
age = None
Gender = None
patientFolder = None
CPNumber = None
_40xFolder = None
_100xFolder = None
cellsFolder = None
magnification = "40x"  # default
_40xTotal = 0
_100xTotal = 0
validInput = False
camera = picamera.PiCamera()
camera.resolution = (960, 720)
#################

# Results
RBCCount = 0
WBCCount = 0
PlateletCount = 0
Neutrophil = 0
Lympocyte = 0
Monocyte = 0
Eosinophil = 0
Basophil = 0
#################


def imageProcessing():
    global RBCCount
    global WBCCount
    global PlateletCount
    global Neutrophil
    global Lympocyte
    global Monocyte
    global Eosinophil
    global Basophil
    # RBCCount
    for i in range(1, 11):
        markShape = 0
        markerColor = (0, 255, 0)

        raw_image = cv2.imread(_40xFolder + "/" + str(i) + ".png")
        # cv2.imshow("raw",raw_image)
        # img = cv2.imread('sample1.png')

        img = raw_image[225 : 225 + 400, 250 : 250 + 400]
        # cv2.imshow("cropped",img)

        hsv_conv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # cv2.imshow('hsv',hsv_conv)

        # HSV array for thresholding
        rbc_low = np.array([100, 15, 165])
        rbc_high = np.array([140, 50, 218])

        # HSV thresholding
        mask = cv2.inRange(hsv_conv, rbc_low, rbc_high)
        # cv2.imshow("mask",mask)

        # Morphological Transformation
        foreground_eroded = cv2.erode(mask, None, iterations=2)
        foreground_dilated = cv2.dilate(foreground_eroded, None, iterations=2)
        # cv2.imshow("morph",foreground_dilated)

        output = {}
        output["foreground_dilated"] = foreground_dilated

        # contours
        contours = cv2.findContours(
            foreground_dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )[-2]

        # background subtraction
        bgs = cv2.bitwise_and(img, img, mask=foreground_dilated)
        output["bgs"] = bgs

        markedImage = img.copy()

        count = 0
        area = 0

        for contour in contours:
            contourArea = cv2.contourArea(contour)
            if 691200 > contourArea >= 1:
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
        output["area"] = ((area / 676) / 160000) * 10000
        output["count"] = count

        # cv2.imshow("raw",output["markedImage"])
        # cv2.imshow("Thresh",output["foreground_dilated"])
        # cv2.imshow("BGS",output["bgs"])

        output["rbc"] = output["count"]
        RBCCount = RBCCount + float(output["area"])
    RBCCount = RBCCount / 10

    # WBCCount
    for i in range(1, 11):
        markShape = 0
        markerColor = (0, 255, 0)

        img = cv2.imread(_40xFolder + "/" + str(i) + ".png")

        hsv_conv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # cv2.imshow('hsv',hsv_conv)

        # HSV array for thresholding
        wbc_low = np.array([130, 53, 170])
        wbc_high = np.array([151, 240, 225])

        # HSV thresholding
        mask = cv2.inRange(hsv_conv, wbc_low, wbc_high)
        # cv2.imshow("mask",mask)

        # Morphological Transformation
        foreground_eroded = cv2.erode(mask, None, iterations=2)
        foreground_dilated = cv2.dilate(foreground_eroded, None, iterations=4)
        # cv2.imshow("morph",foreground_dilated)

        output = {}
        output["foreground_dilated"] = foreground_dilated

        # contours
        contours = cv2.findContours(
            foreground_dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )[-2]

        # background subtraction
        bgs = cv2.bitwise_and(img, img, mask=foreground_dilated)
        output["bgs"] = bgs

        markedImage = img.copy()

        count = 0
        area = 0

        for contour in contours:
            contourArea = cv2.contourArea(contour)
            if 691200 > contourArea >= 1:
                area += contourArea
                count += 1
                if markShape == 0:
                    (x, y, w, h) = cv2.boundingRect(contour)
                    cv2.rectangle(markedImage, (x, y), (x + w, y + h), markerColor, 2)
                else:
                    ((x, y), radius) = cv2.minEnclosingCircle(contour)
                    cv2.circle(
                        markedImage, (int(x), int(y)), int(radius + 2), markerColor, 2
                    )

        output["markedImage"] = markedImage
        output["area"] = area
        output["count"] = count

        # cv2.imshow("raw",output["markedImage"])
        # cv2.imshow("Thresh",output["foreground_dilated"])
        # cv2.imshow("BGS",output["bgs"])

        output["wbc"] = output["count"]
        cv2.putText(
            output["markedImage"],
            "WBC: {0}".format(output["count"]),
            (0, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.5,
            (255, 255, 255),
            2,
            cv2.LINE_AA,
        )
        output["wbc_proc"] = output["markedImage"]
        WBCCount = WBCCount + float(output["count"])
    WBCCount = (WBCCount / 10) * 2

    # PlateletCount
    for i in range(1, 11):
        markShape = 0
        markerColor = (0, 255, 0)

        img = cv2.imread(_100xFolder + "/" + str(i) + ".png")

        """
        rgb_conv = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #BGR TO RGB

        image_blur = cv2.GaussianBlur(rgb_conv, (7, 7), 0)  #Gaussian Blur
        """

        hsv_conv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # cv2.imshow('hsv',hsv_conv)

        # HSV array for thresholding
        platelet_low = np.array([74, 32, 102])
        platelet_high = np.array([142, 142, 233])

        # HSV thresholding
        mask = cv2.inRange(hsv_conv, platelet_low, platelet_high)
        # cv2.imshow("mask",mask)

        # Morphological Transformation
        foreground_eroded = cv2.erode(mask, None, iterations=3)
        foreground_dilated = cv2.dilate(foreground_eroded, None, iterations=2)
        # cv2.imshow("morph",foreground_dilated)

        output = {}
        output["foreground_dilated"] = foreground_dilated

        # contours
        contours = cv2.findContours(
            foreground_dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )[-2]

        # background subtraction
        bgs = cv2.bitwise_and(img, img, mask=foreground_dilated)
        output["bgs"] = bgs

        markedImage = img.copy()

        count = 0
        area = 0

        for contour in contours:
            contourArea = cv2.contourArea(contour)
            if 100 > contourArea >= 10:
                area += contourArea
                count += 1
                if markShape == 0:
                    (x, y, w, h) = cv2.boundingRect(contour)
                    cv2.rectangle(markedImage, (x, y), (x + w, y + h), markerColor, 2)
                else:
                    ((x, y), radius) = cv2.minEnclosingCircle(contour)
                    cv2.circle(
                        markedImage, (int(x), int(y)), int(radius + 2), markerColor, 2
                    )

        output["markedImage"] = markedImage
        output["area"] = area
        output["count"] = count

        # cv2.imshow("raw",output["markedImage"])
        # cv2.imshow("Thresh",output["foreground_dilated"])
        # cv2.imshow("BGS",output["bgs"])

        output["platelet"] = output["count"]
        cv2.putText(
            output["markedImage"],
            "Platelets: {0}".format(output["count"]),
            (0, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.5,
            (255, 255, 255),
            2,
            cv2.LINE_AA,
        )
        output["platelet_proc"] = output["markedImage"]

        # cv2.imshow("Platelet count",output["platelet_proc"])
        PlateletCount = PlateletCount + float(output["count"])
    PlateletCount = (PlateletCount / 10) * 20

    # CNN
    # image folder
    folder_path = cellsFolder
    # path to model
    model_path = directory + "wbc.model"
    # dimensions of images
    img_width, img_height = 96, 96

    # load the trained model
    model = load_model(model_path)
    model.compile(loss="binary_crossentropy", optimizer="rmsprop", metrics=["accuracy"])

    # load all images into a list
    images = []
    for img in os.listdir(folder_path):
        img = os.path.join(folder_path, img)
        img = image.load_img(img, target_size=(img_width, img_height))
        img = image.img_to_array(img)
        img = np.expand_dims(img, axis=0)
        images.append(img)

    # stack up images list to pass for prediction
    images = np.vstack(images)
    classes = model.predict_classes(images, batch_size=1)
    classesOrig = classes.tolist().copy()
    classes = list(dict.fromkeys(classes))
    classes.sort(reverse=True)
    totalCells = len(classesOrig)
    ordered = []
    for x in classes:
        ordered.append(classesOrig.count(x))
    ordered.sort(reverse=True)
    if len(ordered) > 0:
        Neutrophil = (ordered[0] / totalCells) * 100
    if len(ordered) > 1:
        Lympocyte = (ordered[1] / totalCells) * 100
    if len(ordered) > 2:
        Monocyte = (ordered[2] / totalCells) * 100
    if len(ordered) > 3:
        Eosinophil = (ordered[3] / totalCells) * 100
    if len(ordered) > 4:
        Basophil = (ordered[4] / totalCells) * 100


class DoThreading(QThread):
    def __init__(self, _func):
        self.func = _func
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):
        self.func()


class MyWindow(QtGui.QMainWindow):
    def __init__(self):
        try:
            self.close()
        except:
            pass
        super(MyWindow, self).__init__()
        uic.loadUi(directory + "Main.ui", self)
        self.setFixedSize(self.size())
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.center()
        self.show()
        self.pushButton.clicked.connect(self.captureButton)
        self.pushButton_2.clicked.connect(self.searchButton)
        self.pushButton_3.clicked.connect(self.sendButton)
        self.pushButton_4.clicked.connect(self.resetButton)
        self.pushButton_5.clicked.connect(self.analyzeButton)
        self.Male.toggled.connect(self.MFChange)
        self.Female.toggled.connect(self.MFChange)
        self.radio40.toggled.connect(self.magnificationChange)
        self.radio100.toggled.connect(self.magnificationChange)
        self.port = serial.Serial("/dev/ttyS0", baudrate=115200, timeout=5)
        self.start_webcam()

    def start_webcam(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(1000.0 / 60)

    def update_frame(self):
        rawCapture = PiRGBArray(camera)
        camera.capture(rawCapture, format="rgb")
        self.displayImage(rawCapture.array, 1)

    def stop_webcam(self):
        self.timer.stop()

    def displayImage(self, image, window=1):
        self.outImage = QImage(
            image.data, image.shape[1], image.shape[0], QImage.Format_RGB888
        )
        if window == 1:
            self.label.setPixmap(QPixmap.fromImage(self.outImage))
            self.label.setScaledContents(True)

    def GSMSend(self, nmbr, msg):
        number = nmbr
        MESSAGE = msg
        ##        print(msg)
        self.port.write("AT\r\n".encode())
        time.sleep(1)
        rcv = self.port.read(self.port.inWaiting()).decode("utf-8").strip()
        ##        print(rcv)
        self.port.write("AT+CMGF=1\r\n".encode())  # Select Message format as Text mode
        time.sleep(1)
        rcv = self.port.read(self.port.inWaiting()).decode("utf-8").strip()
        ##        print(rcv)
        self.port.write(('AT+CMGS="' + number + '"\r\n').encode())
        time.sleep(1)
        rcv = self.port.read(self.port.inWaiting()).decode("utf-8").strip()
        ##        print(rcv)
        self.port.write((MESSAGE).encode())  # Message
        time.sleep(1)
        rcv = self.port.read(self.port.inWaiting()).decode("utf-8").strip()
        ##        print(rcv)
        self.port.write("\x1A\r\n".encode())  # Enable to send SMS
        time.sleep(1)
        self.doMessage("Succesfully sent.", "Success")

    def MFChange(self):
        if self.Male.isChecked():
            self.labelRange.setText(
                """Normal Range (Male)

CBC
RBC: 3.80 - 5.40 x 10^12/L
WBC: 5 - 10.0 x 10^9/L
Platelet: 150 - 400 x 10^9/L 

DBC
Neutrophil: 36% - 66%
Lymphocyte: 22% - 40%
Monocyte: 4% - 8%
Eosinophil: 1% - 4%
Basophil: 0% - 1%
"""
            )
        elif self.Female.isChecked():
            self.labelRange.setText(
                """Normal Range (Female)

CBC
RBC: 4.10 - 5.10 x 10^12/L
WBC: 5 - 10.0 x 10^9/L
Platelet: 150 - 400 x 10^9/L 

DBC
Neutrophil: 36% - 66%
Lymphocyte: 22% - 40%
Monocyte: 4% - 8%
Eosinophil: 1% - 4%
Basophil: 0% - 1%
"""
            )

    def magnificationChange(self):
        global magnification
        global validInput
        if self.radio40.isChecked():
            magnification = "40x"
        elif self.radio100.isChecked():
            magnification = "100x"

    def captureButton(self):
        global _40xTotal
        global _100xTotal
        if patientName == None or patientName == "":
            self.doMessage("Name of a patient is required.", "Info")
        elif age == None or age == "0":
            self.doMessage("Age is required.", "Info")
        elif validInput == False:
            self.doMessage("Patient not found.", "Info")
        else:
            _40xTotal = len(os.listdir(_40xFolder))
            _100xTotal = len(os.listdir(_100xFolder))
            _cellsTotal = len(os.listdir(cellsFolder))
            if magnification == "40x" and _40xTotal < 10:
                camera.capture(_40xFolder + "/" + str(_40xTotal + 1) + ".png")
            elif magnification == "100x":
                camera.capture(_100xFolder + "/" + str(_100xTotal + 1) + ".png")
                # WBCDetection
                markShape = 0
                markerColor = (0, 255, 0)

                img = cv2.imread(_100xFolder + "/" + str(_100xTotal + 1) + ".png")

                rgb_conv = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # BGR TO RGB

                image_blur = cv2.GaussianBlur(rgb_conv, (7, 7), 0)  # Gaussian Blur

                hsv_conv = cv2.cvtColor(image_blur, cv2.COLOR_RGB2HSV)
                # cv2.imshow('hsv',hsv_conv)

                # HSV array for thresholding
                wbc_low = np.array([115, 86, 199])
                wbc_high = np.array([151, 222, 255])

                # HSV thresholding
                mask = cv2.inRange(hsv_conv, wbc_low, wbc_high)
                # cv2.imshow("mask",mask)

                # Morphological Transformation
                foreground_eroded = cv2.erode(mask, None, iterations=4)
                foreground_dilated = cv2.dilate(foreground_eroded, None, iterations=10)
                # cv2.imshow("morph",foreground_dilated)

                output = {}
                output["foreground_dilated"] = foreground_dilated

                # contours
                contours = cv2.findContours(
                    foreground_dilated.copy(),
                    cv2.RETR_EXTERNAL,
                    cv2.CHAIN_APPROX_SIMPLE,
                )[-2]

                # background subtraction
                bgs = cv2.bitwise_and(img, img, mask=foreground_dilated)
                output["bgs"] = bgs

                markedImage = img.copy()

                count = 0
                area = 0
                i = 0
                for contour in contours:
                    contourArea = cv2.contourArea(contour)
                    if 691200 > contourArea >= 500:
                        area += contourArea
                        count += 1
                        i += 1
                        if markShape == 0:
                            (x, y, w, h) = cv2.boundingRect(contour)
                            cv2.rectangle(
                                markedImage, (x, y), (x + w, y + h), markerColor, 2
                            )
                            cropped = img[y - 10 : y + h + 15, x - 10 : x + w + 15]
                            cv2.imwrite(
                                cellsFolder
                                + "/"
                                + str(_100xTotal + 1)
                                + str(i)
                                + ".png",
                                cropped,
                            )

                output["markedImage"] = markedImage
                output["area"] = area
                output["count"] = count

                # cv2.imshow("raw",output["markedImage"])
                # cv2.imshow("Thresh",output["foreground_dilated"])
                # cv2.imshow("BGS",output["bgs"])

                output["wbc"] = output["count"]
                ##    cv2.putText(output["markedImage"], "WBC: {0}".format(output["count"]), (0, 50),
                ##                            cv2.FONT_HERSHEY_SIMPLEX,
                ##                            1.5, (255, 255, 255), 2, cv2.LINE_AA)
                output["wbc_proc"] = output["markedImage"]
            else:
                self.doMessage("Capturing images are limited to 10 only.", "Info")
            _40xTotal = len(os.listdir(_40xFolder))
            _100xTotal = len(os.listdir(_100xFolder))
            _cellsTotal = len(os.listdir(cellsFolder))
            self.label_5.setText("40x: " + str(_40xTotal))
            self.label_6.setText("100x: " + str(_100xTotal))
            self.label_21.setText("WBC100x: " + str(_cellsTotal))

    def searchButton(self):
        global patientName
        global age
        global patientFolder
        global _40xFolder
        global _100xFolder
        global cellsFolder
        global _40xTotal
        global _100xTotal
        global validInput
        global Gender

        validInput = False
        self.textEdit_2.setText("")
        patientName = str(self.textEdit.toPlainText())
        age = str(self.spinBox.value())
        if patientName == None or patientName == "":
            self.doMessage("Name of patient is required.", "Info")
        elif age == None or age == "0":
            self.doMessage("Age is required.", "Info")
        else:
            patientFolder = None
            files = os.listdir(directory + "Patients")
            if self.Male.isChecked():
                Gender = "M"
            elif self.Female.isChecked:
                Gender = "F"
            if not os.path.exists(
                directory + "Patients/" + patientName + "-" + age + "-" + Gender
            ):
                isRegister = self.doQuestion(
                    "Patient does not exist. Create a new Patient?", "Register?"
                )
                if isRegister == QMessageBox.Yes:
                    os.mkdir(
                        directory + "Patients/" + patientName + "-" + age + "-" + Gender
                    )
                    os.mkdir(
                        directory
                        + "Patients/"
                        + patientName
                        + "-"
                        + age
                        + "-"
                        + Gender
                        + "/40x"
                    )
                    os.mkdir(
                        directory
                        + "Patients/"
                        + patientName
                        + "-"
                        + age
                        + "-"
                        + Gender
                        + "/100x"
                    )
                    os.mkdir(
                        directory
                        + "Patients/"
                        + patientName
                        + "-"
                        + age
                        + "-"
                        + Gender
                        + "/Cells"
                    )
                    patientFolder = (
                        directory + "Patients/" + patientName + "-" + age + "-" + Gender
                    )
                    _40xFolder = (
                        directory
                        + "Patients/"
                        + patientName
                        + "-"
                        + age
                        + "-"
                        + Gender
                        + "/40x"
                    )
                    _100xFolder = (
                        directory
                        + "Patients/"
                        + patientName
                        + "-"
                        + age
                        + "-"
                        + Gender
                        + "/100x"
                    )
                    cellsFolder = (
                        directory
                        + "Patients/"
                        + patientName
                        + "-"
                        + age
                        + "-"
                        + Gender
                        + "/Cells"
                    )
                    _40xTotal = len(os.listdir(_40xFolder))
                    _100xTotal = len(os.listdir(_100xFolder))
                    _cellsTotal = len(os.listtdir(cellsFolder))
                    self.label_5.setText("40x: " + str(_40xTotal))
                    self.label_6.setText("100x: " + str(_100xTotal))
                    self.label_21.setText("WBC100x: " + str(_cellsTotal))
                    print("Directory ", patientFolder, " Created ")
                    validInput = True
            else:
                patientFolder = (
                    directory + "Patients/" + patientName + "-" + age + "-" + Gender
                )
                _40xFolder = (
                    directory
                    + "Patients/"
                    + patientName
                    + "-"
                    + age
                    + "-"
                    + Gender
                    + "/40x"
                )
                _100xFolder = (
                    directory
                    + "Patients/"
                    + patientName
                    + "-"
                    + age
                    + "-"
                    + Gender
                    + "/100x"
                )
                cellsFolder = (
                    directory
                    + "Patients/"
                    + patientName
                    + "-"
                    + age
                    + "-"
                    + Gender
                    + "/Cells"
                )
                _40xTotal = len(os.listdir(_40xFolder))
                _100xTotal = len(os.listdir(_100xFolder))
                _cellsTotal = len(os.listdir(cellsFolder))
                self.label_5.setText("40x: " + str(_40xTotal))
                self.label_6.setText("100x: " + str(_100xTotal))
                self.label_21.setText("WBC100x: " + str(_cellsTotal))
                print("Directory ", patientFolder, " already exists")
                validInput = True

    def sendButton(self):
        global CPNumber
        global validInput
        CPNumber = str(self.textEdit_2.toPlainText())
        if patientName == None or patientName == "":
            self.doMessage("Name of a patient is required.", "Info")
        elif age == None or age == "0":
            self.doMessage("Age is required.", "Info")
        elif validInput == False:
            self.doMessage("Patient is not found.", "Info")
        elif CPNumber.isdigit() == False or len(CPNumber) != 11:
            self.doMessage("Invalid cellphone number.", "Info")
        else:
            self.GSMSend(
                CPNumber,
                """
Patient's Name: {}
Age: {}
Gender: {}

CBC Result
RBC Count: {}x10^12/L
WBC Count: {}x10^9/L
Platelet Count: {}x10^9/L

DBC Result
Neutrophil: {}%
Lymphocyte: {}%
Monocyte: : {}%
Eosinophil: {}%
Basophil: : {}%
""".format(
                    patientName,
                    age,
                    Gender,
                    RBCCount,
                    WBCCount,
                    PlateletCount,
                    Neutrophil,
                    Lympocyte,
                    Monocyte,
                    Eosinophil,
                    Basophil,
                ),
            )

    def resetButton(self):
        self.textEdit.setText("")
        self.spinBox.setValue(0)
        self.textEdit_2.setText("")
        self.Male.setChecked(True)
        self.Female.setChecked(False)
        self.radio40.setChecked(True)
        self.label_5.setText("40x:")
        self.label_6.setText("100x:")
        self.label_9.setText("RBC:")
        self.label_10.setText("WBC:")
        self.label_11.setText("Platelet:")
        self.label_14.setText("Neutrophil:")
        self.label_16.setText("Lymphocyte:")
        self.label_20.setText("Monocyte:")
        self.label_15.setText("Eosinophil:")
        self.label_13.setText("Basophil:")
        RBCCount = 0
        WBCCount = 0
        PlateletCount = 0
        Neutrophil = 0
        Lympocyte = 0
        Monocyte = 0
        Eosinophil = 0
        Basophil = 0

    def analyzeButton(self):
        print("Analyze")
        global RBCCount
        global WBCCount
        global PlateletCount
        global Neutrophil
        global Neutrophil
        global Lympocyte
        global Monocyte
        global Eosinophil
        global Basophil
        if patientName == None or patientName == "":
            self.doMessage("Name of a patient is required.", "Info")
        elif age == None or age == "0":
            self.doMessage("Age is required.", "Info")
        elif validInput == False:
            self.doMessage("Patient is not found.", "Info")
        elif _40xTotal == 10:
            self.stop_webcam()
            imageProcessing()
            RBCCount = round(RBCCount, 2)
            WBCCount = round(WBCCount, 2)
            PlateletCount = round(PlateletCount, 2)
            Neutrophil = round(Neutrophil, 2)
            Lympocyte = round(Lympocyte, 2)
            Monocyte = round(Monocyte, 2)
            Eosinophil = round(Eosinophil, 2)
            Basophil = round(Basophil, 2)
            if self.Male.isChecked():
                if RBCCount >= 3.80 and RBCCount <= 5.40:
                    self.label_9.setText("RBC: " + str(RBCCount) + "x10^12/L")
                elif RBCCount < 3.80:
                    self.label_9.setText("RBC: " + str(RBCCount) + "x10^12/L" + " L")
                elif RBCCount > 5.40:
                    self.label_9.setText("RBC: " + str(RBCCount) + "x10^12/L" + " H")
                if WBCCount >= 5 and WBCCount <= 10:
                    self.label_10.setText("WBC: " + str(WBCCount) + "x10^9/L")
                elif WBCCount < 5:
                    self.label_10.setText("WBC: " + str(WBCCount) + "x10^9/L" + " L")
                elif WBCCount > 10:
                    self.label_10.setText("WBC: " + str(WBCCount) + "x10^9/L" + " H")
                if Platelet:
                    pass
                self.label_11.setText("Platelet: " + str(PlateletCount) + "x10^9/L")
                self.label_14.setText("Neutrophil: " + str(Neutrophil) + "%")
                self.label_16.setText("Lymphocyte: " + str(Lympocyte) + "%")
                self.label_20.setText("Monocyte: " + str(Monocyte) + "%")
                self.label_15.setText("Eosinophil: " + str(Eosinophil) + "%")
                self.label_13.setText("Basophil: " + str(Basophil) + "%")
            elif self.Female.isChecked():
                pass
            self.start_webcam()
        else:
            self.doMessage("Total 40x and 100x images should be both 10.")

    # TOOLBOX
    def center(self):
        frameGm = self.frameGeometry()
        screen = QtGui.QApplication.desktop().screenNumber(
            QtGui.QApplication.desktop().cursor().pos()
        )
        centerPoint = QtGui.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def doMessage(self, text, caption="Info"):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setText(text)
        msg.setWindowTitle(caption)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.show()
        return msg

    def doQuestion(self, text, caption):
        return QMessageBox.question(
            self, caption, text, QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())
