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
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
import math
import ast

#Interpolate
from scipy import interpolate

#Basemap
from mpl_toolkits.basemap import Basemap
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib as mpl

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
    once = True
    def decodeAIS(self,file):
        self.statusbar.showMessage("Decoding... Please wait.")
        self.comboBox_2.clear()
        counter = 1
        aisData = []
        aisData2 = []
        while (self.tableWidget_2.rowCount() > 0):
            self.tableWidget_2.removeRow(0)
        while (self.tableWidget.rowCount() > 0):
            self.tableWidget.removeRow(0)
        self.tableWidget_2.setColumnCount(9)
        self.tableWidget_2.setHorizontalHeaderLabels(str("ID;MMSI;Longitude;Latitude;ROT;SOG;COG;True Heading;Timestamp").split(";"))
        if file.find("Decoded") == -1:
            with open(file) as f:
                for msg in ais.stream.decode(f):
                    rowPosition = self.tableWidget_2.rowCount()
                    self.tableWidget_2.insertRow(rowPosition)
                    if "id" in msg:
                        self.tableWidget_2.setItem(rowPosition, 0, QtGui.QTableWidgetItem(str(msg["id"])))
                    if "mmsi" in msg:
                        self.tableWidget_2.setItem(rowPosition, 1, QtGui.QTableWidgetItem(str(msg["mmsi"])))
                    if "x" in msg:
                        self.tableWidget_2.setItem(rowPosition, 3, QtGui.QTableWidgetItem(str(msg["x"])))
                    if "y" in msg:
                        self.tableWidget_2.setItem(rowPosition, 2, QtGui.QTableWidgetItem(str(msg["y"])))
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
                    aisData2.append(msg)
                    counter = counter + 1
            with open(str(file).replace(".txt","") + " (Decoded)" + ".txt", "w") as f:
                for  msg in aisData2:
                    f.write(str(msg))
                    f.write("\n")
        else:
            data = []
            with open(file,"r") as f:
                for line in f:
                    mod = line.replace("\n","")
                    res = ast.literal_eval(mod)
                    data.append(res)
            for msg in data:
                rowPosition = self.tableWidget_2.rowCount()
                self.tableWidget_2.insertRow(rowPosition)
                if "id" in msg:
                    self.tableWidget_2.setItem(rowPosition, 0, QtGui.QTableWidgetItem(str(msg["id"])))
                if "mmsi" in msg:
                    self.tableWidget_2.setItem(rowPosition, 1, QtGui.QTableWidgetItem(str(msg["mmsi"])))
                if "x" in msg:
                    self.tableWidget_2.setItem(rowPosition, 3, QtGui.QTableWidgetItem(str(msg["x"])))
                if "y" in msg:
                    self.tableWidget_2.setItem(rowPosition, 2, QtGui.QTableWidgetItem(str(msg["y"])))
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
                
        self.sortedAisData = aisData.copy()
