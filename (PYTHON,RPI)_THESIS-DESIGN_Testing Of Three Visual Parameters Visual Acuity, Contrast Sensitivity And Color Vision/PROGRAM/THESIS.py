#!/usr/bin/python3
import sys
from PyQt4 import QtGui, uic, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import speech_recognition as sr
import time
from datetime import datetime
import os
import sqlite3
import random
from PIL import Image, ImageDraw

directory = ""
##directory = "/home/pi/Desktop/"

##VisualAcuity && ContrastSensitivity Settings##
words = ["upward", "downward", "left", "right"]
rows = (str("0"),str("0.10"),str("0.12"),str("0.16"),str("0.20"),str("0.25"),str("0.32"),str("0.40"),str("0.50"),str("0.63"),str("0.80"),str("1.00"),str("1.25"),str("1.60"),str("2.00"))
rows1 = (str("0"),str("6/60"),str("6/48"),str("6/38"),str("6/30"),str("6/24"),str("6/19"),str("6/15"),str("6/12"),str("6/9.5"),str("6/7.5"),str("6/6"),str("6/4.8"),
         str("6/3.8"),str("6/3"))
rows2 = (str("0"),str("20/200"),str("20/160"),str("20/125"),str("20/100"),str("20/80"),str("20/63"),str("20/50"),str("20/40"),str("20/32"),str("20/25"),str("20/20"),
         str("20/16"),str("20/12.5"),str("20/10"))
rows3 = (0,1,0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1,0,-0.1,-0.2,-0.3)
#KAY TRINA
rows4 = (str("0"),str("20/400"), str("20/250"), str("20/200"), str("20/100"), str("20/60"), str("20/50"), str("20/40"), str("20/35"), str("20/30"), str("20/25"), str("20/20"), str("20/15"))
logMars = (str("1.0"),str("0.9"),str("0.8"),str("0.7"),str("0.6"),str("0.5"),str("0.4"),str("0.3"),str("0.2"),str("0.1"),str("0"),str("-0.1"),str("-0.2"))
maxNeedScorePerRow = 3
maxScorePerRow = 5
Sex = None
Age = None
Birthday = None
Address = None

##Colorblindness Result Template Points##4
points = ((86,273),(150,213),(264,171),(368,140),(476,122),(577,140),(692,195),
          (785,301),(813,481),(775,640),(692,738),(588,780),(500,789),(375,746),(286,687),(180,613))

protan = ((0,14),(0,15),(1,13),(1,14),(1,15),(2,12),(2,13),(2,14),(3,11),(3,12),(3,13),(4,10),(4,11),(5,9),(5,10),
	  (6,9),(9,5),(9,6),(10,4),(10,5),(11,3),(11,4),(12,2),(12,3),(13,1),(13,2),(13,3),(14,1),(14,2),(15,1))

deutan = ((2,15),(3,14),(3,15),(4,12),(4,13),(4,14),(5,11),(5,12),(5,13),(6,10),(6,11),(6,12),(7,10),(7,11),(10,6),
	  (10,7),(11,5),(11,6),(11,7),(12,4),(12,5),(12,6),(13,4),(13,5),(14,3),(14,4),(15,2),(15,3))

tritan = ((0,4),(0,5),(0,6),(1,6),(6,1),(7,15),(8,14),(8,15),(9,12),(9,13),(9,14),(10,13),(12,9),(13,9),(13,10),(14,8),
	  (14,9),(15,7),(15,8))

uncategorized = ((0,3),(0,7),(0,8),(0,9),(0,10),(0,11),(0,12),(0,13),(1,4),(1,5),(1,7),(1,8),(1,9),(1,10),(1,11),(1,12),
                 (2,5),(2,6),(2,7),(2,8),(2,9),(2,10),(2,11),(3,6),(3,7),(3,8),(3,9),(3,10),(4,1),(4,7),(4,8),(4,9),(4,15),
		 (5,1),(5,2),(5,8),(5,14),(5,15),(6,2),(6,3),(6,13),(6,14),(6,15),(7,1),(7,2),(7,3),(7,4),(7,12),(7,13),
		 (7,14),(8,1),(8,2), (8,3),(8,4),(8,5),(8,11),(8,12),(8,13),(9,1),(9,2),(9,3),(9,4),(9,15),(10,1),(10,2),
		 (10,3),(10,14),(10,15),(11,1),(11,2),(11,8),(11,14),(11,15),(12,1),(12,7),(12,8),(12,15),(13,6),(13,7),
		 (13,8),(14,5),(14,6),(14,7),(14,10),(14,11),(15,4),(15,5),(15,6),(15,9),(15,10),(15,11),(15,12))

