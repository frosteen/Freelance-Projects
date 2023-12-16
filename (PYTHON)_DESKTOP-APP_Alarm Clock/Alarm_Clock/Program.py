#!/usr/bin/python3

# Built-in Libraries
import sys
import os
import sqlite3
from datetime import datetime
from datetime import timedelta
import time

# Supported Libraries
import sounddevice as sd
import soundfile as sf
from PyQt5 import QtWidgets, QtGui, QtCore, uic
from scipy.io.wavfile import write

# Global Configurations
directory = "./" # get current directory
fs = 48000 # samplerate
duration = 15 # recording duration
database = directory + "data.db" # database
minutesAlarm = ['15','30','45','00'] # Will trigger alarm every 15 seconds

# Apply Global Configurations (Don't Edit)
sd.default.samplerate = fs
repeats = ('Mon','Tue','Wed','Thu','Fri','Sat','Sun')
sd.default.channels = 2
alarmRunning = False
isRepeatingAlarms = False
isFixedDateAlarms = False

# Query device, and use existing
query_devices = str(sd.query_devices()).split('\n')
for x in query_devices:
    if x.find(">") != -1:
        sd.default.device = int(x[3]), None

# Multithreading
class DoThreading(QtCore.QThread):
    def __init__(self, _func):
        self.func = _func
        QtCore.QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):
        self.func()

