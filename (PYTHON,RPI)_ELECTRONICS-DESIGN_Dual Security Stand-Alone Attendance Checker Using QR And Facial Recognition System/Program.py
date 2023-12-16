#!/usr/bin/python3
import sys
from PyQt4 import QtGui, uic, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import threading
import time
import sqlite3
import cv2
from PIL import Image
import numpy as np
import os, shutil
import qrcode
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
from datetime import datetime
import pyzbar.pyzbar as pyzbar
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

##directory = "/home/pi/Desktop/ThesisColloqProgram/"
directory = ""

face_detector = cv2.CascadeClassifier(directory+'haarcascade_frontalface_default.xml')
path = directory+'dataset'
recognizer = cv2.face.LBPHFaceRecognizer_create()
cascadePath = directory+"haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)
font = cv2.FONT_HERSHEY_SIMPLEX
detector = face_detector;

#SETTINGS
confidenceLevel = 40
maxTrain = 20

#EMAILING QR
emailMo = "MapuaUThesisColloquium@gmail.com"
passMo = "tcolloq1234"
subjectMo = "QR CODE THESIS COLLOQUIUM"
textMo = "Please us this QR code for your attendance. Thank you!"

#EMAILING THESIS COLLOQ
subjectMo1 = "THESIS COLLOQUIUM CERTIFICATE"
textMo1 = "Congratulations for attending the Thesis Colloquium!"

runTime = False

class DoThreading(QThread):
    def __init__(self, _func):
        self.func = _func
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):
        self.func()

class MyWindow(QtGui.QMainWindow):
    def sendMailAttach(self,fromaddr,password,toaddr,subject, body,filename):
        msg = MIMEMultipart()         
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = subject         
        msg.attach(MIMEText(body, 'plain'))
        attachment = open(filename, "rb")         
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)         
        msg.attach(part)         
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, password)
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()
        attachment.close()
        
    def __init__(self):
        try:self.close()
        except: pass
        try: self.stop_webcam1()
        except: pass
        super(MyWindow, self).__init__()
        uic.loadUi(directory + 'PREREG.ui', self)
        self.setFixedSize(self.size())
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.center()
        self.show()
        self.pushButton_3.clicked.connect(self.showAttUI)
        self.pushButton_2.clicked.connect(self.showCamUI)
        self.pushButton_4.clicked.connect(self.deleteButtonClicked)
        self.pushButton_5.clicked.connect(self.trainsButtonClicked)
        self.count = 0
        self.startTrain = False
        runTime = False
        self.getAttendance = False
        
    #CAMERA
    def start_webcam(self,name):
        self.capture = cv2.VideoCapture(0)
        self.timer=QTimer(self)
        self.timer.timeout.connect(lambda: self.update_frame(name))
        self.timer.start()

    def update_frame(self,name):
        ret, self.image = self.capture.read()
        self.image=cv2.flip(self.image, 1)
        self.displayImage(self.image, 1, name)

    def stop_webcam(self):
        self.timer.stop()
        self.capture.release()

        
        
    getID = []
    doFace = False
    doQR = False
    id3 = ""
    counter = 0
    def start_webcam1(self):
        self.capture = cv2.VideoCapture(0)
        self.timer=QTimer(self)
        self.timer.timeout.connect(self.update_frame1)
        self.timer.start()

    def update_frame1(self):
        ret, self.image = self.capture.read()
        self.image=cv2.flip(self.image, 1)
        self.displayImage1(self.image, 1)

    def stop_webcam1(self):
        self.timer.stop()
        self.capture.release()
    def displayImage1(self, img, window=1):
        qformat = QImage.Format_Indexed8
        if len(img.shape)==3:
            if(img.shape[2])==4:
                qformat=QImage.Format_RGBA8888
            else:
                qformat=QImage.Format_RGB888

        #FACE RECOG
        if self.getAttendance:
            self.labelName.setText("Name: ")
            self.labelTimeIn.setText("Time In: ")
            self.labelTimeOut.setText("Time Out: ")
            conn = sqlite3.connect(directory+"DATABASE.db")
            c = conn.cursor()
            for x in c.execute("SELECT * FROM REG"):
                self.getID.append(str(x[0])+","+x[1]+","+x[2]+" "+x[3])
            conn.commit()
            conn.close()