normal = ((0,1),(1,2),(2,3),(3,4),(4,5),(5,6),(6,7),(7,8),(8,9),(9,10),(10,11),(11,12),(12,13),(13,14),(14,15),
          (2,1),(3,2),(4,3),(5,4),(6,5),(7,6),(8,7),(9,8),(10,9),(11,10),(12,11),(13,12),(14,13),(15,14))

medyoNormal = ((0,2),(1,3),(2,4),(3,1),(3,5),(4,2),(4,6),(5,3),(5,7),(6,4),(6,8),(7,5),(7,9),(8,6),(8,10),
               (9,7),(9,11),(10,8),(10,12),(11,9),(11,13),(12,10),(12,14),(13,11),(13,15),(14,12),(15,13))

class DoThreading(QThread):
    def __init__(self, _func):
        self.func = _func
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):
        self.func()

class MyWindow(QtGui.QMainWindow):
    theID = 0
    mode = 0
    def __init__(self):
        try:
            self.close()
            os.system("killall -9 omxplayer.bin &")
        except: pass
        super(MyWindow, self).__init__()
        uic.loadUi(directory + 'MainWindow.ui', self)
        self.setFixedSize(self.size())
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.center()
        self.show()
        self.pushButton.clicked.connect(self.visualAcuityIns)
        self.pushButton_2.clicked.connect(self.contrastSensitivityIns)
        self.pushButton_3.clicked.connect(self.colorBlindnessIns)
        self.vACounting = 0
    def clickPlay(self,msg):
        try:
            os.system("killall -9 omxplayer.bin &")
        except:
            pass
        os.system("omxplayer -o local --no-keys "+msg+" &")

    def repeat(self):
        try:
            self.close()
            os.system("killall -9 omxplayer.bin &")
        except: pass
        super(MyWindow, self).__init__()
        uic.loadUi(directory + 'Repeat.ui', self)
        self.setFixedSize(self.size())
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.center()
        self.show()
        self.pushButton.clicked.connect(self.visualAcuity)
        self.pushButton_3.clicked.connect(lambda: self.clickPlay(directory+"Sounds/"+"RightTurn.m4a"))
        self.clickPlay(directory+"Sounds/"+"RightTurn.m4a")
    
    def visualAcuityIns(self):
        try:
            self.close()
            os.system("killall -9 omxplayer.bin &")
        except: pass
        super(MyWindow, self).__init__()
        uic.loadUi(directory + 'VisualAcuityIns.ui', self)
        self.setFixedSize(self.size())
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.center()
        self.show()
        self.pushButton.clicked.connect(self.applicationForm)
        self.pushButton_2.clicked.connect(self.__init__)
        self.pushButton_3.clicked.connect(lambda: self.clickPlay(directory+"Sounds/"+"VAIns.m4a"))
        self.mode = 1
        self.clickPlay(directory+"Sounds/"+"VAIns.m4a")
        
    def contrastSensitivityIns(self):
        try:
            self.close()
            os.system("killall -9 omxplayer.bin &")
        except: pass
        super(MyWindow, self).__init__()
        uic.loadUi(directory + 'ContrastSensitivityIns.ui', self)
        self.setFixedSize(self.size())
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.center()
        self.show()
        self.pushButton.clicked.connect(self.applicationForm)
        self.pushButton_2.clicked.connect(self.__init__)
        self.pushButton_3.clicked.connect(lambda: self.clickPlay(directory+"Sounds/"+"CSIns.m4a"))
        self.mode = 2
        self.clickPlay(directory+"Sounds/"+"CSIns.m4a")

    def colorBlindnessIns(self):
        try:
            self.close()
            os.system("killall -9 omxplayer.bin &")
        except: pass
        super(MyWindow, self).__init__()
        uic.loadUi(directory + 'ColorBlindnessIns.ui', self)
        self.setFixedSize(self.size())
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.center()
        self.show()
        self.pushButton.clicked.connect(self.applicationForm)
        self.pushButton_2.clicked.connect(self.__init__)
        self.pushButton_3.clicked.connect(lambda: self.clickPlay(directory+"Sounds/"+"CBIns.m4a"))
        self.mode = 3
        self.clickPlay(directory+"Sounds/"+"CBIns.m4a")

    def submittedForm(self):
        global Sex
        global Age
        global Birthday
        global Address
        if self.textEdit.toPlainText() != "" and self.textEdit_2.toPlainText() != "" and self.textEdit_3.toPlainText() != "":
            conn = sqlite3.connect(directory+'Patients.db')
            c = conn.cursor()
            Sex = self.textEdit_4.toPlainText()
            Age = self.textEdit_5.toPlainText()
            Birthday = self.textEdit_6.toPlainText()
            Address = self.textEdit_7.toPlainText()
            c.execute("INSERT INTO Details (Last, Given, Middle, Sex, Age, Birthday, Address)\
                      VALUES ('"+self.textEdit.toPlainText()+"','"+self.textEdit_2.toPlainText()+"','"+self.textEdit_3.toPlainText()+"','\
                        "+self.textEdit_4.toPlainText()+"'\
                        ,'"+self.textEdit_5.toPlainText()+"','"+self.textEdit_6.toPlainText()+"','"+self.textEdit_7.toPlainText()+"')")
            for row in c.execute("SELECT * FROM sqlite_sequence WHERE name='Details'"):
                self.theID = row[1]
                break
            conn.commit()
            conn.close()
            msg = self.doMessage("Submitted successfully!","Info")
            returnValue = msg.exec()
            if returnValue == QMessageBox.Ok:
                if self.mode == 1 or self.mode == 2:
                    self.visualAcuity()
                elif self.mode == 3:
                    self.colorBlindness()
        else:
            self.doMessage("Some required fields are empty.", "Info")
        
    def applicationForm(self):
        try:
            self.close()
            os.system("killall -9 omxplayer.bin &")
        except: pass
        super(MyWindow, self).__init__()
        uic.loadUi(directory + 'ApplicationForm.ui', self)
        self.setFixedSize(self.size())
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.center()
        self.show()
        self.pushButton.clicked.connect(self.submittedForm)

    def submittedCB(self):
        tuloy = False
        for x in range(0,16):
            lbl=self.findChild(QLabel, "ans_"+str(x))
            if lbl.statusTip() == "":
                self.doMessage("Some fields are empty.","Info")
                tuloy = False
                break
            else:
                tuloy = True
        if tuloy:
            
            conn = sqlite3.connect(directory+'Patients.db')
            c = conn.cursor()
            Name = None
            now = datetime.now()
            date = now.strftime("%m-%d-%Y")
            for x in c.execute("SELECT * FROM Details WHERE ID="+str(self.theID)):
                Name = x[1]+", "+x[2]+" "+x[3]
                break
            conn.commit()
            conn.close()
            
            self.groupBox_2.show()
            values = []
            for x in range(0,16):
                lbl=self.findChild(QLabel, "ans_"+str(x))
                values.append(lbl.statusTip())
            im = Image.open(directory+"CBResultTemplate.jpg")
            for i in range(len(values)-1):
                draw = ImageDraw.Draw(im)
                draw.line(points[int(values[i])]+points[int(values[i+1])], fill=(50,50,50), width=5)
            im.save(directory+"Database/CB/"+str(self.theID)+"-"+Name+"-("+date+").jpg", "JPEG")

            ##ADDED##
            notChronoSlopes = []

            #NO OF PROTAN, DEUTAN AND TRITAN CALCULATIONS
            noProtan = 0
            noDeutan = 0
            noTritan = 0
            noUncategorized = 0
            noNormal = 0
            noMedyoNormal = 0

            for i in range(len(values)-1):
                x1 = int(values[i])
                x2 = int(values[i+1])
                if (x1,x2) in protan:
                    noProtan = noProtan + 1
                elif (x1,x2) in deutan:
                    noDeutan = noDeutan + 1
                elif (x1,x2) in tritan:
                    noTritan = noTritan + 1
                elif (x1,x2) in normal:
                    noNormal = noNormal + 1
                elif (x1,x2) in medyoNormal:
                    noMedyoNormal = noMedyoNormal + 1
                elif (x1,x2) in uncategorized:
                    noUncategorized = noUncategorized + 1

            getMax = max([noProtan, noDeutan, noTritan, noUncategorized])
            diag = "Normal"
            
            if noMedyoNormal >= 4:
                diag = "Inclassifiable, needs discrimination test"

            if getMax > 1:
                if noUncategorized == getMax:
                    diag = "Inclassifiable, needs discrimination test"
                if noProtan == getMax:
                    diag = "Protan"
                if noDeutan == getMax:
                    diag = "Deutan"
                if noTritan == getMax:
                    diag = "Tritan"
                
            if ((noProtan > 0 and noDeutan > 0) or (noProtan > 0 and noTritan > 0) or (noTritan > 0 and noDeutan > 0)) and (noProtan == noDeutan or noProtan == noTritan or noDeutan == noTritan):
                diag = "Inclassifiable, needs discrimination test"  
            

            self.label.setText("""Confusion Axis\t\tMajor Crossovers
Protan\t\t\t\t{}
Deutan\t\t\t\t{}
Tritan\t\t\t\t{}
Uncategorized\t\t\t{}

Diagnosis\t{}""".format(noProtan, noDeutan, noTritan, noUncategorized, diag))
            
            with open(directory+"Database/CB/"+str(self.theID)+"-"+Name+"-("+date+").txt", 'w+') as f:
                f.write("""Confusion Axis\t\tMajor Crossovers
Protan\t\t\t\t{}
Deutan\t\t\t\t{}
Tritan\t\t\t\t{}
Uncategorized\t\t\t{}
----------------------------------------
Diagnosis\t{}""".format(noProtan, noDeutan, noTritan, noUncategorized, diag))

    def colorBlindness(self):
        try:
            self.close()
            os.system("killall -9 omxplayer.bin &")
        except: pass
        super(MyWindow, self).__init__()
        uic.loadUi(directory + 'ColorBlindness.ui', self)
        self.setFixedSize(self.size())
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.center()
        self.show()
        self.pushButton.clicked.connect(self.close)
        self.pushButton_2.clicked.connect(self.submittedCB)
        self.groupBox_2.hide()
        self.pushButton_3.clicked.connect(self.__init__)
        
        #DO RANDOM COLORS
        numbers = [i for i in range(1,16)]
        random.shuffle(numbers)

        self.storednumber = None
        
        def clicked(event, lbl):
            if self.storednumber == None and str(lbl.statusTip()) != "":
                self.storednumber = lbl.statusTip()
                lbl.setPixmap(QPixmap())
                lbl.setStatusTip("")
        def clickedans(event, ans):
            if self.storednumber != None and str(ans.statusTip()) == "":
                pixmap = QPixmap(directory+"ColorBlindness/"+str(self.storednumber)+".jpg")
                ans.setPixmap(pixmap)
                ans.setStatusTip(str(self.storednumber))
                self.storednumber = None
            elif self.storednumber != None and str(ans.statusTip()) != "":
                pixmap = QPixmap(directory+"ColorBlindness/"+str(self.storednumber)+".jpg")
                ans.setPixmap(pixmap)
                
                #BUMABALIK ALGO
                currentStatusTip = ans.statusTip()
                counter = 0
                for x in numbers:
                    counter = counter + 1
                    if str(currentStatusTip) == str(x):
                        lbl2=self.findChild(QLabel, "label_"+str(counter))
                        pixmap = QPixmap(directory+"ColorBlindness/"+currentStatusTip+".jpg")
                        lbl2.setPixmap(pixmap)
                        lbl2.setStatusTip(currentStatusTip)
                        break;
                ans.setStatusTip(str(self.storednumber))
                self.storednumber = None
            elif self.storednumber == None:
                self.storednumber = ans.statusTip()
                ans.setStatusTip("")
                ans.setPixmap(QPixmap())
        files = os.listdir(directory+"ColorBlindness")
        counter = 0
        for x in range(1,16):
            pixmap = QPixmap(directory+"ColorBlindness/"+str(numbers[x-1])+".jpg")
            lbl=self.findChild(QLabel, "label_"+str(x))
            lbl.setPixmap(pixmap)
            lbl.setStatusTip(str(numbers[x-1]))

        self.label_1.mousePressEvent = lambda e: clicked(e, self.label_1)
        self.label_2.mousePressEvent = lambda e: clicked(e, self.label_2)
        self.label_3.mousePressEvent = lambda e: clicked(e, self.label_3)
        self.label_4.mousePressEvent = lambda e: clicked(e, self.label_4)
        self.label_5.mousePressEvent = lambda e: clicked(e, self.label_5)
        self.label_6.mousePressEvent = lambda e: clicked(e, self.label_6)
        self.label_7.mousePressEvent = lambda e: clicked(e, self.label_7)
        self.label_8.mousePressEvent = lambda e: clicked(e, self.label_8)
        self.label_9.mousePressEvent = lambda e: clicked(e, self.label_9)
        self.label_10.mousePressEvent = lambda e: clicked(e, self.label_10)
        self.label_11.mousePressEvent = lambda e: clicked(e, self.label_11)
        self.label_12.mousePressEvent = lambda e: clicked(e, self.label_12)
        self.label_13.mousePressEvent = lambda e: clicked(e, self.label_13)
        self.label_14.mousePressEvent = lambda e: clicked(e, self.label_14)
        self.label_15.mousePressEvent = lambda e: clicked(e, self.label_15)

        self.ans_1.mousePressEvent = lambda e: clickedans(e, self.ans_1)
        self.ans_2.mousePressEvent = lambda e: clickedans(e, self.ans_2)
        self.ans_3.mousePressEvent = lambda e: clickedans(e, self.ans_3)
        self.ans_4.mousePressEvent = lambda e: clickedans(e, self.ans_4)
        self.ans_5.mousePressEvent = lambda e: clickedans(e, self.ans_5)
        self.ans_6.mousePressEvent = lambda e: clickedans(e, self.ans_6)
        self.ans_7.mousePressEvent = lambda e: clickedans(e, self.ans_7)
        self.ans_8.mousePressEvent = lambda e: clickedans(e, self.ans_8)
        self.ans_9.mousePressEvent = lambda e: clickedans(e, self.ans_9)
        self.ans_10.mousePressEvent = lambda e: clickedans(e, self.ans_10)
        self.ans_11.mousePressEvent = lambda e: clickedans(e, self.ans_11)
        self.ans_12.mousePressEvent = lambda e: clickedans(e, self.ans_12)
        self.ans_13.mousePressEvent = lambda e: clickedans(e, self.ans_13)
        self.ans_14.mousePressEvent = lambda e: clickedans(e, self.ans_14)
        self.ans_15.mousePressEvent = lambda e: clickedans(e, self.ans_15)

    def visualAcuity(self):
        try:
            self.close()
            os.system("killall -9 omxplayer.bin &")
        except: pass
        super(MyWindow, self).__init__()
        uic.loadUi(directory + 'VisualAcuity.ui', self)
        self.setFixedSize(self.size())
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.center()
        self.show()
        self.pushButton.clicked.connect(self.close)
        self.pushButton_2.clicked.connect(self.__init__)
        self.pushButton_3.clicked.connect(self.repeat)
        self.LeftorRight = ""
        self.vACounting = self.vACounting + 1
        if self.vACounting == 1:
            self.LeftorRight = "Right"
            Eye_Evaluated = "Right"
        elif self.vACounting == 2:
            self.LeftorRight = "Left"
            Eye_Evaluated = "Left"
            self.pushButton_3.setVisible(False)
            self.vACounting = 0
        def done(i):
            pixmap = QPixmap("")
            self.lblcenter.setPixmap(pixmap)
            time.sleep(1)
            if self.mode == 1:
                pixmap = QPixmap(directory+"VisualAcuity/"+str(i))
            elif self.mode == 2:
                pixmap = QPixmap(directory+"ContrastSensitivity/"+str(i))
            self.lblcenter.setPixmap(pixmap)

        def do():
            self.groupBox.hide()
            self.totalScoreAcuity = 0
            self.score = 0
            self.realScore = 0
            old = None
            tick = datetime.now()
            files = ""
            dirName = None
            row = 0
            if self.mode == 1:
                files = os.listdir(directory+"VisualAcuity")
                dirName = "VA"
            elif self.mode == 2:
                files = os.listdir(directory+"ContrastSensitivity")
                dirName = "CS"
            counting = 0
            files.sort()
            os.system("omxplayer -o local --no-keys "+directory+"Sounds/"+"Beep.mp3"+"")
            os.system("omxplayer -o local --no-keys "+directory+"Sounds/"+"Beep.mp3"+"")
            os.system("omxplayer -o local --no-keys "+directory+"Sounds/"+"Beep.mp3"+"")
            for i in files:
                self.emit(SIGNAL('done(QString)'),i)
                print(i)
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    def repeat():
                        while 1:
                            self.label.setText("SAY: ABOVE, BELOW, LEFT, RIGHT")
                            r.adjust_for_ambient_noise(source)
                            audio = r.listen(source)
                            text=""
                            try:
                                text = r.recognize_google(audio, language='en-US')
                                proceed = False
                                if text.replace(" ","") in ["awkward","stopword","popcorn"]:
                                    text = "upward"
                                if text.replace(" ","") in ["laugh", "laughed"]:
                                    text = "left"
                                if self.mode == 1:
                                    text1 = i.strip(".png").split("-")[1]
                                elif self.mode == 2:
                                    text1 = i.strip(".jpg").split("-")[1]
                                if text.find(words[0]) != -1:
                                    text = "upward"
                                    proceed = True
                                if text.find(words[1]) != -1:
                                    text = "downward"
                                    proceed = True
                                if text.find(words[2]) != -1:
                                    text = "left"
                                    proceed = True
                                if text.find(words[3]) != -1:
                                    text = "right"
                                    proceed = True
                                if proceed:
                                    if str(text1) == str(text):
                                        self.label.setText("Moving to the Next..")
                                        self.score = self.score + 1
                                        print("Correct!")
                                        
                                        os.system("omxplayer -o local --no-keys "+directory+"Sounds/"+"Beep.mp3"+"")
                                        break
                                    else:
                                        self.label.setText("Moving to the Next..")
                                        print("Wrong!")
                                        
                                        os.system("omxplayer -o local --no-keys "+directory+"Sounds/"+"Beep.mp3"+"")
                                        break
                                else:
                                    print(text)
                                    self.label.setText("Could not recognize, Please repeat")
                                    time.sleep(1.5)
                            except:
                                print(text)
                                self.label.setText("Could not recognize, Please repeat")
                                time.sleep(1.5)
                                pass
                    repeat()
                counting = counting + 1
                if counting == maxScorePerRow:
                    counting = 0
                    print("Score at "+str(row+1)+": "+str(self.score))
                    self.realScore = self.score
                    if self.score >= maxNeedScorePerRow:
                        row = row + 1
                        self.score = 0
                    else:
                        print("Failed to go Next")
                        break
            tock = datetime.now()
            #SOVLING HERE#
            conn = sqlite3.connect(directory+'Patients.db')
            c = conn.cursor()
            Metric = 0
            LogMAR_Acuity = logMars[row]
            Viewing_Distance = 0
            Decimal_Visual_Acuity = 0
            Correct = self.realScore
            Miss = maxScorePerRow - self.realScore
            Test_Duration = tock - tick
            Name = "-"
            for x in c.execute("SELECT * FROM Details WHERE ID="+str(self.theID)):
                Name = x[1]+", "+x[2]+" "+x[3]
                break
            now = datetime.now()
            Date = now.strftime("%m-%d-%Y")
            ##############
            self.groupBox.show()
            self.groupBox.raise_()
            if self.mode == 1:
                self.label_2.setText("VISUAL ACUITY RESULT")
                output = str(rows4[row]) #20/400 ni trina
            if self.mode == 2:
                self.label_2.setText("CONTRAST SENSITIVITY RESULT")
