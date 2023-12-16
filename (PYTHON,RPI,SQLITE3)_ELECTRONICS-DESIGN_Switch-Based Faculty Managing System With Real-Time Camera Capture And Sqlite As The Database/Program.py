#!/usr/bin/python3
import sys
from PyQt4 import QtGui, uic, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import threading
import time
import RPi.GPIO as GPIO
import sqlite3
import serial
import cv2

directory = "/home/pi/FacultyManagingSystem/"
pins = [3,5,7,11,13,15,19,21,23,29,31,33,35,37,8,10,12,16,18,22]

try:
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    for x in pins:
        GPIO.setup(x, GPIO.IN)
except:
    GPIO.cleanup()
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    for x in pins:
        GPIO.setup(x, GPIO.IN)

class DoThreading(QThread):
    def __init__(self, _func):
        self.func = _func
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):
        self.func()

class MyWindow(QtGui.QMainWindow):
    isAttendance = False
    isRegister = False
    try:
        ser = serial.Serial('/dev/ttyUSB0',9600)
    except:
        ser = serial.Serial('/dev/ttyUSB1',9600)
    def __init__(self):
        try: self.close()
        except: pass
        super(MyWindow, self).__init__()
        uic.loadUi(directory + 'MainWindow.ui', self)
        self.setFixedSize(self.size())
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.center()
        self.show()
        self.pushButtonADD.clicked.connect(self.mainADDUIShow)
        self.isRegsiter = False
        self.pushButtonOK.clicked.connect(self.pushButtonOKClicked)
        self.pushButtonREQUESTS.clicked.connect(self.pushButtonREQUESTSClicked)
        def update():
            conn = sqlite3.connect(directory+"FacultyDatabase.db")
            c = conn.cursor()
            datas = c.execute("SELECT * FROM Professors")
            savedData = list(datas)
            conn.commit()
            conn.close()
            self.comboBoxProfessor.clear()
            for name in savedData:
                self.comboBoxProfessor.addItem(name[1])
        update()
        def doAttendance():
            self.isAttendance = True
            while self.isAttendance == True:
                time.sleep(0.01)
                for x in pins:
                    readPin = GPIO.input(x)
                    conn = sqlite3.connect(directory+"FacultyDatabase.db")
                    c = conn.cursor()
                    datas = c.execute("SELECT * FROM Professors")
                    savedData = list(datas)
                    conn.commit()
                    conn.close()
                    for x1 in savedData:
                        if str(x) == str(x1[0]):
                            if str(x1[2]) != "Out" and readPin == 0:
                                conn = sqlite3.connect(directory+"FacultyDatabase.db")
                                c = conn.cursor()
                                c.execute("UPDATE Professors SET REMARKS='Out' WHERE PIN='"+str(x1[0])+"'")
                                conn.commit()
                                conn.close()
                                self.pushButtonADD.setEnabled(False)
                                self.pushButtonOK.setEnabled(False)
                                self.labelStatus.setText(x1[1]+" timed out!")
                                time.sleep(1)
                                self.labelStatus.setText("...")
                                self.pushButtonADD.setEnabled(True)
                                self.pushButtonOK.setEnabled(True)
                            elif str(x1[2]) != "In" and readPin == 1:
                                conn = sqlite3.connect(directory+"FacultyDatabase.db")
                                c = conn.cursor()
                                c.execute("UPDATE Professors SET REMARKS='In' WHERE PIN='"+str(x1[0])+"'")
                                conn.commit()
                                conn.close()
                                self.pushButtonADD.setEnabled(False)
                                self.pushButtonOK.setEnabled(False)
                                self.labelStatus.setText(x1[1]+" timed in!")
                                time.sleep(1)
                                self.labelStatus.setText("...")
                                self.pushButtonADD.setEnabled(True)
                                self.pushButtonOK.setEnabled(True)
                                
        self.start_webcam()
        self.th = DoThreading(doAttendance)
        self.th.daemon = True
        self.th.start()


    #CAMERA
    def start_webcam(self):
        self.capture = cv2.VideoCapture(0)
        
        self.timer=QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(2)
        

    def update_frame(self):
        ret, self.image = self.capture.read()
        self.image=cv2.flip(self.image, 1)
        self.displayImage(self.image, 1)

    def stop_webcam(self):
        self.timer.stop()
        self.capture.release()

    def displayImage(self, img, window=1):
        qformat = QImage.Format_Indexed8
        if len(img.shape)==3:
            if(img.shape[2])==4:
                qformat=QImage.Format_RGBA8888
            else:
                qformat=QImage.Format_RGB888
        self.outImage = QImage(img, img.shape[1], img.shape[0], img.strides[0], qformat)
        self.outImage=self.outImage.rgbSwapped()
        if window == 1:
            self.labelCamWindow.setPixmap(QPixmap.fromImage(self.outImage))
            self.labelCamWindow.setScaledContents(True)
        
    def pushButtonREQUESTSClicked(self):
        try: self.close()
        except: pass
        super(MyWindow, self).__init__()
        uic.loadUi(directory + 'MainRequest.ui', self)
        self.setFixedSize(self.size())
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.center()
        self.show()
        self.isRegister = False
        self.stop_webcam()
        self.pushButtonBACK.clicked.connect(self.__init__)
        self.ser.write("...".encode())
        conn = sqlite3.connect(directory+"FacultyDatabase.db")
        c = conn.cursor()
        datas = c.execute("SELECT * FROM Requests")
        savedData = list(datas)
        conn.commit()
        conn.close()
        self.labelName.setText(savedData[0][0])
        self.labelSN.setText(savedData[0][1])
        self.labelRequest.setText(savedData[0][2])
        self.labelProfessor.setText(savedData[0][3])
        self.labelCamReq.setPixmap(QPixmap(directory+"student.png"))
        self.labelCamReq.setScaledContents(True)

    def pushButtonOKClicked(self):
        sName = str(self.lineEditName.text())
        sNumber = str(self.lineEditSN.text())
        sReq = str(self.lineEditRequest.text())
        sProfName = str(self.comboBoxProfessor.currentText())
        if sName == "" or sNumber == "" or sReq == "" or sProfName == "":
            self.doMessage("Some of the fields are empty.", "Info")
        else:
            conn = sqlite3.connect(directory+"FacultyDatabase.db")
            c = conn.cursor()
            datas = c.execute("SELECT * FROM Professors")
            savedData = list(datas)
            conn.commit()
            conn.close()
            for x in savedData:
                if str(x[1]) == sProfName and str(x[2]) == "In":
                    self.ser.write((sProfName.split(",")[0] + "-" + sNumber).encode())
                    conn = sqlite3.connect(directory+"FacultyDatabase.db")
                    c = conn.cursor()
                    c.execute("UPDATE Requests SET NAME='"+sName+"',REQUEST='"+sReq+"',PROFESSOR='"+sProfName+"',SN='"+sNumber+"'\
                            WHERE ID=1")
                    conn.commit()
                    conn.close()                    
                    cv2.imwrite(directory+'student.png', self.image)
                    self.doMessage("Request submitted!\nThe professor is in the faculty.", "Info")
                    break
                elif str(x[1]) == sProfName and str(x[2]) == "Out":
                    self.doMessage("Professor is not in the faculty.", "Info")
                    self.ser.write("...".encode())
                    break
        self.lineEditName.clear()
        self.lineEditSN.clear()
        self.lineEditRequest.clear()

    def mainADDUIShow(self):
        try: self.close()
        except: pass
        super(MyWindow, self).__init__()
        uic.loadUi(directory + 'MainADD.ui', self)
        self.setFixedSize(self.size())
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.center()
        self.show()
        self.pushButtonBACK.clicked.connect(self.__init__)
        self.pushButtonACCEPT.clicked.connect(self.pushButtonACCEPTClicked)
        self.labelStatus1.setText("*Select a button.")
        self.isAttendance = False
        self.stop_webcam()
        def doRegister():
            self.isRegister = True
            while self.isRegister == True:
                time.sleep(0.1)
                for x in pins:
                    readPin = GPIO.input(x)                
                    if readPin == 1:
                        conn = sqlite3.connect(directory+"FacultyDatabase.db")
                        c = conn.cursor()
                        for x1 in c.execute("SELECT * FROM Professors"):
                            if str(x1[0]) == str(x):
                                self.labelName.setText(str(x1[1]))
                                break
                        conn.close()
                        self.labelStatus1.setText(str(x))
                        break
        self.th = DoThreading(doRegister)
        self.th.daemon = True
        self.th.start()

    def pushButtonACCEPTClicked(self):
        conn = sqlite3.connect(directory+"FacultyDatabase.db")
        c = conn.cursor()
        if str(self.labelStatus1.text()) == "*Select a button.":
            self.doMessage("Please select a button.", "Info")
        else:
            try: c.execute("INSERT INTO Professors (PIN, NAME, REMARKS) VALUES ('"+self.labelStatus1.text()+"','"+self.lineEditProfName.text()+"','Out')")
            except: c.execute("UPDATE Professors SET NAME='"+self.lineEditProfName.text()+"' WHERE PIN='"+self.labelStatus1.text()+"'")
            conn.commit()
            conn.close()
            self.doMessage("Added to the database.", "Info")
    
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
