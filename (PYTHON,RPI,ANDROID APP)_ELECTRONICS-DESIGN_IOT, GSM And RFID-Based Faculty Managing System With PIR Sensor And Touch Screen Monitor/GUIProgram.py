#!/usr/bin/python3
import sys
from PyQt4 import QtGui, uic, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import threading
import time
from firebase import firebase
import RPi.GPIO as GPIO
import MFRC522
import random
import datetime
import os
import serial
import re

SERIAL_PORT = "/dev/ttyS0"    # Rasp 3 UART Port
ser = serial.Serial(SERIAL_PORT, baudrate = 115200, timeout = 5)

directory = "/home/pi/FacultyManagingSystem/"
database = firebase.FirebaseApplication('https://facultymanagingsystem.firebaseio.com/', authentication=None)

try:
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(20,GPIO.IN)
  GPIO.setup(21,GPIO.OUT)
  GPIO.setup(16, GPIO.OUT)
except:
  GPIO.cleanup()
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(20,GPIO.IN)
  GPIO.setup(21,GPIO.OUT)
  GPIO.setup(16,GPIO.OUT)

class SimpleMFRC522:

  READER = None;
  
  KEY = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
  BLOCK_ADDRS = [8, 9, 10]
  
  def __init__(self):
    self.READER = MFRC522.MFRC522()
  def read(self):
    id, text = self.read_no_block()
    return id, text

  def read_id(self):
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

class DoThreading(QThread):
    def __init__(self, _func):
        self.func = _func
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):
        self.func()
class MyWindow(QtGui.QMainWindow):

    started = False
          
    def __init__(self):
        try: self.close()
        except: pass
        super(MyWindow, self).__init__()
        uic.loadUi(directory + 'MainMenuUI.ui', self)
        self.setFixedSize(self.size())
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.center()
        self.show()
        self.pushButton_2.clicked.connect(self.pushButton_2_clicked)
        self.pushButton.clicked.connect(self.pushButton_clicked)
        def refreshList(res):
          self.listWidget.clear()
          self.listWidget_2.clear()
          self.listWidget_3.clear()
          if res != None and res["Professors"] != None:
            for k,v in res["Professors"].items():
              if v["Remarks"] == "In":
                if v["School"] == "EE":
                  self.listWidget.addItem(QListWidgetItem(str(v["Name"])))
                if v["School"] == "ECE":
                  self.listWidget_2.addItem(QListWidgetItem(str(v["Name"])))
                if v["School"] == "CPE":
                  self.listWidget_3.addItem(QListWidgetItem(str(v["Name"])))
        res = database.get("",None)
        refreshList(res)
        
        def doAttendance():
          self.isRegistering = False
          isReading = True
          self.isAttendance = True
          while self.isAttendance:
            reader = SimpleMFRC522()
            try:
              id, text = reader.read()
              if id != None:
                res = database.get("",None)
                if res != None:
                  GO = False
                  for k,v in res["Professors"].items():
                    if v["RFID"] == str(id):
                      if (res["Professors"][str(k)]["Remarks"] != "In"):
                        self.labelStatus.setText("Timed In")
                        self.doBuzzer()
                        database.patch("Professors/"+str(k),{'Remarks':'In'})
                        self.labelStatus.setText("")
                      elif (res["Professors"][str(k)]["Remarks"] != "Out"):
                        self.labelStatus.setText("Timed Out")
                        self.doBuzzer()
                        database.patch("Professors/"+str(k),{'Remarks':'Out'})
                        self.labelStatus.setText("")
                      res = database.get("",None)
                      refreshList(res)
                      GO = True
                      break
                  if GO == False:
                    self.labelStatus.setText("NOT REGISTERED!")
                    self.doBuzzer()
                    time.sleep(1)
                    self.labelStatus.setText("")
            finally:
              pass
        self.th = DoThreading(doAttendance)
        self.th.daemon = True
        self.th.start()
            

        def poreber():
          while 1:
            #TIME RESET
            if ((str(datetime.datetime.now().time()).split(':')[0] == "24") and
            (str(datetime.datetime.now().time()).split(':')[1] == "00") and
            (str(datetime.datetime.now().time()).split(':')[2].split(".")[0] == "00")):
              res = database.get("", None)
              dicts = {}
              for k,v in res["Professors"].items():
                dicts.update({str(k):{"Remarks":"Out",
                                     "Announcement":"",
                                      "Name":str(v["Name"]),
                                      "School":str(v["School"])}})
              database.patch("Professors",dicts)

        def pirRead ():
          while 1:
            readIn = GPIO.input(20) 
           ## print(readIn)
            if readIn ==1:
               GPIO.output (21, 1)
               time.sleep(60)
            elif readIn ==0:
              GPIO.output(21, 0)
              time.sleep(0.1)
                 
        def readSMS():
            #SMS READ
            ser.write("AT+CMGF=1\r".encode()) # set to text mode
            time.sleep(1)
            ser.write('AT+CMGDA="DEL ALL"\r'.encode()) # delete all SMS
            time.sleep(1)
            reply = ser.read(ser.inWaiting()).decode() # Clean buf
            while 1:
                reply = ser.read(ser.inWaiting()).decode()
                if reply != "":
                    ser.write("AT+CMGR=1\r".encode())
                    time.sleep(0.5)
                    reply = ser.read(ser.inWaiting()).decode()

                    
                    text = reply.split('\r\n')[3]
                    textList = text.split(' ')
                    textListCopy = textList.copy()
                    rfid = textListCopy[0]
                    del textListCopy[0]
                    newText = " ".join(str(x) for x in textListCopy)
