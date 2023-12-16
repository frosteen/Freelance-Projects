#!/usr/bin/python3
import sys
from PyQt4 import QtGui, uic, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import threading
import sqlite3
from pyfingerprint.pyfingerprint import PyFingerprint
import time
import tempfile
import os

directory = "/home/pi/Desktop/FingerPrint/"

class DoThreading(QThread):
    def __init__(self, _func):
        self.func = _func
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):
        self.func()

class MyWindow(QtGui.QMainWindow):

    pinNumber = ""
    
    def __init__(self):
        try:self.close()
        except: pass
        try: self.stop_webcam1()
        except: pass
        super(MyWindow, self).__init__()
        uic.loadUi(directory + 'RegistrationWindow.ui', self)
        self.setFixedSize(self.size())
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.center()
        self.show()
        self.pushButtonS.clicked.connect(self.scannerWindowOpen)
        self.pushButtonD.clicked.connect(self.deleteClicked)
        self.pushButtonRegister.clicked.connect(self.registerClicked)

    #TOOLBOX    
    def center(self):
        frameGm = self.frameGeometry()
        screen = QtGui.QApplication.desktop().screenNumber(QtGui.QApplication.desktop().cursor().pos())
        centerPoint = QtGui.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())
        
    def doMessage(self, text, caption="Info"):
        msg = QMessageBox(self)
        msg.setText(text)
        msg.setWindowTitle(caption)
        msg.show()
        return msg
    
    def doQuestion(self, text, caption):
        return QMessageBox.question(self, caption, text, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

    def registerClicked(self):
        atmNum = str(self.lineEditNumber.text())
        atmName = str(self.lineEditName.text())
        atmPin = str(self.lineEditPin.text())
        if (atmNum != "" and atmName != "" and atmPin != ""):
            def doThis():
                try:
                    f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

                    if ( f.verifyPassword() == False ):
                        raise ValueError('The given fingerprint sensor password is wrong!')
                except Exception as e:
                    print('The fingerprint sensor could not be initialized!')
                    print('Exception message: ' + str(e))
                try:
                    self.pushButtonRegister.setEnabled(False)
                    self.pushButtonS.setEnabled(False)
                    self.pushButtonD.setEnabled(False)
                    self.labelStatus.setText("Waiting for finger...")
                    while (f.readImage() == False):
                        pass
                    self.labelStatus.setText("Please wait...")
                    count = 0
                    conn = sqlite3.connect(directory+"database.db")
                    c = conn.cursor()
                    for x in c.execute("SELECT * FROM USERS"):
                        count = count + 1
                    conn.commit()
                    conn.close()
                    imageDestination = directory+'FingerPrintImages/FingerPrint-'+str(count)+'.bmp'
                    f.downloadImage(imageDestination)
                    f.convertImage(0x01)
                    result = f.searchTemplate()
                    positionNumber = result[0]
                    if ( positionNumber >= 0 ):
                        self.labelStatus.setText("Finger exists...")
                    else:
                        self.labelStatus.setText("Remove finger...")
                        time.sleep(2)
                        self.labelStatus.setText("Waiting for same finger again...")
                        while (f.readImage() == False):
                            pass
                        f.convertImage(0x02)
                        if (f.compareCharacteristics() == 0):
                            self.labelStatus.setText("Fingers do not match")
                        else:
                            f.createTemplate()
                            positionNumber = f.storeTemplate()

                            #INSERT FINGERPRINT ON DATABASE
                            conn = sqlite3.connect(directory+"database.db")
                            c = conn.cursor()
                            c.execute("INSERT INTO USERS (Number,Name,Pin,FingerPrint) VALUES ('"+atmNum+"','"+atmName+"','"+atmPin+"','"+str(positionNumber)+"')")
                            conn.commit()
                            conn.close()
                            self.labelStatus.setText("Finger enrolled successfully at position "+str(positionNumber)+"!")
                            self.lineEditNumber.setText("")
                            self.lineEditName.setText("")
                            self.lineEditPin.setText("")
                    time.sleep(2)
                    self.labelStatus.setText("...")
                except Exception as e:
                    self.labelStatus.setText('Operation failed! '+str(e)) 
                self.pushButtonRegister.setEnabled(True)
                self.pushButtonS.setEnabled(True)
                self.pushButtonD.setEnabled(True)

            self.th3 = DoThreading(doThis)
            self.th3.daemon = True
            self.th3.start()               
        else:
            self.doMessage("Some required fields are empty.","Info")

    def scannerWindowOpen(self):
        try:self.close()
        except: pass
        try: self.stop_webcam1()
        except: pass
        super(MyWindow, self).__init__()
        uic.loadUi(directory + 'ScannerWindow.ui', self)
        self.setFixedSize(self.size())
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.center()
        self.show()
        self.pushButtonR.clicked.connect(self.__init__)
        self.label_4.setEnabled(False)
        self.lineEditPin.setEnabled(False)
        self.pbSubmit2.setEnabled(False)
        self.pbSubmit1.clicked.connect(self.submit1Clicked)
        self.pbSubmit2.clicked.connect(self.submit2Clicked)

    def submit1Clicked(self):
        conn = sqlite3.connect(directory+"database.db")
        c = conn.cursor()
        datas = (list(c.execute("SELECT * FROM USERS"))).copy()
        conn.commit()
        conn.close()
        counter = 0
        for x in datas:
            if str(x[1]) == str(self.lineEditPin_2.text()):
                counter = counter + 1
                self.label_2.setEnabled(False)
                self.lineEditPin_2.setEnabled(False)
                self.pbSubmit1.setEnabled(False)
                def doLoop1():
                    try:
                        f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

                        if ( f.verifyPassword() == False ):
                            raise ValueError('The given fingerprint sensor password is wrong!')
                    except Exception as e:
                        print('The fingerprint sensor could not be initialized!')
                        print('Exception message: ' + str(e))
                    self.labelStatus.setText("Waiting for finger...")
                    while (f.readImage() == False):
                        pass
                    f.convertImage(0x01)
                    result = f.searchTemplate()
                    positionNumber = result[0]
                    accuracyScore = result[1]
                    if (positionNumber == -1):
                        self.labelStatus.setText("No match found!")
                        self.label_2.setEnabled(True)
                        self.lineEditPin_2.setEnabled(True)
                        self.lineEditPin_2.setText("")
                        self.pbSubmit1.setEnabled(True)
                    else:
                        conn = sqlite3.connect(directory+"database.db")
                        c = conn.cursor()
                        accountNumber = ""
                        for x in c.execute("SELECT * FROM USERS WHERE FingerPrint='"+str(positionNumber)+"'"):
                            self.pinNumber = str(x[3])
                            accountNumber = str(x[1])
                            print(accountNumber)
                            break
                        conn.commit()
                        conn.close()
                        print(self.lineEditPin_2.text())
                        if (accountNumber == str(self.lineEditPin_2.text())):
                            self.labelStatus.setText("The accuracy score is: "
                                                     +str(accuracyScore))
                            self.label_4.setEnabled(True)
                            self.lineEditPin.setEnabled(True)
                            self.lineEditPin.setText("")
                            self.pbSubmit2.setEnabled(True)
                            self.pbSubmit2.clicked.connect(self.submit2Clicked)
                        else:
                            self.labelStatus.setText("Finger Print and Account Number doesn't match.")
                            self.label_2.setEnabled(True)
                            self.lineEditPin_2.setEnabled(True)
                            self.lineEditPin_2.setText("")
                            self.pbSubmit1.setEnabled(True)
                    time.sleep(2)
                    self.labelStatus.setText("...")
                self.th2 = DoThreading(doLoop1)
                self.th2.daemon = True
                self.th2.start()
                break
        if counter == 0:
            self.doMessage("Account doesn't exist.")

    def submit2Clicked(self):
        if str(self.pinNumber) == str(self.lineEditPin.text()):
            self.doMessage("Valid PIN!", "Info")
        else:
            self.doMessage("Invalid PIN!", "Info")
            self.label_2.setEnabled(True)
            self.lineEditPin_2.setEnabled(True)
            self.lineEditPin_2.setText("")
            self.pbSubmit1.setEnabled(True)
            
            self.label_4.setEnabled(False)
            self.lineEditPin.setEnabled(False)
            self.lineEditPin.setText("")
            self.pbSubmit2.setEnabled(False)

    def deleteClicked(self):
        if (self.doQuestion("Are you sure you want to reset?", "Info") == QMessageBox.Yes):
            try:
                f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

                if ( f.verifyPassword() == False ):
                    raise ValueError('The given fingerprint sensor password is wrong!')
            except Exception as e:
                print('The fingerprint sensor could not be initialized!')
                print('Exception message: ' + str(e))
            for i in range(0, 21):
                f.deleteTemplate(int(i))
            conn = sqlite3.connect(directory+"database.db")
            c = conn.cursor()
            datas = c.execute("DELETE FROM USERS")
            conn.commit()
            conn.close()
            
            folder = directory+'FingerPrintImages'
            for the_file in os.listdir(folder):
                file_path = os.path.join(folder, the_file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                    #elif os.path.isdir(file_path): shutil.rmtree(file_path)
                except Exception as e:
                    print(e)
            self.doMessage("Database deleted successfully!", "Info")
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())
