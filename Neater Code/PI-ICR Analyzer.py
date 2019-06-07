# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from mainwindow import Ui_MainWindow
import pyqtgraph as pg
from Definitions import *
from calibratewindow import Ui_CalibrateWindow


def LoadReference(self):
    #This bit loads a new file and calls the files useful_phase and phase_fits_bank to find clusters in the data
    refFile, _filter = QtWidgets.QFileDialog.getOpenFileName(ui, 'Load Reference File', "data", "Text files (*.txt)")
    if refFile == "":
        string = "reference"
        ShowBox(string)
    else:
        global rxs, rxserr, rys, ryserr, rips, rxkeep, rykeep, rX, rnum, rlabels, rclusters
        ui.refClusterSelect.clear()
        ui.refGraph.clear()
        rXPOS,rYPOS,rTOF,rSUMX,rSUMY,rdf2 = poswithtof(refFile, -35000, -25000)
        rxs, rxserr, rys, ryserr, rips, rxkeep, rykeep, rX, rnum, rlabels, rclusters = cluster_spots(rXPOS, rYPOS, 1, 1)
        #Add the clusters to the combo box under the graph
        colornames = ['Blue', 'Red', 'Green', 'Cyan', 'Yellow', 'Magenta']
        ClusterList = []
        for i in range(0,rnum):
            ClusterList.append(colornames[i])
        ui.refClusterSelect.addItems(ClusterList)
        #Send the cluster information on to be plotted in the GUI
        CreateRefPlot(self, rX, rlabels, rclusters)
        cluster_of_interest = 0
        radius, dradius, phi, dphi = Calculator(rxs, rxserr, rys, ryserr, cluster_of_interest)
        ui.refRadius.setText(str(radius)+" ("+str(dradius)+")")
        ui.refPhi.setText(str(phi)+" ("+str(dphi)+")")
    

def LoadMeasurement(self):
    #This bit loads a new file and calls the files useful_phase and phase_fits_bank to find clusters in the data
    measFile, _filter = QtWidgets.QFileDialog.getOpenFileName(ui, 'Load Measurement File', "data", "Text files (*.txt)")
    if measFile == "":
        string = "measurement"
        ShowBox(string)
    else:
        global mxs, mxserr, mys, myserr, mips, mxkeep, mykeep, mX, mnum, mlabels, mclusters
        ui.measClusterSelect.clear()
        ui.measGraph.clear()
        mXPOS,mYPOS,mTOF,mSUMX,mSUMY,mdf2 = poswithtof(measFile, -35000, -25000)
        mxs, mxserr, mys, myserr, mips, mxkeep, mykeep, X, num, labels, clusters = cluster_spots(mXPOS, mYPOS, 1, 1)
        #Add the clusters to the combo box under the graph
        colornames = ['Blue', 'Red', 'Green', 'Cyan', 'Yellow', 'Magenta']
        ClusterList = []
        for i in range(0,num):
            ClusterList.append(colornames[i])
        ui.measClusterSelect.addItems(ClusterList)
        #Send the cluster information on to be plotted
        CreateMeasPlot(self, X, labels, clusters)
        cluster_of_interest = 0
        radius, dradius, phi, dphi = Calculator(mxs, mxserr, mys, myserr, cluster_of_interest)
        ui.measRadius.setText(str(radius)+" ("+str(dradius)+")")
        ui.measPhi.setText(str(phi)+" ("+str(dphi)+")")

def CreateRefPlot(self, data, labels, clusters):
    #Make a pretty plot
    colors = ['b', 'r', 'g', 'c', 'y', 'm', 'w']
    ui.refGraph.setXRange(-13,7, padding=0)
    ui.refGraph.setYRange(-6,14, padding=0)
    for k, col in zip(unique(labels), colors):
        my = labels == k
        ui.refGraph.plot(data[my,0], data[my,1], pen=None, symbol='o', symbolBrush = colors[k])
    ui.refGraph.plot(clusters[:,0], clusters[:,1], pen=None, symbol='o', symbolSize=10, symbolBrush = 'k')

