#!/usr/bin/python3
import sys
from PyQt4 import QtGui, uic, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import threading
import RPi.GPIO as GPIO
import MFRC522
import time
import sqlite3
import serial
import cv2

directory = "/home/pi/FacultyManagingSystem/"

reading = False

try:
  GPIO.setmode(GPIO.BCM)
  GPIO.setwarnings(False)
  GPIO.setup(21, GPIO.OUT)
  GPIO.output(21, 0)
except:
  GPIO.cleanup()
  GPIO.setmode(GPIO.BCM)
  GPIO.setwarnings(False)
  GPIO.setup(21, GPIO.OUT)
  GPIO.output(21, 0)

class SimpleMFRC522:

  READER = None;
  
  KEY = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
  BLOCK_ADDRS = [8, 9, 10]
  
  def __init__(self):
    self.READER = MFRC522.MFRC522()
  
  def read(self):
      global reading
      id, text = self.read_no_block()
      reading = True
      while not id and reading:
          id, text = self.read_no_block()  
      return id, text

  def read_id(self):
    id = self.read_id_no_block()
    while not id:
      id = self.read_id_no_block()
    return id

  def read_id_no_block(self):
      (status, TagType) = self.READER.MFRC522_Request(self.READER.PICC_REQIDL)
      if status != self.READER.MI_OK:
          return None, None
      (status, uid) = self.READER.MFRC522_Anticoll()
      if status != self.READER.MI_OK:
          return None, None
      return self.uid_to_num(uid)
  
  def read_no_block(self):
    (status, TagType) = self.READER.MFRC522_Request(self.READER.PICC_REQIDL)
    if status != self.READER.MI_OK:
        return None, None
    (status, uid) = self.READER.MFRC522_Anticoll()
    if status != self.READER.MI_OK:
        return None, None
    id = self.uid_to_num(uid)
    self.READER.MFRC522_SelectTag(uid)
    status = self.READER.MFRC522_Auth(self.READER.PICC_AUTHENT1A, 11, self.KEY, uid)
    data = []
    text_read = ''
    if status == self.READER.MI_OK:
        for block_num in self.BLOCK_ADDRS:
            block = self.READER.MFRC522_Read(block_num) 
            if block:
            		data += block
        if data:
             text_read = ''.join(chr(i) for i in data)
    self.READER.MFRC522_StopCrypto1()
    return id, text_read
    

    
  def write(self, text):
      id, text_in = self.write_no_block(text)        
      while not id:
          id, text_in = self.write_no_block(text)  
      return id, text_in


  def write_no_block(self, text):
      (status, TagType) = self.READER.MFRC522_Request(self.READER.PICC_REQIDL)
      if status != self.READER.MI_OK:
          return None, None
      (status, uid) = self.READER.MFRC522_Anticoll()
      if status != self.READER.MI_OK:
          return None, None
      id = self.uid_to_num(uid)
      self.READER.MFRC522_SelectTag(uid)
      status = self.READER.MFRC522_Auth(self.READER.PICC_AUTHENT1A, 11, self.KEY, uid)
      self.READER.MFRC522_Read(11)
      if status == self.READER.MI_OK:
          data = bytearray()
          data.extend(bytearray(text.ljust(len(self.BLOCK_ADDRS) * 16).encode('ascii')))
          i = 0
          for block_num in self.BLOCK_ADDRS:
            self.READER.MFRC522_Write(block_num, data[(i*16):(i+1)*16])
            i += 1
      self.READER.MFRC522_StopCrypto1()
      return id, text[0:(len(self.BLOCK_ADDRS) * 16)]
      
  def uid_to_num(self, uid):
      n = 0
      for i in range(0, 5):
          n = n * 256 + uid[i]
      return n

reader = SimpleMFRC522()
isAttendance = False
isRegister = False

class DoThreading(QThread):
    def __init__(self, _func):
        self.func = _func
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):
        self.func()