# MainWindow
class Window(QtWidgets.QMainWindow):
    def __init__(self):
        try: self.close()
        except: pass
        super(Window, self).__init__()
        uic.loadUi(directory + 'Main.ui', self)
        self.setFixedSize(self.size())
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.center()
        self.show()

        # Other Events
        self.pushButton.clicked.connect(self.recordButton)
        self.pushButton_2.clicked.connect(self.playButton)
        self.pushButton_3.clicked.connect(self.saveButton)
        self.pushButton_8.clicked.connect(self.itemPlayButton)
        self.pushButton_9.clicked.connect(self.itemDeleteButton)
        self.listWidget.itemClicked.connect(self.listWidgetRecordItem)
        self.tabWidget.currentChanged.connect(self.tabWidgetCurrentChanged)

        # Fixed Date Alarm Events
        self.pushButton_6.clicked.connect(self.addFixedDateAlarm)
        self.pushButton_4.clicked.connect(self.selectSoundFixedDateAlarm)
        self.pushButton_10.clicked.connect(self.deleteItemFixedDateAlarm)
        self.listWidget_2.itemClicked.connect(self.listWidgetFixedDateAlarm)

        # Repeating Alarm Events
        self.pushButton_7.clicked.connect(self.addRepeatingAlarm)
        self.pushButton_5.clicked.connect(self.selectSoundRepeatingAlarm)
        self.pushButton_11.clicked.connect(self.deleteItemRepeatingAlarm)
        self.listWidget_3.itemClicked.connect(self.listWidgetRepeatingAlarm)

        # Initial Functions
        self.refreshRecords()
        self.refreshFixedDateAlarm()
        self.refreshRepeatingAlarm()
        self.tabWidgetCurrentChanged()

        # Clock Function   
        def runClock():
            global alarmRunning
            global isRepeatingAlarms
            global isFixedDateAlarms
            rSound1 = None
            fSound1 = None

            # PlaySound Thread
            def playSound():
                global alarmRunning
                global isRepeatingAlarms
                global isFixedDateAlarms
                if isRepeatingAlarms:
                    data, fs = sf.read(rSound1)
                    isRepeatingAlarms = False
                    sd.play(data,fs)
                    time.sleep(14.5)
                    sd.stop()
                    alarmRunning = False
                    self.label_8.setText("-")
                elif isFixedDateAlarms:
                    data, fs = sf.read(fSound1)
                    isFixedDateAlarms = False
                    sd.play(data,fs)
                    time.sleep(14.5)
                    sd.stop()
                    alarmRunning = False
                    self.label_8.setText("-")

            # Check Fixed Date Alarms and Repeating Alarms, and Update Clock
            while 1:
                # Get Current Date and Time                
                now = datetime.now()
                
                timeNow = now.strftime("%I:%M:%S %p")
                dateNow =  now.strftime("%A, %B %d, %Y")
                self.label.setText(timeNow)
                self.label_9.setText(dateNow)

                # Compare Time to Alarms
                timeNowCompare = now.strftime("%I:%M %p")
                timeWeekDayCompare = now.strftime("%a")
                theSeconds = now.strftime("%S")
                dateNowCompare = now.strftime("%m/%d/%Y")

                # Get All Fixed Date and Repeating Alarms
                fixedDateAlarms = self.sqlCursor("SELECT * FROM 'Fixed Date Alarm'")
                repeatingAlarms = self.sqlCursor("SELECT * FROM 'Repeating Alarm'")

                if theSeconds in minutesAlarm and not alarmRunning:
                    if not isRepeatingAlarms:
                        for x in repeatingAlarms:
                            rID, rName, rDate, rSound, rRepeat = x
                            for x in rRepeat.split(", "):
                                if str(rDate) == str(timeNowCompare) and x == str(timeWeekDayCompare):
                                    rSound1 = rSound
                                    alarmRunning = True
                                    isRepeatingAlarms = True
                                    self.label_8.setText(str(rName))
                                    th = DoThreading(playSound)
                                    th.daemon = True
                                    th.start()
                                    break
                    if not isFixedDateAlarms:
                        for x in fixedDateAlarms:
                            fID, fName, fDate, fSound = x
                            fTime = fDate.split(" ")[1] + " " + fDate.split(" ")[2]
                            fMMDDYY = fDate.split(" ")[0]
                            if str(fTime) == str(timeNowCompare) and str(fMMDDYY) == str(dateNowCompare):
                                fSound1 = fSound
                                alarmRunning = True
                                isFixedDateAlarms = True
                                self.label_8.setText(str(fName))
                                th = DoThreading(playSound)
                                th.daemon = True
                                th.start()
                                if theSeconds == '45':
                                    self.sqlExec("DELETE FROM 'Fixed Date Alarm' WHERE ID = {0}".format(str(fID)))
                                    self.refreshFixedDateAlarm()
                                    break
                time.sleep(0.01)

        self.th = DoThreading(runClock)
        self.th.daemon = True
        self.th.start()

    # Refresh List View Functions
    def refreshRecords(self):
        self.records = os.listdir(directory + "Records/")
        self.listWidget.clear()
        self.listWidget.addItems(self.records)
        
    def refreshFixedDateAlarm(self):
        alarms = self.sqlCursor("SELECT * FROM 'Fixed Date Alarm'")
        self.listWidget_2.clear()
        if len(alarms) != 0:
            for x in alarms:
                self.listWidget_2.addItem("ID: " + str(x[0]) + "\n" + "Name: " + x[1] + "\n" + "Date: " + x[2] + "\n" + "Sound: " + x[3].split("/")[-1])

    def refreshRepeatingAlarm(self):
        alarms = self.sqlCursor("SELECT * FROM 'Repeating Alarm'")
        self.listWidget_3.clear()
        if len(alarms) != 0:
            for x in alarms:
                self.listWidget_3.addItem("ID: " + str(x[0]) + "\n" + "Name: " + x[1] + "\n" + "Date: " + x[2] + "\n" + "Repeat: " + x[4] + "\n" + "Sound: " + x[3].split("/")[-1])

    ## Widget Functions
            
    # Fixed Date Alarm Functions
    def listWidgetFixedDateAlarm(self, item):
        self.itemFixedDateAlarm = str(item.text())
    
    def deleteItemFixedDateAlarm(self):
        if self.itemFixedDateAlarm != None:
            ID = self.itemFixedDateAlarm.split("\n")[0].split(": ")[1]
            self.sqlExec("DELETE FROM 'Fixed Date Alarm' WHERE ID = {0}".format(ID))
            self.refreshFixedDateAlarm()
        else:
            self.doMessage("Please select an item in the list above.")
    
    def selectSoundFixedDateAlarm(self):
        self.wavName, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'WAV File', directory + "Records/","WAV files (*.wav)")
        if self.wavName == "":
            self.pushButton_4.setText("Please select sound")
        else:
            self.pushButton_4.setText(str(self.wavName.split("/")[-1]))
    
    def addFixedDateAlarm(self):
        name = str(self.lineEdit_2.text())
        date = str(self.dateTimeEdit.dateTime().toString(self.dateTimeEdit.displayFormat()))
        sound = self.wavName
        if name != "" and sound != None and sound != "":
            self.sqlExec("INSERT INTO 'Fixed Date Alarm' (Name,Date,Sound) VALUES ('{0}','{1}','{2}')".format(name,date,sound))
            self.refreshFixedDateAlarm()
            self.doMessage("Alarm saved.")
        else:
            self.doMessage("Some required fields are missing.")

    # Repeating Alarm Functions
    def listWidgetRepeatingAlarm(self, item):
        self.itemRepeatingAlarm = str(item.text())
    
    def deleteItemRepeatingAlarm(self):
        if self.itemRepeatingAlarm != None:
            ID = self.itemRepeatingAlarm.split("\n")[0].split(": ")[1]
            self.sqlExec("DELETE FROM 'Repeating Alarm' WHERE ID = {0}".format(ID))
            self.refreshRepeatingAlarm()
        else:
            self.doMessage("Please select an item in the list above.")
    
    def selectSoundRepeatingAlarm(self):
        self.wavName2, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'WAV File', directory + "Records/","WAV files (*.wav)")
        if self.wavName2 == "":
            self.pushButton_5.setText("Please select sound")
        else:
            self.pushButton_5.setText(str(self.wavName2.split("/")[-1]))
    
    def addRepeatingAlarm(self):
        name = str(self.lineEdit_3.text())
        date = str(self.dateTimeEdit_2.dateTime().toString(self.dateTimeEdit_2.displayFormat()))
        repeat = ""
        for i in range(1,8):
            checkBox = self.tabWidget.currentWidget().findChild(QtWidgets.QCheckBox, "R"+str(i))
            if checkBox.isChecked() == True:
                repeat += repeats[i-1] + ", "
        if repeat != "":
            repeat = repeat[:-2]
        sound = self.wavName2
        if name != "" and sound != None and sound != "" and repeat != "":
            self.sqlExec("INSERT INTO 'Repeating Alarm' (Name,Date,Sound,Repeat) VALUES ('{0}','{1}','{2}','{3}')".format(name,date,sound,repeat))
            self.refreshRepeatingAlarm()
            self.doMessage("Alarm saved.")
        else:
            self.doMessage("Some required fields are missing.")

    # Other Functions
    def tabWidgetCurrentChanged(self):
        self.canPlay = False
        self.recordItem = None
        self.itemFixedDateAlarm = None
        self.itemRepeatingAlarm = None
        self.lineEdit.setText("")
        self.lineEdit_2.setText("")
        self.lineEdit_3.setText("")
        self.wavName = None
        self.wavName2 = None
        self.pushButton_4.setText("Please select sound")
        self.pushButton_5.setText("Please select sound")
        self.dateTimeEdit.setDateTime(QtCore.QDateTime.currentDateTime())
        self.dateTimeEdit_2.setDateTime(QtCore.QDateTime.currentDateTime())
        for i in range(1,8):
            checkBox = self.tabWidget.widget(0).findChild(QtWidgets.QCheckBox, "R"+str(i))
            checkBox.setChecked(False)
        
    def recordButton(self):
        self.canPlay = False

        self.data = sd.rec(int(duration * fs))
        sd.wait()
        write(directory+"record.wav",fs,self.data)
        self.doMessage("Done recording.")
        
        self.canPlay = True

    def playButton(self):
        if self.canPlay:
            data, fs = sf.read(directory+"record.wav")
            sd.play(data,fs)
            sd.wait()
        else:
            self.doMessage("Please record first.")

    def saveButton(self):
        if self.canPlay and str(self.lineEdit.text()) != "":
            fileName = str(self.lineEdit.text()).replace(".wav","")
            write(directory + "Records/" + fileName + ".wav",fs,self.data)
            self.refreshRecords()
            self.doMessage("Record saved.")
        else:
            self.doMessage("Please record first, and name field must not be empty.")

    def listWidgetRecordItem(self,item):
        self.recordItem = str(item.text())

    def itemPlayButton(self):
        if self.recordItem != None:
            data, fs = sf.read(directory + "Records/" + self.recordItem)
            sd.play(data,fs)
            sd.wait()
        else:
            self.doMessage("Please select a record in the list above.")
    
    def itemDeleteButton(self):
        if self.recordItem != None:
            os.remove(directory + "Records/" + self.recordItem)
            self.refreshRecords()
        else:
            self.doMessage("Please select a record in the list above.")

    # SQLite3 Query Connection
    def sqlExec(self, query, database=database):
        conn = sqlite3.connect(database)
        conn.execute(query)
        conn.commit()
        conn.close()

    def sqlCursor(self, query, database=database):
        conn = sqlite3.connect(database)
        retrieve = conn.execute(query)
        retrieve1 = []
        for x in retrieve:
            retrieve1.append(x)
        conn.close()
        return retrieve1

    # Toolbox
    def center(self):
        frameGm = self.frameGeometry()
        screen = QtWidgets.QApplication.desktop().screenNumber(QtWidgets.QApplication.desktop().cursor().pos())
        centerPoint = QtWidgets.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())
        
    def doMessage(self, text, caption="Info"):
        msg = QtWidgets.QMessageBox(self)
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText(text)
        msg.setWindowTitle(caption)
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.show()
        return msg
    
    def doQuestion(self, text, caption="Question"):
        return QtWidgets.QMessageBox.question(self, caption, text, QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)

# Initiate Gui
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    app.exec_()
