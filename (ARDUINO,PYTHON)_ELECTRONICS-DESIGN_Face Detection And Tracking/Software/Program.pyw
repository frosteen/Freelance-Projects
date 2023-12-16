import sys
from PyQt4 import QtGui, uic, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import threading
import time
import serial
import cv2
import sys
import datetime

#Threading class
class DoThreading(QThread):
    def __init__(self, _func):
        self.func = _func
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):
        self.func()

class MyWindow(QtGui.QMainWindow):
    face_cascade = cv2.CascadeClassifier('assets/haarcascade_frontalface_default.xml') #face classifier
    isCapturing = False
    def __init__(self):
        try: self.close()
        except: pass
        super(MyWindow, self).__init__()
        uic.loadUi('GUI.ui', self)
        self.setFixedSize(self.size())
        self.center()
        self.show()
        self.pushButtonTrack.clicked.connect(self.start_webcam)
        self.pushButtonStop.clicked.connect(self.stop_webcam)
        self.pushButtonCapture.clicked.connect(self.capture_webcam)
        def doStart():
            try:
                file = open("Port.txt","r")
                self.serialCom = file.read() #com port of arduino, you can change this
                file.close()
                self.pushButtonCapture.setEnabled(False)
                self.pushButtonTrack.setEnabled(False)
                self.pushButtonStop.setEnabled(False)
                self.arduino = serial.Serial(self.serialCom, 9600) #connect to arduino through serial communication
                self.labelStatus.setText("Connected to Arduino.")
                time.sleep(3)
                self.pushButtonCapture.setEnabled(False)
                self.pushButtonTrack.setEnabled(True)
                self.pushButtonStop.setEnabled(False)
                self.labelStatus.setText("You can ON the device.")
                time.sleep(3)
                self.labelStatus.setText("")
            except:
                self.labelStatus.setText("Connect Arduino to "+self.serialCom+" then start again.")
                self.pushButtonCapture.setEnabled(False)
                self.pushButtonTrack.setEnabled(False)
                self.pushButtonStop.setEnabled(False)
        self.th = DoThreading(doStart)
        self.th.daemon = True
        self.th.start()

    def capture_webcam(self):
        if self.pushButtonCapture.text() == "CAPTURE":
            self.pushButtonCapture.setText("STOP");
            self.fourcc = cv2.VideoWriter_fourcc(*'XVID') #create a videowriter
            self.out = cv2.VideoWriter('Videos/Captured.avi',self.fourcc, 20.0, (640,480)) #write the video in the video writer
            # and name it with date and time
            self.isCapturing = True
        elif self.pushButtonCapture.text() == "STOP":
            self.pushButtonCapture.setText("CAPTURE");
            self.isCapturing = False
            self.out.release() #stop the video writing
            self.doMessage("Video captured successfully!", "Info")

    ##############################################CAMERA################################################

    def start_webcam(self):
        self.arduino.write("A".encode()) #send character 'A' to arduino
        self.pushButtonTrack.setEnabled(False)
        self.pushButtonStop.setEnabled(True)
        self.pushButtonCapture.setEnabled(True)
        file = open("Device.txt","r")
        self.captureDevice = file.read() #com port of arduino, you can change this
        file.close()

        self.capture=cv2.VideoCapture(int(self.captureDevice))
    
        self.timer=QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start()

    #update the frame
    def update_frame(self):
        ret, self.image = self.capture.read()
        self.image=cv2.flip(self.image, 1)
        if self.isCapturing:
            self.out.write(self.image)
        self.displayImage(self.image, 1)

    def stop_webcam(self):
        try:
            self.pushButtonTrack.setEnabled(True)
            self.pushButtonStop.setEnabled(False)
            self.pushButtonCapture.setEnabled(False)
            self.timer.stop()
            self.capture.release()
            self.arduino.write("D".encode())
        except:
            print("error")

            
    #IMAGE PROCESSING OF FACE
    def displayImage(self, img, window=1):
        gray  = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #convert image to grayscale
        faces = self.face_cascade.detectMultiScale(gray, 1.2) #find the face in grayscale
        if window == 1: #if window opened
            if len(faces) != 0: #find only 1 face
                for (x,y,w,h) in faces:
                    cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),5) #create a rectangle on the face, you can delete this
                    xx = int(x+w/2) #find midpoint of rectangle
                    yy = int(y+h/2) #find midpoint of rectangle
                    center = (xx,yy) #get the center
                    data = "X{0:d}Y{1:d}".format(int(xx), int(yy)) #send midpoint to arduino
                    self.arduino.write(data.encode())
            else:
                    data = "X{0:d}Y{1:d}".format(int(250), int(250)) #if there are more than 1 faces then don't move the camera
                    self.arduino.write(data.encode())
            self.outImage = QImage(img, img.shape[1], img.shape[0], img.strides[0], QImage.Format_RGB888) #convert image to QImage
            self.outImage = self.outImage.rgbSwapped()
            self.labelCam.setPixmap(QPixmap.fromImage(self.outImage)) #show the live image on the Graphical User Interface (GUI)

    ######################################################################################################

    def center(self):
        frameGm = self.frameGeometry()
        screen = QtGui.QApplication.desktop().screenNumber(QtGui.QApplication.desktop().cursor().pos())
        centerPoint = QtGui.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())
        
    def doMessage(self, text, caption):
        msg = QMessageBox(self)
        msg.setText(text)
        msg.setWindowTitle(caption)
        msg.show()
        return msg
    
    def doQuestion(self, text, caption):
        return QMessageBox.question(w, caption, text, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())