##            print(self.getID)
        self.getAttendance = False
        if self.doFace and self.counter == 0:
            self.timer.start()
            self.labelStatus.setText("SHOW FACE TO CAMERA")
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale( 
                gray,
                scaleFactor = 1.2,
                minNeighbors = 5,
               )
            for(x,y,w,h) in faces:
                cv2.rectangle(img, (x,y), (x+w,y+h), (52, 168, 83), 1)
                id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
                # Check if confidence is less them 100 ==> "0" is perfect match 
                if (confidence < 100):
                    id2 = id-1
                    self.id3 = self.getID[id2]
                    id = self.getID[id2].split(",")[1]
                    if (100-confidence) >= confidenceLevel:
                        self.labelName.setText("Name: "+self.getID[id2].split(",")[1]+", "+ self.getID[id2].split(",")[2])
                        self.labelTimeIn.setText("Time In: ")
                        self.labelTimeOut.setText("Time Out: ")
                        self.doFace = False
                        self.doQR = True
                        break
                    confidence = "  {0}%".format(round(100 - confidence))
                else:
                    id = "UNKNOWN"
                    confidence = "  {0}%".format(round(100 - confidence))
                cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 1)
                cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)
        if self.doQR and self.counter == 0:
            self.labelStatus.setText("SHOW QR CODE TO CAMERA")
            decodedObjects = pyzbar.decode(cv2.flip(img,1))
##            print(decodedObjects)
            # Print results
            for obj in decodedObjects:
                print('Type : ', obj.type)
                print('Data : ', obj.data.decode("utf-8") ,'\n')
                if (str(obj.data.decode("utf-8")) == str(self.id3.split(",")[0])):
                    self.doFace = True
                    self.doQR = False
                    conn = sqlite3.connect(directory+"DATABASE.db")
                    c = conn.cursor()
                    time = []
                    total = []
                    for x in c.execute("SELECT * FROM REG WHERE ID="+str(self.id3.split(",")[0])):
                        time = x
                    for x in c.execute("SELECT TimeIn FROM REG"):
                        total.append(x[0])
##                    print(time)
                    conn.commit()
                    conn.close()
                    if str(time[9]) == "None":
                        conn = sqlite3.connect(directory+"DATABASE.db")
                        c = conn.cursor()
                        c.execute("UPDATE REG\
                        SET TimeIn = '"+self.labelTime.text().split("\n")[0]+"', Date='"+self.labelTime.text().split("\n")[1]+"'\
                        WHERE ID="+str(self.id3.split(",")[0]))
                        conn.commit()
                        conn.close()
                        self.labelTimeIn.setText("Time In: "+self.labelTime.text().split("\n")[0])
                        self.labelStatus.setText("SUCCESS! NEXT SCAN FOR '5' SECONDS")
                        actualtotal = 0
                        for x in total:
                            if x != "None":
                                actualtotal = actualtotal + 1
                        self.labelCounter.setText("Counter: "+str(actualtotal))
                        self.counter = 1
                    elif str(time[10]) == "None":
                        conn = sqlite3.connect(directory+"DATABASE.db")
                        c = conn.cursor()
                        c.execute("UPDATE REG\
                        SET TimeOut = '"+self.labelTime.text().split("\n")[0]+"'\
                        WHERE ID="+str(self.id3.split(",")[0]))
                        conn.commit()
                        conn.close()
                        self.labelTimeIn.setText("Time In: "+str(time[9]))
                        self.labelTimeOut.setText("Time Out: "+self.labelTime.text().split("\n")[0])

                        ##CERT TEMPLATE HERE!!##########################

                        msg1 = "MAPÚA UNIVERSITY"
                        msg2 = "Certificate of Completion"
                        msg3 = str(time[2])+" "+str(time[3])+" "+str(time[1])
                        msg4 = self.labelTime.text().split("\n")[1]
                        msg5 = "TIME IN: "+str(time[9])
                        msg6 = "TIME OUT: "+self.labelTime.text().split("\n")[0]
                        s1 = str(time[9])
                        s2 = self.labelTime.text().split("\n")[0]