##                    print(rfid, newText)
                    res = database.get("", None)
                    for x in res["Professors"]:
                      if str(x) == str(rfid):
                        database.patch("Professors/"+rfid,{"Announcement":"\""+newText+"\""})
                    
                    time.sleep(.5)
                    ser.write('AT+CMGDA="DEL ALL"\r'.encode()) # delete all
                    time.sleep(.5)
                    ser.read(ser.inWaiting()) # Clear buffer
                    time.sleep(.5)   
        if not self.started:
          self.started = True
          self.th1 = DoThreading(poreber)
          self.th1.daemon = True
          self.th1.start()
          self.th3 = DoThreading(readSMS)
          self.th3.daemon = True
          self.th3.start()
          self.th4 = DoThreading(pirRead)
          self.th4.daemon = True
          self.th4.start()


    def doBuzzer(self):
      def doThiz():
        GPIO.output(16, 1)
        time.sleep(1)
        GPIO.output(16,0)
      self.th11 = DoThreading(doThiz)
      self.th11.Daemon = True
      self.th11.start()

    def pushButton_2_clicked(self):
        self.isAttendance = False
        try: self.close()
        except: pass
        super(MyWindow, self).__init__()
        uic.loadUi(directory + 'AnnouncementUI.ui', self)
        self.setFixedSize(self.size())
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.center()
        self.show()
        self.pushButton_2.clicked.connect(self.__init__)
        res = database.get("",None)
        def getRowName(item):
          for k,v in res["Professors"].items():
            if str(v["Name"]) == str(item.text()):
              self.doMessage(str(v["Announcement"]),str(item.text()))
              break;
        self.listWidget.itemActivated.connect(getRowName)
        self.listWidget_2.itemActivated.connect(getRowName)
        self.listWidget_3.itemActivated.connect(getRowName)
        
        def refreshList(res):
          self.listWidget.clear()
          self.listWidget_2.clear()
          self.listWidget_3.clear()
          for k,v in res["Professors"].items():
            if v["Announcement"] != "":
              if v["School"] == "EE":
                self.listWidget.addItem(QListWidgetItem(v["Name"]))
              if v["School"] == "ECE":
                self.listWidget_2.addItem(QListWidgetItem(v["Name"]))
              if v["School"] == "CPE":
                self.listWidget_3.addItem(QListWidgetItem(v["Name"]))
        refreshList(res)
    cntr = 0
    def pushButton_clicked(self):
        try: self.close()
        except: pass
        super(MyWindow, self).__init__()
        uic.loadUi(directory + 'AdminUI.ui', self)
        self.setFixedSize(self.size())
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.center()
        self.show()
        self.pushButton_2.clicked.connect(self.__init__)
        self.pushButton.clicked.connect(self.pbRegister)
        self.pushButton_3.clicked.connect(self.pbDelete)
        self.pushButton_4.clicked.connect(self.pbKeyboard)
        def doRegister():
            self.isRegistering = True
            self.isAttendance = False
            isReading = True
            while self.isRegistering:
              reader = SimpleMFRC522()
              try:
                id, text = reader.read()
                if id != None:
                  if str(self.label_5.text()) != str("*Please TAP RFID"):
                    os.system('xdotool key Control_L+v')
                  else:
                    self.doBuzzer()
                  self.label_5.setText(str(id))
                  self.label_4.setText("None")
                  res = database.get('',None)
                  self.cntr = 0
                  self.number = None
                  for k,v in res["Professors"].items():
                    if str(v["RFID"]) == str(id):
                      self.number = str(k)
                      self.label_4.setText(str(k)+" - "+str(v["Name"]))
                      index = self.comboBox.findText(res["Professors"][str(k)]["School"], QtCore.Qt.MatchFixedString)
                      if index >= 0:
                        self.comboBox.setCurrentIndex(index)
                      break;
                    self.cntr = self.cntr + 1
              finally:
                pass
        self.th = DoThreading(doRegister)
        self.th.daemon = True
        self.th.start()

    def pbKeyboard(self):
        try: self.close()
        except: pass

    def pbDelete(self):
      database.delete("Professors/"+self.label_5.text(), None)
      self.doMessage("Deleted in the database!", "Info")
      self.label_5.setText("*Please TAP RFID")
      self.label_4.setText("None")
      self.lineEdit.setText("")

    def pbRegister(self):
      if self.number == None:
        database.patch("Professors/eece"+str(self.cntr+1)+"/",{"Name":self.lineEdit.text(),
                                                              "School":self.comboBox.currentText(), "Remarks":"Out",
                                                              "Announcement":"",
                                                              "RFID":self.label_5.text()})
        self.doMessage("Succesfully registered!\nCODE: "+"eece"+str(self.cntr+1), "Info")
        self.label_5.setText("*Please TAP RFID")
        self.label_4.setText("None")
        self.lineEdit.setText("")
      else:
        database.patch("Professors/"+str(self.number)+"/",{"Name":self.lineEdit.text(),
                                                              "School":self.comboBox.currentText(), "Remarks":"Out",
                                                              "Announcement":"",
                                                              "RFID":self.label_5.text()})
        self.doMessage("Succesfully registered!\nCODE: "+str(self.number), "Info")
        self.label_5.setText("*Please TAP RFID")
        self.label_4.setText("None")
        self.lineEdit.setText("")
    
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
