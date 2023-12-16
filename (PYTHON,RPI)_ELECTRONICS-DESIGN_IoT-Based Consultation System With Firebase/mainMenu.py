try:
    import sys
    import os
    from PyQt4 import uic, QtGui, QtCore
    from PyQt4.uic import *
    from PyQt4.QtGui import *
    from PyQt4.QtCore import *
    from firebase import firebase
    from cv2 import *
    import base64
except ImportError:
    print("You don't have any 'required' libraries.")

mainDatabase = firebase.FirebaseApplication('https://facultydatabase-4b787.firebaseio.com/', authentication=None)
directory = "/home/pi/STUDENT/"

class MainProgram(QtGui.QMainWindow):
##    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    def center(self):
        frameGm = self.frameGeometry()
        screen = QtGui.QApplication.desktop().screenNumber(QtGui.QApplication.desktop().cursor().pos())
        centerPoint = QtGui.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    #CAMERA
    def start_webcam(self):
        self.capture=cv2.VideoCapture(0)

        self.timer=QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(1)

    def update_frame(self):
        ret, self.image = self.capture.read()
        self.image=cv2.flip(self.image, 1)
        self.displayImage(self.image, 1)

    def stop_webcam(self):
        try:
            self.timer.stop()
            cv2.imwrite(directory+'pic.png', self.image)
            self.capture.release()
        except:print("error")

    def displayImage(self, img, window=1):
        self.outImage = QImage(img, img.shape[1], img.shape[0], img.strides[0], QImage.Format_RGB888)
        self.outImage=self.outImage.rgbSwapped()
        if window == 1:
            self.labelPicture.setPixmap(QPixmap.fromImage(self.outImage))
            self.labelPicture.setScaledContents(True)

    ###
    
        
    def __init__(self):
        try:self.close()
        except:pass
        super(MainProgram, self).__init__()
        uic.loadUi(directory+'MainScreen.ui', self)
        self.setFixedSize(self.size())
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.center()
        self.show()
        self.pushButtonTakePicture.clicked.connect(self.pButtonTakePictureClicked)
        self.checkBox8.clicked.connect(self.checkBox8Clicked)
        self.pushButtonRefresh.clicked.connect(self.pButtonRefreshClicked)
        self.pushButtonSubmit.clicked.connect(self.pButtonSubmitClicked)
        self.pButtonRefreshClicked()
        self.start_webcam()
        


    #MESSAGE BOX
    def showMessage(self, text, caption):
        msg = QMessageBox
        msg.information(self, caption, text)

    def showQuestion(self, text, caption):
        msg = QMessageBox
        return msg.question(self, caption, text, msg.Yes | msg.No)

    #MAIN SCREEN UI
    def pButtonRefreshClicked(self):
        self.comboBoxAcademicAdviser.clear()
        res = mainDatabase.get("", None)
        #mainDatabase.delete("/ADVISING", None)
        if res != None:
            if res["ATTENDANCE"] != None:
                for key, value in res["ATTENDANCE"].items():
                    self.comboBoxAcademicAdviser.addItem(str(key))
                    
    def checkBox8Clicked(self):
        if self.checkBox8.isChecked() == True:
            self.lineEditConcern.setDisabled(False)
            self.lineEditConcern.clear()
        else:
            self.lineEditConcern.setDisabled(True)
            self.lineEditConcern.clear()

    def pButtonTakePictureClicked(self):
        if self.pushButtonTakePicture.text() == "Take Picture":
            if self.lineEditStudentNumber.text() == "":
                self.showMessage("Complete all the missing fields.", "INFORMATION")
                self.pushButtonSubmit.setDisabled(True)
            else:
                self.pushButtonTakePicture.setText("Retake")
                self.pushButtonSubmit.setDisabled(False)
                self.stop_webcam()
        else:
            self.pushButtonTakePicture.setText("Take Picture")
            self.pushButtonSubmit.setDisabled(True)
            self.start_webcam()

    def checkNameInput(self, text):
        for c in str(self.lineEditStudentName.text()):
            if c == ".":
                return False
        return True

    def imageToBase64(self, img):
        with open(img, "rb") as imageFile:
            stringImage = base64.b64encode(imageFile.read())
            return stringImage
        
    def pButtonSubmitClicked(self):
        if self.checkNameInput(str(self.lineEditStudentName.text())) == False:
            self.showMessage("Student Name shouldn't contain any periods.", "INFORMATION")
        else:
            if self.lineEditStudentNumber.text() == "":
                self.showMessage("Student number is empty.", "INFORMATION")
            else:
                insertThis = {
                        'Name':'',
                        'ProgramYear':'',
                        'AcademicAdviser':'',
                        'Date':'',
                        'NatureOfAdvising': '',
                        'Consultation': '',
                        'Message': '',
                        'Picture': str(self.imageToBase64(directory+"pic.png"))
                    }
                insertThis['Name'] = self.lineEditStudentName.text()
                insertThis['ProgramYear'] = self.lineEditProgramYear.text()
                insertThis['AcademicAdviser'] = self.comboBoxAcademicAdviser.currentText()
                insertThis['Date'] = self.lineEditDate.text()
                if self.checkBox1.isChecked() == True:
                    insertThis['NatureOfAdvising'] += "1"
                else:
                    insertThis['NatureOfAdvising'] += "0"
                if self.checkBox2.isChecked() == True:
                    insertThis['NatureOfAdvising'] += "1"
                else:
                    insertThis['NatureOfAdvising'] += "0"
                if self.checkBox3.isChecked() == True:
                    insertThis['NatureOfAdvising'] += "1"
                else:
                    insertThis['NatureOfAdvising'] += "0"
                if self.checkBox4.isChecked() == True:
                    insertThis['NatureOfAdvising'] += "1"
                else:
                    insertThis['NatureOfAdvising'] += "0"
                if self.checkBox5.isChecked() == True:
                    insertThis['NatureOfAdvising'] += "1"
                else:
                    insertThis['NatureOfAdvising'] += "0"
                if self.checkBox6.isChecked() == True:
                    insertThis['NatureOfAdvising'] += "1"
                else:
                    insertThis['NatureOfAdvising'] += "0"
                if self.checkBox7.isChecked() == True:
                    insertThis['NatureOfAdvising'] += "1"
                else:
                    insertThis['NatureOfAdvising'] += "0"
                if self.checkBox8.isChecked() == True:
                    insertThis['NatureOfAdvising'] += "1"
                    insertThis['Consultation'] = self.lineEditConcern.text()
                else:
                    insertThis['NatureOfAdvising'] += "0"
                res = mainDatabase.get('/ATTENDANCE', None)
                if res != None:
                    if self.comboBoxAcademicAdviser.currentText() in res:
                        if ("In" in res[self.comboBoxAcademicAdviser.currentText()] and
                            not "Out" in res[self.comboBoxAcademicAdviser.currentText()]):
                            mainDatabase.patch("/ADVISING/N"+self.lineEditStudentNumber.text(), insertThis)
                            self.doClear()
                            self.showMessage("Your request has been sent. Prof. "+self.comboBoxAcademicAdviser.currentText()+" is waiting for you. Please proceed to the advising room.", "INFORMATION")
                        else:
                            mainDatabase.patch("/ADVISING/N"+self.lineEditStudentNumber.text(), insertThis)
                            resQ = self.showQuestion("Prof. "+self.comboBoxAcademicAdviser.currentText()+" is not available. Do you want to leave a message?", "QUESTION")
                            if resQ == QMessageBox.Yes:
                                self.showMessageScreen(self.lineEditStudentNumber.text())
                            else:
                                self.doClear()
                    else:
                        self.showMessage("Professor doesn't exist in the database.", "INFORMATION")

    def doClear(self):
        self.lineEditStudentName.clear()
        self.lineEditStudentNumber.clear()
        self.lineEditProgramYear.clear()
        self.lineEditDate.clear()
        self.checkBox1.setChecked(False)
        self.checkBox2.setChecked(False)
        self.checkBox3.setChecked(False)
        self.checkBox4.setChecked(False)
        self.checkBox5.setChecked(False)
        self.checkBox6.setChecked(False)
        self.checkBox7.setChecked(False)
        self.checkBox8.setChecked(False)
        self.pushButtonTakePicture.setText("Take Picture")
        self.pushButtonSubmit.setDisabled(True)
        self.start_webcam()

    #MESSAGE SCREEN UI
    def showMessageScreen(self, studentNumber):
        try:self.close()
        except:pass
        super(MainProgram, self).__init__()
        uic.loadUi(directory+'MessageScreen.ui', self)
        self.setFixedSize(self.size())
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.center()
        self.show()
        self.pushButtonSubmit.clicked.connect(lambda: self.pButtonSubmitClickedM(studentNumber))

    def pButtonSubmitClickedM(self, studentNumber):
        mainDatabase.patch("/ADVISING/N"+studentNumber, { 'Message':self.textEdit.toPlainText() })
        self.__init__()
        self.showMessage("Successfully submitted.", "INFORMATION")

#START PROGRAM
app = QtGui.QApplication(sys.argv)
window = MainProgram()
sys.exit(app.exec_())