##                        FMT = '%H:%M:%S'
                        FMT = '%I:%M:%S %p'
                        tdelta = datetime.strptime(s2, FMT) - datetime.strptime(s1, FMT)
                        msg7 = "DURATION: " + str(tdelta)

                        def doText(draw, font, size, msg, width, height):
                            selectFont = ImageFont.truetype(font, size = size)
                            w, h = draw.textsize(msg,font=selectFont)
                            draw.text(((width-w)/2, height), msg, (39, 37, 37), font=selectFont)

                        img = Image.open(directory+"certTemplate.png")
                        draw = ImageDraw.Draw(img)
                        width, height = img.size
                        doText(draw, directory+"Nunito-Light.ttf", 80, msg1, width, 20)
                        doText(draw, directory+"vivaldi.ttf", 60, msg2, width, 150)
                        doText(draw, directory+"Cambria.ttf", 60, msg3, width, 250)
                        doText(draw, directory+"vivaldi.ttf", 60, msg4, width, 350)
                        doText(draw, directory+"Cambria.ttf", 40, msg5, width, 450)
                        doText(draw, directory+"Cambria.ttf", 40, msg6, width, 500)
                        doText(draw, directory+"Cambria.ttf", 40, msg7, width, 550)
                        img.save(directory+'CERTIFICATION.png', "PNG", resolution=100.0)

                        #################################################

                        self.labelStatus.setText("SUCCESS! NEXT SCAN FOR '5' SECONDS")
                        self.counter = 1
                        
                        self.sendMailAttach(emailMo, passMo, str(time[8]),subjectMo1,
                                textMo1,directory+"CERTIFICATION.png")
                    else:
                        self.labelName.setText("Name: ")
                        self.labelTimeIn.setText("Time In: ")
                        self.labelTimeOut.setText("Time Out: ")
                        self.labelStatus.setText("INVALID! NEXT SCAN FOR '5' SECONDS")
                        self.counter = 1
                    break
                else:
                    self.doFace = True
                    self.doQR = False
                    self.labelName.setText("Name: ")
                    self.labelTimeIn.setText("Time In: ")
                    self.labelTimeOut.setText("Time Out: ")
                    self.labelStatus.setText("INVALID! NEXT SCAN FOR '5' SECONDS")
                    self.counter = 1
                    break
        if self.counter != 0 and self.counter <= 100:
            self.counter = self.counter + 1
##            print(self.counter)
        else:
            self.counter = 0
        #########HANGGANG DITO NALANG :(######################################
        self.outImage = QImage(img, img.shape[1], img.shape[0], img.strides[0], qformat)
        self.outImage=self.outImage.rgbSwapped()
        if window == 1:
            self.labelCamera.setPixmap(QPixmap.fromImage(self.outImage))
##            self.labelCamera.setScaledContents(True)
            pass
        
    def displayImage(self, img, window=1, name=""):
        qformat = QImage.Format_Indexed8
        if len(img.shape)==3:
            if(img.shape[2])==4:
                qformat=QImage.Format_RGBA8888
            else:
                qformat=QImage.Format_RGB888
        #PUT FACE HERE
        if self.startTrain:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_detector.detectMultiScale(gray, 1.3, 5)
            for (x,y,w,h) in faces:
                cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 1)     
                self.count += 1
                # Save the captured image into the datasets folder
                cv2.imwrite(directory+"dataset/" + name +"-"+str(self.count) + ".jpg", gray[y:y+h,x:x+w])
##            print(self.count)
            if self.count >= maxTrain:
                self.doMessage("Trained successfully.", "Information")
                self.stop_webcam()
                self.__init__()
        self.outImage = QImage(img, img.shape[1], img.shape[0], img.strides[0], qformat)
        self.outImage=self.outImage.rgbSwapped()
        if window == 1:
            self.label.setPixmap(QPixmap.fromImage(self.outImage))