##                output = str(rows[row]) #Kung gusto niyo 0.10
##                output = str(rows1[row]) #Kung gusto niyo 6/60
                output = str(rows2[row]) #Kung gusto niyo 20/200
##                output = str(rows3[row]) #Kung gusto niyo 1.0
            self.label_3.setText(output)
            self.label_4.setText("Eye Evaluated: {}"
                                 .format(str(Eye_Evaluated)))
            self.label_5.setText("Correct: {}\nMiss: {}"
                                 .format(str(Correct),str(Miss)))
            self.label_6.setText("Name: {}\nDate: {}".format(Name,Date))
            with open(directory+"Database/"+dirName+"/"+str(self.theID)+"-"+Name+"-("+Date+")-"+self.LeftorRight+".txt", 'w+') as f:
                f.write("""Result={}
Eye Evaluated={}
Correct={}
Miss={}
Name={}
Sex={}
Age={}
Birthday={}
Address={}
Date={}""".format(str(output),str(Eye_Evaluated),str(Correct),str(Miss),Name,Sex,Age,Birthday,Address,Date))
        self.th = DoThreading(do)
        self.connect(self, SIGNAL("done(QString)"),done)
        self.th.daemon=True
        self.th.start()

    #TOOLBOX    
    def center(self):
        frameGm = self.frameGeometry()
        screen = QtGui.QApplication.desktop().screenNumber(QtGui.QApplication.desktop().cursor().pos())
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
        return QMessageBox.question(self, caption, text, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())