##        self.sortedAisData.reverse()
        vessels = []
        for x in self.sortedAisData:
            if "mmsi" in x:
                vessels.append(x["mmsi"])
                
        vessels = list(dict.fromkeys(vessels))
        for x in vessels:
            self.comboBox_2.addItem(str(x))
        self.statusbar.showMessage("AIS Data has been decoded.")

    def decodeButton(self):
        self.decodeAIS(self.comboBox.currentText())

    def searchButton(self):
        self.MMSI = self.comboBox_2.currentText()
        if self.MMSI != "":
            self.statusbar.showMessage("Plotting... Please wait.")
            timestamps = None
            self.cntr = 1
            self._5TimestampsAisData = []
            for msg in self.sortedAisData:
                if str(msg["mmsi"]) == str(self.MMSI):
                    if timestamps != str(msg["timestamp"]):
                        self._5TimestampsAisData.append(msg)
                        timestamps = str(msg["timestamp"])
                        self.cntr = self.cntr + 1
            
            self.cntr = 1
            for x in self._5TimestampsAisData:
                x["timestamp"] = self.cntr
                self.cntr = self.cntr + 1
                    
            #Training Set
            self.inputs = []
            self.outputs = []
            while (self.tableWidget.rowCount() > 0):
                self.tableWidget.removeRow(0)
            self.tableWidget.setColumnCount(8)
            self.tableWidget.setHorizontalHeaderLabels(str("MMSI;Timestamp;Longitude;Latitude;ROT;SOG;COG;True Heading").split(";"))
            for x in self._5TimestampsAisData:
                if "x" in x and "y" in x and "sog" in x and "rot" in x:
                    self.inputs.append([x["timestamp"]])
                    self.outputs.append([x["x"],x["y"],x["rot"],x["sog"],x["cog"],x["true_heading"]])
                    rowPosition = self.tableWidget.rowCount()
                    self.tableWidget.insertRow(rowPosition)
                    self.tableWidget.setItem(rowPosition, 0, QtGui.QTableWidgetItem(str(self.MMSI)))
                    self.tableWidget.setItem(rowPosition, 1, QtGui.QTableWidgetItem(str(x["timestamp"])))
                    self.tableWidget.setItem(rowPosition, 3, QtGui.QTableWidgetItem(str(x["x"])))
                    self.tableWidget.setItem(rowPosition, 2, QtGui.QTableWidgetItem(str(x["y"])))
                    self.tableWidget.setItem(rowPosition, 4, QtGui.QTableWidgetItem(str(x["rot"])))
                    self.tableWidget.setItem(rowPosition, 5, QtGui.QTableWidgetItem(str(x["sog"])))
                    self.tableWidget.setItem(rowPosition, 6, QtGui.QTableWidgetItem(str(x["cog"])))
                    self.tableWidget.setItem(rowPosition, 7, QtGui.QTableWidgetItem(str(x["true_heading"])))
            self.xpts = []
            self.ypts = []
            self.trueHeadingAngles = []
            for x in self.outputs:
                self.xpts.append(x[0])
                self.ypts.append(x[1])
                self.trueHeadingAngles.append(x[5])

            #PLOTTING
            self.ax.clear()
            m = Basemap(projection='mill',llcrnrlat=-90,urcrnrlat=90,llcrnrlon=-180,urcrnrlon=180,resolution='l',ax=self.ax)
            m.drawmapboundary(fill_color='#A6CAE0', linewidth=0)
            m.fillcontinents(color='grey', alpha=0.7, lake_color='grey')
            m.drawcoastlines(linewidth=0.1, color="white")
            m.drawparallels(np.arange(-90,90,10),labels=[True,False,False,False])
            m.drawmeridians(np.arange(-180,180,30),labels=[0,0,0,1])
            for i in range(len(self.xpts)):
                m.plot(self.xpts[i],self.ypts[i],latlon=True,markersize=5,c="Blue",marker=(3,0,self.trueHeadingAngles[i]))
            m.plot(self.xpts, self.ypts,'-',latlon=True, markersize=0, c="Blue", linewidth=1)
            files = os.listdir(os.getcwd()+"\SUGGESTED-ROUTES")
            for file in files:
                with open(os.getcwd()+"\SUGGESTED-ROUTES"+"\\"+file) as f:
                    self.longitudes = []
                    self.latitudes = []
                    for line in f:
                        self.longitude = float(line.replace("\n","").split(",")[0])
                        self.latitude = float(line.replace("\n","").split(",")[1])
                        self.longitudes.append(self.longitude)
                        self.latitudes.append(self.latitude)
                    self.longNew = interpolate.interp1d(self.latitudes, self.longitudes,kind = 'linear')
                    self.latNew = np.linspace(self.latitudes[0],self.latitudes[len(self.latitudes)-1],num=100)
                    m.plot(self.latNew, self.longNew(self.latNew),'-',latlon=True, markersize=0, c="Black", linewidth=1)
            self.figure.tight_layout()
            self.canvas.draw()
            self.statusbar.showMessage("Selected data has been plotted successfully.")
            def predictNatin():
                if self.cntr > 5:
                    #MLPRegression
##                    mlp = MLPRegressor(hidden_layer_sizes=(3,), activation='tanh', solver='lbfgs', alpha=1e-20)

                    #THE BEST I FOUND
                    mlp = MLPRegressor(
                        hidden_layer_sizes=(100,),  activation='relu', solver='adam', alpha=0.001, batch_size='auto',
                        learning_rate='constant', learning_rate_init=0.01, power_t=0.5, max_iter=1000, shuffle=True,
                        random_state=0, tol=0.0001, verbose=False, warm_start=False, momentum=0.9, nesterovs_momentum=True,
                        early_stopping=False, validation_fraction=0.1, beta_1=0.9, beta_2=0.999, epsilon=1e-08)
                    