class MyWindow(QtGui.QMainWindow):
    try:
        ser = serial.Serial('/dev/ttyUSB0',9600)
    except:
        ser = serial.Serial('/dev/ttyUSB1',9600)
        
    #RESET ATTENDANCE    
    conn = sqlite3.connect(directory+"FacultyDatabase.db")
    c = conn.cursor()
    c.execute("UPDATE Professors SET Remarks='Out'")
    conn.commit()
    conn.close()
    
    def __init__(self):
        try: self.close()
        except: pass
        global isRegister
        global reading
        reading = False
        isRegister = False
        super(MyWindow, self).__init__()
        uic.loadUi(directory + 'MainMenu.ui', self)
        self.setFixedSize(self.size())
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.center()
        self.show()
        self.labelStatus.setText("...")
        self.pushButtonRegister.clicked.connect(self.loadRegisterUI)
        self.pushButtonSubmit.clicked.connect(self.pushButtonSubmitClicked)
        def refreshComboBox():
            self.comboBoxProfessor.clear()
            conn = sqlite3.connect(directory+'FacultyDatabase.db')
            c = conn.cursor()
            for x in c.execute("SELECT * FROM Professors"):
              self.comboBoxProfessor.addItem(x[1])
            conn.commit()
            conn.close()
        refreshComboBox()
        def updateStatusText(val):
            self.labelStatus.setText(val)
        def runAttendance():
            global isAttendance
            isAttendance = True
            while isAttendance:
                try:
                    if isAttendance:
                        id, text = reader.read()
                        conn = sqlite3.connect(directory+'FacultyDatabase.db')
                        c = conn.cursor()
                        counter = 0
                        collection = []
                        for x in c.execute("SELECT * FROM Professors"):
                            collection.append(x[0])
                            if str(x[0]) == str(id):
                                if str(x[2]) == "Out":
                                    self.emit(SIGNAL('Update'), x[1]+" successfully timed in!")
                                    c.execute("UPDATE Professors \
                                            SET REMARKS = 'In' \
                                            WHERE ID = '"+(str(x[0]))+"'")
                                    self.pushButtonRegister.setEnabled(False)
                                    self.pushButtonSubmit.setEnabled(False)
                                    self.pushButtonView.setEnabled(False)
                                    GPIO.output(21, 1)
                                    time.sleep(2)
                                    GPIO.output(21, 0)
                                    self.pushButtonRegister.setEnabled(True)
                                    self.pushButtonSubmit.setEnabled(True)
                                    self.pushButtonView.setEnabled(True)
                                    break
                                elif str(x[2]) == "In":
                                    self.emit(SIGNAL('Update'), x[1]+" successfully timed out!")
                                    c.execute("UPDATE Professors \
                                            SET REMARKS = 'Out' \
                                            WHERE ID = '"+(str(x[0]))+"'")
                                    self.pushButtonRegister.setEnabled(False)
                                    self.pushButtonSubmit.setEnabled(False)
                                    self.pushButtonView.setEnabled(False)
                                    GPIO.output(21, 1)
                                    time.sleep(2)
                                    GPIO.output(21, 0)
                                    self.pushButtonRegister.setEnabled(True)
                                    self.pushButtonSubmit.setEnabled(True)
                                    self.pushButtonView.setEnabled(True)
                                    break
                            counter = counter + 1
                        if int(counter) == int(len(collection)):
                            self.emit(SIGNAL('Update'), "RFID can't be found in the Faculty Database.")
                            self.pushButtonRegister.setEnabled(False)
                            self.pushButtonSubmit.setEnabled(False)
                            self.pushButtonView.setEnabled(False)
                            GPIO.output(21, 1)
                            time.sleep(3)
                            GPIO.output(21, 0)
                            self.pushButtonRegister.setEnabled(True)
                            self.pushButtonSubmit.setEnabled(True)
                            self.pushButtonView.setEnabled(True)
                        conn.commit()
                        conn.close()
                        self.emit(SIGNAL('Update'), "...")
                finally:
                    pass
                  
        self.th = DoThreading(runAttendance)
        self.th.daemon = True
        self.th.start()
        self.connect(self, SIGNAL('Update'), updateStatusText)
        self.pushButtonView.clicked.connect(self.pushButtonViewClicked)
        self.start_webcam()

    #CAMERA
    def start_webcam(self):
        self.capture = cv2.VideoCapture(0)
        self.timer=QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start()

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
            self.labelCamMain.setPixmap(QPixmap.fromImage(self.outImage))
            self.labelCamMain.setScaledContents(True)

    def pushButtonViewClicked(self):
        try: self.close()
        except: pass
        global isAttendance
        global reading
        reading = False
        isAttendance = False
        self.stop_webcam()
        super(MyWindow, self).__init__()
        uic.loadUi(directory + 'View.ui', self)
        self.setFixedSize(self.size())
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.center()
        self.show()
        self.pushButtonBack.clicked.connect(self.__init__)
        conn = sqlite3.connect(directory+'FacultyDatabase.db')
        c = conn.cursor()
        savedData = list(c.execute("SELECT * FROM Requests"))
        conn.commit()
        conn.close()
        self.ser.write("...".encode())
        self.labelName.setText(savedData[0][0])
        self.labelStudentNumber.setText(savedData[0][1])
        self.labelRequest.setText(savedData[0][2])
        self.labelProfessor.setText(savedData[0][3])
        self.labelCamView.setPixmap(QPixmap(directory+"student.jpg"))
        self.labelCamView.setScaledContents(True)

    def pushButtonSubmitClicked(self):
        name = self.lineEditName.text()
        sn = self.lineEditStudentNumber.text()
        req = self.lineEditRequest.text()
        prof = self.comboBoxProfessor.currentText()
        if name == "" or sn == "" or req == "" or prof == "":
            self.doMessage("Please fill up all the fields.", "Info")
        else:
            conn = sqlite3.connect(directory+"FacultyDatabase.db")
            c = conn.cursor()
            datas = c.execute("SELECT * FROM Professors")
            savedData = list(datas)
            conn.commit()
            conn.close()
            for x in savedData:
                if str(x[1]) == prof and str(x[2]) == "In":
                    self.ser.write((prof.split(",")[0] + "-" + sn).encode())
                    conn = sqlite3.connect(directory+"FacultyDatabase.db")
                    c = conn.cursor()
                    c.execute("UPDATE Requests SET Name='"+name+"',Request='"+req+"',Professor='"+prof+"',StudentNumber='"+sn+"'\
                            WHERE ID=1")
                    conn.commit()
                    conn.close()
                    self.doMessage("Professor is in the faculty.\nPlease wait.", "Info")
                    break
                elif str(x[1]) == prof and str(x[2]) == "Out":
                    self.doMessage("Professor is not in the faculty.", "Info")
                    self.ser.write("...".encode())
                    break
        self.lineEditName.clear()
        self.lineEditStudentNumber.clear()
        self.lineEditRequest.clear()
        cv2.imwrite(directory+"student.jpg", self.image)

    def loadRegisterUI(self):
        self.close()
        global isAttendance
        global reading
        reading = False
        isAttendance = False
        self.stop_webcam()
        super(MyWindow, self).__init__()
        uic.loadUi(directory + 'Register.ui', self)
        self.setFixedSize(self.size())
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.center()
        self.show()
        self.pushButtonBack.clicked.connect(self.__init__)
        self.pushButtonRegister.clicked.connect(self.pushButtonRegisterClicked)
        def updateStatusLabel(val):
            self.labelRFID.setText(str(val))
            self.lineEditName.setEnabled(True)
            self.pushButtonRegister.setEnabled(True)
        def runRegister():
            global isRegister
            isRegister = True
            while isRegister:
                try:
                    if isRegister:
                        id, text = reader.read()
                        saveId = id
                        self.emit(SIGNAL('UpdateID'), saveId)
                        GPIO.output(21, 1)
                        self.pushButtonBack.setEnabled(False)
                        self.labelStatus1.setText("You can now remove the RFID.")
                        conn = sqlite3.connect(directory+'FacultyDatabase.db')
                        c = conn.cursor()
                        for x in c.execute("SELECT * FROM Professors"):
                          if str(x[0]) == str(saveId):
                            self.labelOldName.setText(str(x[1]))
                            break
                        conn.commit()
                        conn.close()
                        time.sleep(2)
                        self.pushButtonBack.setEnabled(True)
                        GPIO.output(21, 0)
                        self.labelStatus1.setText("")
                finally:
                    pass
                
        self.th = DoThreading(runRegister)
        self.connect(self, SIGNAL('UpdateID'), updateStatusLabel)
        self.th.start()

    def pushButtonRegisterClicked(self):
        global isRegister
        isRegister = False
        conn = sqlite3.connect(directory+'FacultyDatabase.db')
        c = conn.cursor()
        try:
            c.execute("INSERT INTO Professors (ID, NAME, REMARKS) VALUES ('"+(self.labelRFID.text())+"','"+(self.lineEditName.text())+"','Out')")
        except:
            c.execute(" UPDATE Professors \
                    SET NAME = '"+(self.lineEditName.text())+"', REMARKS = 'Out' \
                    WHERE ID = '"+(self.labelRFID.text())+"'")
        conn.commit()
        conn.close()
        self.labelOldName.setText(str(self.lineEditName.text()))
        self.doMessage("Registered successfully!", "Info")
        
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
