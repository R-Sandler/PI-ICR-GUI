# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg
from Definitions import *
from calibratewindow import Ui_CalibrateWindow


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        #This is all just drawing the GUI and setting things in place
        MainWindow.setObjectName("PI-ICR Analysis")
        MainWindow.resize(1500, 1000)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.refClusterSelect = QtWidgets.QComboBox(self.centralWidget)
        self.refClusterSelect.setGeometry(QtCore.QRect(20, 540, 500, 22))
        self.refClusterSelect.setObjectName("refClusterSelect")
        self.measClusterSelect = QtWidgets.QComboBox(self.centralWidget)
        self.measClusterSelect.setGeometry(QtCore.QRect(680, 540, 500, 22))
        self.measClusterSelect.setObjectName("measClusterSelect")
        self.refPhi = QtWidgets.QLineEdit(self.centralWidget)
        self.refPhi.setGeometry(QtCore.QRect(220, 570, 200, 20))
        self.refPhi.setObjectName("refPhi")
        self.measPhi = QtWidgets.QLineEdit(self.centralWidget)
        self.measPhi.setGeometry(QtCore.QRect(880, 570, 200, 20))
        self.measPhi.setObjectName("measPhi")
        self.label = QtWidgets.QLabel(self.centralWidget)
        self.label.setGeometry(QtCore.QRect(100, 570, 71, 20))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralWidget)
        self.label_2.setGeometry(QtCore.QRect(760, 570, 71, 20))
        self.label_2.setObjectName("label_2")
        self.refRadius = QtWidgets.QLineEdit(self.centralWidget)
        self.refRadius.setGeometry(QtCore.QRect(220, 600, 200, 20))
        self.refRadius.setObjectName("refRadius")
        self.measRadius = QtWidgets.QLineEdit(self.centralWidget)
        self.measRadius.setGeometry(QtCore.QRect(880, 600, 200, 20))
        self.measRadius.setObjectName("measRadius")
        self.label_3 = QtWidgets.QLabel(self.centralWidget)
        self.label_3.setGeometry(QtCore.QRect(100, 600, 71, 20))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralWidget)
        self.label_4.setGeometry(QtCore.QRect(760, 600, 71, 20))
        self.label_4.setObjectName("label_4")
        self.Theta = QtWidgets.QLineEdit(self.centralWidget)
        self.Theta.setGeometry(QtCore.QRect(650, 630, 200, 20))
        self.Theta.setObjectName("Theta")
        self.N = QtWidgets.QLineEdit(self.centralWidget)
        self.N.setGeometry(QtCore.QRect(650, 660, 200, 20))
        self.N.setObjectName("N")
        self.Frequency = QtWidgets.QLineEdit(self.centralWidget)
        self.Frequency.setGeometry(QtCore.QRect(650, 690, 200, 20))
        self.Frequency.setObjectName("Frequency")
        self.label_5 = QtWidgets.QLabel(self.centralWidget)
        self.label_5.setGeometry(QtCore.QRect(530, 630, 71, 20))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralWidget)
        self.label_6.setGeometry(QtCore.QRect(530, 660, 71, 20))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralWidget)
        self.label_7.setGeometry(QtCore.QRect(530, 690, 71, 20))
        self.label_7.setObjectName("label_7")
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1500, 21))
        self.menuBar.setObjectName("menuBar")
        fileMenu = self.menuBar.addMenu('&File')
        infoMenu = self.menuBar.addMenu('&Info')
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        self.refGraph = pg.PlotWidget(self.centralWidget)
        self.refGraph.setObjectName("refGraph")
        self.refGraph.setGeometry(QtCore.QRect(20, 30, 500, 500))
        self.measGraph = pg.PlotWidget(self.centralWidget)
        self.measGraph.setObjectName("measGraph")
        self.measGraph.setGeometry(QtCore.QRect(680, 30, 500, 500))
        self.EnterButton = QtWidgets.QPushButton(self.centralWidget)
        self.EnterButton.setGeometry(450, 640, 60, 60)
        self.EnterButton.setDefault(False)
        self.EnterButton.setFlat(False)
        self.EnterButton.setObjectName("EnterButton")
        self.EnterButton.setText("Calculate")
        self.Species = QtWidgets.QLabel(self.centralWidget)
        self.Species.move(570, 30)
        self.Species.setObjectName("Species")
        self.Species.setStyleSheet("font:30pt")
        self.Species.setText("<sup>39</sup>K")

        #Add things to the menu bar
        self.actionLoad_New_Reference = fileMenu.addAction("Load New Reference")
        self.actionLoad_New_Measurement = fileMenu.addAction("Load New Measurement")
        self.actionExit = fileMenu.addAction("Exit")

        self.actionCalibrate = infoMenu.addAction("Calibrate")

        #When the "calculate" button is clicked, go do stuff
        self.EnterButton.clicked.connect(self.Enter)

        #When a combobox is used, recalculate the information for that file (not yet implemented)
        self.refClusterSelect.activated.connect(self.refCluster)
        self.measClusterSelect.activated.connect(self.measCluster)

        self.retranslateUi(MainWindow)

        #When the menu bar is used to load files, go do stuff
        self.actionLoad_New_Reference.triggered.connect(self.LoadReference)
        self.actionLoad_New_Measurement.triggered.connect(self.LoadMeasurement)
        self.actionExit.triggered.connect(self.Exit)
        self.actionCalibrate.triggered.connect(self.CalibrateSelect)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def LoadReference(self):

        #This bit loads a new file and calls the files useful_phase and phase_fits_bank to find clusters in the data
        refFile, _filter = QtWidgets.QFileDialog.getOpenFileName(self.centralWidget, 'Load Reference File', "data", "Text files (*.txt)")
        if refFile == "":
            string = "reference"
            self.ShowBox(string)
        else:
            global rxs, rxserr, rys, ryserr, rips, rxkeep, rykeep, rX, rnum, rlabels, rclusters
            self.refClusterSelect.clear()
            self.refGraph.clear()
            rXPOS,rYPOS,rTOF,rSUMX,rSUMY,rdf2 = poswithtof(refFile, -35000, -25000)
            rxs, rxserr, rys, ryserr, rips, rxkeep, rykeep, rX, rnum, rlabels, rclusters = cluster_spots(rXPOS, rYPOS, 1, 1)
            #Add the clusters to the combo box under the graph
            colornames = ['Blue', 'Red', 'Green', 'Cyan', 'Yellow', 'Magenta']
            ClusterList = []
            for i in range(0,rnum):
                ClusterList.append(colornames[i])
            self.refClusterSelect.addItems(ClusterList)
            #Send the cluster information on to be plotted in the GUI
            self.CreateRefPlot(rX, rlabels, rclusters)
            cluster_of_interest = 0
            radius, dradius, phi, dphi = Calculator(rxs, rxserr, rys, ryserr, cluster_of_interest)
            self.refRadius.setText(str(radius)+" ("+str(dradius)+")")
            self.refPhi.setText(str(phi)+" ("+str(dphi)+")")
        

    def LoadMeasurement(self):
        #This bit loads a new file and calls the files useful_phase and phase_fits_bank to find clusters in the data
        measFile, _filter = QtWidgets.QFileDialog.getOpenFileName(self.centralWidget, 'Load Measurement File', "data", "Text files (*.txt)")
        if measFile == "":
            string = "measurement"
            self.ShowBox(string)
        else:
            global mxs, mxserr, mys, myserr, mips, mxkeep, mykeep, mX, mnum, mlabels, mclusters
            self.measClusterSelect.clear()
            self.measGraph.clear()
            mXPOS,mYPOS,mTOF,mSUMX,mSUMY,mdf2 = poswithtof(measFile, -35000, -25000)
            mxs, mxserr, mys, myserr, mips, mxkeep, mykeep, X, num, labels, clusters = cluster_spots(mXPOS, mYPOS, 1, 1)
            #Add the clusters to the combo box under the graph
            colornames = ['Blue', 'Red', 'Green', 'Cyan', 'Yellow', 'Magenta']
            ClusterList = []
            for i in range(0,num):
                ClusterList.append(colornames[i])
            self.measClusterSelect.addItems(ClusterList)
            #Send the cluster information on to be plotted
            self.CreateMeasPlot(X, labels, clusters)
            cluster_of_interest = 0
            radius, dradius, phi, dphi = Calculator(mxs, mxserr, mys, myserr, cluster_of_interest)
            self.measRadius.setText(str(radius)+" ("+str(dradius)+")")
            self.measPhi.setText(str(phi)+" ("+str(dphi)+")")

    def CreateRefPlot(self, data, labels, clusters):
        #Make a pretty plot
        colors = ['b', 'r', 'g', 'c', 'y', 'm', 'w']
        self.refGraph.setXRange(-13,7, padding=0)
        self.refGraph.setYRange(-6,14, padding=0)
        for k, col in zip(unique(labels), colors):
            my = labels == k
            self.refGraph.plot(data[my,0], data[my,1], pen=None, symbol='o', symbolBrush = colors[k])
        self.refGraph.plot(clusters[:,0], clusters[:,1], pen=None, symbol='o', symbolSize=10, symbolBrush = 'k')

    def CreateMeasPlot(self, data, labels, clusters):
        #Make a pretty plot
        colors = ['b', 'r', 'g', 'c', 'y', 'm', 'w']
        self.measGraph.setXRange(-13,7, padding=0)
        self.measGraph.setYRange(-6,14, padding=0)
        for k, col in zip(unique(labels), colors):
            my = labels == k
            self.measGraph.plot(data[my,0], data[my,1], pen=None, symbol='o', symbolBrush = colors[k])
        self.measGraph.plot(clusters[:,0], clusters[:,1], pen=None, symbol='o', symbolSize=10, symbolBrush = 'k')

    def refCluster(self, index):
        #Recalculate the radius and angle of the plot for the selected cluster
        self.refRadius.clear()
        self.refPhi.clear()
        radius, dradius, phi, dphi = Calculator(rxs, rxserr, rys, ryserr, index)
        self.refRadius.setText(str(radius)+" ("+str(dradius)+")")
        self.refPhi.setText(str(phi)+" ("+str(dphi)+")")
        #If the other plot is loaded, recalculate the frequency
        text = self.measPhi.text()
        if text == "":
            text = "Nope"
        else:
            self.Enter()


    def measCluster(self, index):
        #Recalculate the radius and angle of the plot for the selected cluster
        self.measRadius.clear()
        self.measPhi.clear()
        radius, dradius, phi, dphi = Calculator(mxs, mxserr, mys, myserr, index)
        self.measRadius.setText(str(radius)+" ("+str(dradius)+")")
        self.measPhi.setText(str(phi)+" ("+str(dphi)+")")
        #If the other plot is loaded, recalculate the frequency
        text = self.refPhi.text()
        if text == "":
            text = "Nope"
        else:
            self.Enter()


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Angle"))
        self.label_2.setText(_translate("MainWindow", "Angle"))
        self.label_3.setText(_translate("MainWindow", "Radius"))
        self.label_4.setText(_translate("MainWindow", "Radius"))
        self.label_5.setText(_translate("MainWindow", "Theta"))
        self.label_6.setText(_translate("MainWindow", "N"))
        self.label_7.setText(_translate("MainWindow", "Frequency"))
        self.actionLoad_New_Reference.setText(_translate("MainWindow", "Load New Reference"))
        self.actionLoad_New_Measurement.setText(_translate("MainWindow", "Load New Measurement"))

    def Enter(self):
        text = self.refPhi.text()
        if text == "":
            string = "reference"
            self.ShowBox(string)
        else:
            rindex = self.refClusterSelect.currentIndex()
            text = self.measPhi.text()
            if text == "":
                string = "measurement"
                self.ShowBox(string)
            else:
                mindex = self.measClusterSelect.currentIndex()
                N, theta, dtheta, frequency, dfrequency = Frequency(rxs, rxserr, rys, ryserr, rindex, mxs, mxserr, mys, myserr, mindex)
                self.N.setText(str(N))
                self.Frequency.setText(str(frequency) + " (" + str(dfrequency) +")")
                self.Theta.setText(str(theta) + " (" + str(dtheta) + ")")
                

    def ShowBox(self, string):
        self.msg = QtWidgets.QMessageBox()
        title = "Missing "+string+" file"
        message = "No "+string+" file is selected. Please select a "+string+" file."
        self.msg.setWindowTitle(title)
        self.msg.setText(message)
        self.msg.exec_()

    def CalibrateSelect(self):
        self.cw = Ui_CalibrateWindow()
        #self.cw.exec_()
        self.cw.freqCCalc.clicked.connect(self.CalibrateCalc)
        self.cw.exec_()

    def CalibrateCalc(self):
        print("Wahoo!")

    def Exit(self):
        sys.exit(app.exec_())

def except_hook(cls, exception, traceback):
        sys.__excepthook__(cls, exception, traceback)
       
if __name__ == "__main__":
    import sys
    sys.excepthook = except_hook
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QWidget()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