def CreateMeasPlot(self, data, labels, clusters):
    #Make a pretty plot
    colors = ['b', 'r', 'g', 'c', 'y', 'm', 'w']
    ui.measGraph.setXRange(-13,7, padding=0)
    ui.measGraph.setYRange(-6,14, padding=0)
    for k, col in zip(unique(labels), colors):
        my = labels == k
        ui.measGraph.plot(data[my,0], data[my,1], pen=None, symbol='o', symbolBrush = colors[k])
    ui.measGraph.plot(clusters[:,0], clusters[:,1], pen=None, symbol='o', symbolSize=10, symbolBrush = 'k')

def refCluster(index):
    #Recalculate the radius and angle of the plot for the selected cluster
    ui.refRadius.clear()
    ui.refPhi.clear()
    radius, dradius, phi, dphi = Calculator(rxs, rxserr, rys, ryserr, index)
    ui.refRadius.setText(str(radius)+" ("+str(dradius)+")")
    ui.refPhi.setText(str(phi)+" ("+str(dphi)+")")
    #If the other plot is loaded, recalculate the frequency
    text = self.measPhi.text()
    if text == "":
        text = "Nope"
    else:
        self.Enter()


def measCluster(index):
    #Recalculate the radius and angle of the plot for the selected cluster
    ui.measRadius.clear()
    ui.measPhi.clear()
    radius, dradius, phi, dphi = Calculator(mxs, mxserr, mys, myserr, index)
    ui.measRadius.setText(str(radius)+" ("+str(dradius)+")")
    ui.measPhi.setText(str(phi)+" ("+str(dphi)+")")
    #If the other plot is loaded, recalculate the frequency
    text = ui.refPhi.text()
    if text == "":
        text = "Nope"
    else:
        self.Enter()


def Enter(self):
    #When the "Calculate" button is clicked, check that both files are loaded
    #then calculate the frequency
    text = ui.refPhi.text()
    if text == "":
        string = "reference"
        ShowBox(string)
    else:
        rindex = ui.refClusterSelect.currentIndex()
        text = ui.measPhi.text()
        if text == "":
            string = "measurement"
            ShowBox(string)
        else:
            mindex = ui.measClusterSelect.currentIndex()
            N, theta, dtheta, frequency, dfrequency = Frequency(rxs, rxserr, rys, ryserr, rindex, mxs, mxserr, mys, myserr, mindex)
            ui.N.setText(str(N))
            ui.Frequency.setText(str(frequency) + " (" + str(dfrequency) +")")
            ui.Theta.setText(str(theta) + " (" + str(dtheta) + ")")
            

def ShowBox(string):
    msg = QtWidgets.QMessageBox()
    title = "Missing "+string+" file"
    message = "No "+string+" file is selected. Please select a "+string+" file."
    msg.setWindowTitle(title)
    msg.setText(message)
    msg.exec_()

def CalibrateSelect(self):
    cw = Ui_CalibrateWindow()
    cw.freqCCalc.clicked.connect(CalibrateCalc)
    cw.exec_()

def CalibrateCalc(self):
    print("Wahoo!")

def Exit(self):
    sys.ui.exit(app.exec_())

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

    #When the "calculate" button is clicked, go do stuff
    ui.EnterButton.clicked.connect(Enter)

    #When a combobox is used, recalculate the information for that file (not yet implemented)
    ui.refClusterSelect.activated.connect(refCluster)
    ui.measClusterSelect.activated.connect(measCluster)

    #When the menu bar is used to load files, go do stuff
    ui.actionLoad_New_Reference.triggered.connect(LoadReference)
    ui.actionLoad_New_Measurement.triggered.connect(LoadMeasurement)
    ui.actionExit.triggered.connect(Exit)
    ui.actionCalibrate.triggered.connect(CalibrateSelect)

    ui.sys.exit(app.exec_())
