#!/usr/bin/python3
import sys
from PyQt4 import QtGui, uic, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import os
import ais.stream
from numpy import *
import numpy as np
from sklearn.neural_network import MLPRegressor
from mpl_toolkits.basemap import Basemap
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import math
from matplotlib.figure import Figure
import matplotlib as mpl
from sklearn.preprocessing import StandardScaler

directory = ""

class DoThreading(QThread):
    def __init__(self, _func):
        self.func = _func
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):
        self.func()

class MyWindow(QtGui.QMainWindow):

    def decodeAIS(self,file):
        counter = 1
        aisData = []
        while (self.tableWidget.rowCount() > 0):
            self.tableWidget_2.removeRow(0)
        self.tableWidget_2.setColumnCount(9)
        self.tableWidget_2.setHorizontalHeaderLabels(str("ID;MMSI;Longitude;Latitude;ROT;SOG;COG;True Heading;Timestamp").split(";"))
        with open(file) as f:
            for msg in ais.stream.decode(f):
                rowPosition = self.tableWidget_2.rowCount()
                self.tableWidget_2.insertRow(rowPosition)
                if "id" in msg:
                    self.tableWidget_2.setItem(rowPosition, 0, QtGui.QTableWidgetItem(str(msg["id"])))
                if "mmsi" in msg:
                    self.tableWidget_2.setItem(rowPosition, 1, QtGui.QTableWidgetItem(str(msg["mmsi"])))
                if "x" in msg:
                    self.tableWidget_2.setItem(rowPosition, 2, QtGui.QTableWidgetItem(str(msg["x"])))
                if "y" in msg:
                    self.tableWidget_2.setItem(rowPosition, 3, QtGui.QTableWidgetItem(str(msg["y"])))
                if "rot" in msg:
                    self.tableWidget_2.setItem(rowPosition, 4, QtGui.QTableWidgetItem(str(msg["rot"])))
                if "sog" in msg:
                    self.tableWidget_2.setItem(rowPosition, 5, QtGui.QTableWidgetItem(str(msg["sog"])))
                if "cog" in msg:
                    self.tableWidget_2.setItem(rowPosition, 6, QtGui.QTableWidgetItem(str(msg["cog"])))
                if "true_heading" in msg:
                    self.tableWidget_2.setItem(rowPosition, 7, QtGui.QTableWidgetItem(str(msg["true_heading"])))
                if "timestamp" in msg:
                    self.tableWidget_2.setItem(rowPosition, 8, QtGui.QTableWidgetItem(str(msg["timestamp"])))
                    aisData.append(msg)
                counter = counter + 1
        self.sortedAisData = sorted(aisData, key = 
                     lambda kv:(kv["timestamp"], kv["timestamp"]))
        vessels = []
        for x in aisData:
            if "mmsi" in x:
                vessels.append(x["mmsi"])
                
        vessels = list(dict.fromkeys(vessels))
        for x in vessels:
            self.comboBox_2.addItem(str(x))
        self.statusbar.showMessage("AIS Data has been decoded.")

    def decodeButton(self):
        self.decodeAIS(self.comboBox.currentText())

    def searchButton(self):
        vesselID = self.comboBox_2.currentText()
        if vesselID != "":
            timestamps = 1
            _5TimestampsAisData = []
            for msg in self.sortedAisData:
                if str(msg["mmsi"]) == str(vesselID):
                    if timestamps > 5:
##                        print("-----------------------------------------------------")
##                        print("id:",msg["id"])
##                        print("mmsi:",msg["mmsi"])
##                        print("rot:",msg["rot"])
##                        print("sog:",msg["sog"])
##                        print("x:",msg["x"])
##                        print("y:",msg["y"])
##                        print("cog:",msg["cog"])
##                        print("true_heading:",msg["true_heading"])
##                        print("timestamp:",msg["timestamp"])
##                        print("-----------------------------------------------------")
                        _5TimestampsAisData.append(msg)
                        timestamps = 1
                    timestamps = timestamps + 1
                    
            #Training Set
            inputs = []
            outputs = []
            for x in _5TimestampsAisData:
                if "x" in x and "y" in x and "sog" in x and "rot" in x:
                    inputs.append([x["timestamp"]])
                    outputs.append([x["x"],x["y"],x["rot"],x["sog"],x["cog"],x["true_heading"]])
                    
            #MLPRegression
##            mlp = MLPRegressor(hidden_layer_sizes=(3), activation='tanh', solver='lbfgs', alpha=1e-20)
            mlp = MLPRegressor(
                hidden_layer_sizes=(10,),  activation='relu', solver='adam', alpha=0.001, batch_size='auto',
                learning_rate='constant', learning_rate_init=0.01, power_t=0.5, max_iter=1000, shuffle=True,
                random_state=9, tol=0.0001, verbose=False, warm_start=False, momentum=0.9, nesterovs_momentum=True,
                early_stopping=False, validation_fraction=0.1, beta_1=0.9, beta_2=0.999, epsilon=1e-08)
            
            #Training
            mlp.fit(inputs,outputs)
            startTime = inputs[0][0]
            endTime = inputs[-1][0]
            
            #Score closer to 0 means best
            print(mlp.score(inputs, outputs))
            xpts = []
            ypts = []
            trueHeadingAngles = []
            xpts1 = []
            ypts1 = []
            trueHeadingAngles1 = []
            for x in outputs:
                xpts.append(x[0])
                ypts.append(x[1])
                trueHeadingAngles.append(x[5])
            for i in range(endTime,endTime+60,10):
                predictionOutput = mlp.predict([[i]]).tolist()[0]
                xpts1.append(predictionOutput[0])
                ypts1.append(predictionOutput[1])
                trueHeadingAngles1.append(predictionOutput[5])
            
            #PLOTTING
            self.ax.clear()
            m = Basemap(projection='mill',llcrnrlat=-90,urcrnrlat=90,llcrnrlon=-180,urcrnrlon=180,resolution='l',ax=self.ax)
            m.drawmapboundary(fill_color='#A6CAE0', linewidth=0)
            m.fillcontinents(color='grey', alpha=0.7, lake_color='grey')
            m.drawcoastlines(linewidth=0.1, color="white")
            m.drawparallels(np.arange(-90,90,10),labels=[True,False,False,False])
            m.drawmeridians(np.arange(-180,180,30),labels=[0,0,0,1])
            for i in range(len(xpts)):
                m.plot(xpts[i],ypts[i],latlon=True,markersize=10,c="Blue",marker=(3,0,trueHeadingAngles[i]))
            for i in range(len(xpts1)):
                m.plot(xpts1[i],ypts1[i],latlon=True,markersize=10,c="Red",marker=(3,0,trueHeadingAngles1[i]))
            self.figure.tight_layout()
            self.canvas.draw()
                
    def __init__(self):
        try:self.close()
        except: pass
        super(MyWindow, self).__init__()
        uic.loadUi(directory + 'Main.ui', self)
        self.setFixedSize(self.size())
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.center()
        self.show()

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.verticalLayout.addWidget(self.toolbar)
        self.verticalLayout.addWidget(self.canvas)
        self.ax = self.figure.add_subplot(111)

        
        files = os.listdir(os.getcwd())
        for f in files:
            if str(os.path.splitext(f)[1]) == ".txt" and f != "requirements.txt":
                self.comboBox.addItem(f)
        self.pushButton.clicked.connect(self.decodeButton)
        self.pushButton_2.clicked.connect(self.searchButton)

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