##            self.label.setScaledContents(True)
            pass

    #TOOLBOX    
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
        return QMessageBox.question(self, caption, text, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

    def showAttUI(self):
        try: self.close()
        except: pass
        super(MyWindow, self).__init__()
        uic.loadUi(directory + 'ATTENDANCE.ui', self)
        self.setFixedSize(self.size())
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.center()
        self.show()
        self.pushButtonBack.clicked.connect(self.__init__)
        self.getAttendance = True
        self.doFace = True
        self.doQR = False
        self.getID = []
        self.id3 = ""
        self.counter = 0
        def doLoop():
            runTime = True
            while runTime:
                self.labelTime.setText(str(datetime.now().strftime('%I:%M:%S %p')+"\n"+str(datetime.now().strftime('%b %d,%Y'))).upper())
                time.sleep(1)
        self.th = DoThreading(doLoop)
        self.th.start()
        self.start_webcam1()

    def showCamUI(self):
        if (self.lineEdit.text() != "" and self.lineEdit_5.text() != "" and self.lineEdit_6.text() != "" and self.lineEdit_2.text() != "" and
            self.lineEdit_3.text() != "" and self.lineEdit_7.text() != "" and self.lineEdit_4.text() != "" and self.lineEdit_8.text() != ""):

            #DO SQL
            getID = ""
            conn = sqlite3.connect(directory+"DATABASE.db")
            c = conn.cursor()
            c.execute("INSERT INTO REG (Surname, Firstname, MiddleInitial, SN, Program, Year, ThesisTitle, Email)\
VALUES ('"+self.lineEdit.text().upper()+"','"+self.lineEdit_5.text().upper()+"','"+self.lineEdit_6.text().upper()+"','"+self.lineEdit_2.text()+"',\
'"+self.lineEdit_3.text().upper()+"','"+self.lineEdit_7.text()+"','"+self.lineEdit_4.text().upper()+"','"+self.lineEdit_8.text()+"');")
##            time.sleep(1)
            for x in c.execute("SELECT * FROM REG WHERE Surname='"+self.lineEdit.text().upper()+"' AND Firstname='"+self.lineEdit_5.text().upper()+
                               "' AND MiddleInitial='"+self.lineEdit_6.text().upper()+"'"):
                getID = x[0]
           
            conn.commit()
            conn.close()

            img = qrcode.make(getID)
            img.save("SECURITY.png")
            self.sendMailAttach(emailMo, passMo, str(self.lineEdit_8.text()),subjectMo,
                                textMo,directory+"SECURITY.png")
            
            try: self.close()
            except: pass
            super(MyWindow, self).__init__()
            uic.loadUi(directory + 'CAMERA.ui', self)
            self.setFixedSize(self.size())
            self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
            self.center()
            self.show()
            self.start_webcam(name="TRAINED FACE"+"-"+str(getID))
            self.pushButton.clicked.connect(self.trainButtonClicked)
        else:
            self.doMessage("Some required fields are empty.", "Information")
    def deleteButtonClicked(self):
        if self.doQuestion("Are you sure you want to reset?", "Question") == QMessageBox.Yes:
            conn = sqlite3.connect(directory+"DATABASE.db")
            c = conn.cursor()
            c.execute("DROP TABLE REG")
            c.execute("""
CREATE TABLE `REG` (
	`ID`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`Surname`	TEXT,
	`Firstname`	TEXT,
	`MiddleInitial`	TEXT,
	`SN`	TEXT,
	`Program`	TEXT,
	`Year`	TEXT,
	`ThesisTitle`	TEXT,
	`Email`	TEXT,
	`TimeIn`	TEXT,
	`TimeOut`	TEXT,
	`Date`	TEXT
);
""")
            self.doMessage("Successfully deleted database.","Information")
            conn.commit()
            conn.close()
            folder = directory+'dataset'
            for the_file in os.listdir(folder):
                file_path = os.path.join(folder, the_file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                    #elif os.path.isdir(file_path): shutil.rmtree(file_path)
                except Exception as e:
                    print(e)

    def trainButtonClicked(self):
##        print("clicked")
        self.startTrain = True
    def trainsButtonClicked(self):
        def getImagesAndLabels(path):
            imagePaths = [os.path.join(path,f) for f in os.listdir(path)]
            faceSamples = []
            ids = []
            for imagePath in imagePaths:
                PIL_img = Image.open(imagePath).convert('L')
                img_numpy = np.array(PIL_img, 'uint8')
                id = int(os.path.split(imagePath)[-1].split("-")[1])
                print(id)
                faces = detector.detectMultiScale(img_numpy)
                for (x,y,w,h) in faces:
                    faceSamples.append(img_numpy[y:y+h,x:x+w])
                    ids.append(id)
            return faceSamples,ids
        faces,ids = getImagesAndLabels(path)
        recognizer.train(faces, np.array(ids))
        recognizer.write(directory+'trainer.json')
        self.doMessage("All faces are trained.", "Information")
        recognizer.read(directory+'trainer.json')

        

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())