##                    mlp = MLPRegressor(
##                        hidden_layer_sizes=(10,),  activation='relu', solver='adam', alpha=0.001, batch_size='auto',
##                        learning_rate='constant', learning_rate_init=0.01, power_t=0.5, max_iter=1000, shuffle=True,
##                        random_state=9, tol=0.0001, verbose=False, warm_start=False, momentum=0.9, nesterovs_momentum=True,
##                        early_stopping=False, validation_fraction=0.1, beta_1=0.9, beta_2=0.999, epsilon=1e-08)
                    
                    #Training
                    scaler = StandardScaler()  # doctest: +SKIP
                    # Don't cheat - fit only on training data
                    scaler.fit(self.inputs)
                    X_train = scaler.transform(self.inputs)  # doctest: +SKIP
                    scaler.fit(self.outputs)  # doctest: +SKIP
                    Y_train = scaler.transform(self.outputs)
                    # apply same transformation to test data
                    mlp.fit(X_train,Y_train)
                    
                    startTime = self.inputs[0][0]
                    endTime = self.inputs[-1][0]
                    #Score closer to 0 means best
                    print("PREDICTION SCORE (\"Score closer to 0 means best\"): ", mlp.score(X_train, Y_train))
                    self.xpts1 = []
                    self.ypts1 = []
                    self.trueHeadingAngles1 = []
                    predictions = []
                    newTimestamps = []
                    for i in range(endTime+1,endTime+60*5, 1):
                        newTimestamps.append(i)
                        scaler.fit(self.inputs)
                        predictionOutput = mlp.predict(scaler.transform([[i]])).tolist()[0]
                        scaler.fit(self.outputs)
                        predictions.append(scaler.inverse_transform(predictionOutput))
                        self.xpts1.append(scaler.inverse_transform(predictionOutput)[0])
                        self.ypts1.append(scaler.inverse_transform(predictionOutput)[1])
                        self.trueHeadingAngles1.append(scaler.inverse_transform(predictionOutput)[5])
                    
                    while (self.tableWidget.rowCount() > 0):
                        self.tableWidget.removeRow(0)
                    self.tableWidget.setColumnCount(8)
                    self.tableWidget.setHorizontalHeaderLabels(str("MMSI;Timestamp;Longitude;Latitude;ROT;SOG;COG;True Heading").split(";"))
                    for x in self._5TimestampsAisData:
                        if "x" in x and "y" in x and "sog" in x and "rot" in x:
                            rowPosition = self.tableWidget.rowCount()
                            self.tableWidget.insertRow(rowPosition)
                            self.tableWidget.setItem(rowPosition, 0, QtGui.QTableWidgetItem(str(self.MMSI)))
                            self.tableWidget.setItem(rowPosition, 1, QtGui.QTableWidgetItem(str(x["timestamp"])))
                            self.tableWidget.setItem(rowPosition, 3, QtGui.QTableWidgetItem(str(x["x"])))
                            self.tableWidget.setItem(rowPosition, 2, QtGui.QTableWidgetItem(str(x["y"])))
                            self.tableWidget.setItem(rowPosition, 4, QtGui.QTableWidgetItem(str(x["rot"])))
                            self.tableWidget.setItem(rowPosition, 5, QtGui.QTableWidgetItem(str(x["sog"])))
                            self.tableWidget.setItem(rowPosition, 6, QtGui.QTableWidgetItem(str(x["cog"])))
                            self.tableWidget.setItem(rowPosition, 7, QtGui.QTableWidgetItem(str(x["true_heading"])))
                    for i in range(len(predictions)):
                        rowPosition = self.tableWidget.rowCount()
                        self.tableWidget.insertRow(rowPosition)
                        self.tableWidget.setItem(rowPosition, 0, QtGui.QTableWidgetItem(str(self.MMSI)+"(P)"))
                        self.tableWidget.setItem(rowPosition, 1, QtGui.QTableWidgetItem(str(newTimestamps[i])))
                        self.tableWidget.setItem(rowPosition, 3, QtGui.QTableWidgetItem(str(predictions[i][0])))
                        self.tableWidget.setItem(rowPosition, 2, QtGui.QTableWidgetItem(str(predictions[i][1])))
                        self.tableWidget.setItem(rowPosition, 4, QtGui.QTableWidgetItem(str(predictions[i][2])))
                        self.tableWidget.setItem(rowPosition, 5, QtGui.QTableWidgetItem(str(predictions[i][3])))
                        self.tableWidget.setItem(rowPosition, 6, QtGui.QTableWidgetItem(str(predictions[i][4])))
                        self.tableWidget.setItem(rowPosition, 7, QtGui.QTableWidgetItem(str(predictions[i][5])))

                    #PLOTTING W/ PREDICTIONS
                    self.ax.clear()
                    m = Basemap(projection='mill',llcrnrlat=-90,urcrnrlat=90,llcrnrlon=-180,urcrnrlon=180,resolution='l',ax=self.ax)
                    m.drawmapboundary(fill_color='#A6CAE0', linewidth=0)
                    m.fillcontinents(color='grey', alpha=0.7, lake_color='grey')
                    m.drawcoastlines(linewidth=0.1, color="white")
                    m.drawparallels(np.arange(-90,90,10),labels=[True,False,False,False])
                    m.drawmeridians(np.arange(-180,180,30),labels=[0,0,0,1])
                    for i in range(len(self.xpts)):
                        m.plot(self.xpts[i],self.ypts[i],latlon=True,markersize=5,c="Blue",marker=(3,0,self.trueHeadingAngles[i]))                    
                    for i in range(len(self.xpts1)):
                        m.plot(self.xpts1[i],self.ypts1[i],latlon=True,markersize=5,c="Red",marker=(3,0,self.trueHeadingAngles1[i]))
                    m.plot(self.xpts, self.ypts,'-',latlon=True, markersize=0, c="Blue", linewidth=1)
                    self.xpts1.insert(0,self.xpts[-1])
                    self.ypts1.insert(0,self.ypts[-1])
                    m.plot(self.xpts1, self.ypts1,'-',latlon=True, markersize=0, c="Red", linewidth=1)
                    self.xpts1.remove(self.xpts[-1])
                    self.ypts1.remove(self.ypts[-1])
                    #SUGGESTED-ROUTES
                    joinedXpts = self.xpts+self.xpts1
                    joinedYpts = self.ypts+self.ypts1
                    files = os.listdir(os.getcwd()+"\SUGGESTED-ROUTES")
                    ROUTES = {}
                    for file in files:
                        self.correct = 0
                        with open(os.getcwd()+"\SUGGESTED-ROUTES"+"\\"+file) as f:
                            self.longitudes = []
                            self.latitudes = []
                            for line in f:
                                self.longitude = float(line.replace("\n","").split(",")[0])
                                self.latitude = float(line.replace("\n","").split(",")[1])
                                self.longitudes.append(self.longitude)
                                self.latitudes.append(self.latitude)
                            self.longNew = interpolate.interp1d(self.latitudes, self.longitudes,kind = 'linear')
                            self.latNew = np.linspace(self.latitudes[0],self.latitudes[len(self.latitudes)-1],num=10000)
                            m.plot(self.latNew, self.longNew(self.latNew),'-',latlon=True, markersize=0, c="Black", linewidth=1)
                            for lat1,long1 in zip(self.latNew,self.longNew(self.latNew)):
                                for lat,long in zip(joinedXpts, joinedYpts):
                                    if (long <= long1+0.0001 and long >= long1-0.0001) and lat <= lat1+0.0001 and lat >= lat1-0.0001:
                                        self.correct = self.correct+1
                            ROUTES[file.replace(".txt","")] = self.correct
                    maxCorrect = max(ROUTES, key=ROUTES.get)
                    maxCorrectNum = max(ROUTES.values())
                    if maxCorrectNum != 0:
                        self.statusbar.showMessage("The route is " + maxCorrect + ". The ship is in the correct suggested route.")
                    else:
                        self.statusbar.showMessage("Can't find ship's route.")
                    self.figure.tight_layout()
                    self.canvas.draw()
                    #
                else:
                    self.doMessage("Cannot predict, TIMESTAMPS are less than 5.")
            
            if self.once:
                self.once = False
                self.predict.clicked.connect(predictNatin)
                
    def __init__(self):
        try:self.close()
        except: pass
        super(MyWindow, self).__init__()
        uic.loadUi(directory + 'Main.ui', self)
        self.setFixedSize(self.size())
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.center()
        self.show()

        #Basemap Figure
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.verticalLayout.addWidget(self.toolbar)
        self.verticalLayout.addWidget(self.canvas)
        self.ax = self.figure.add_subplot(111)
        #
        
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
