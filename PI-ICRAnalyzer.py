# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from mainwindow import Ui_MainWindow
import pyqtgraph as pg
import re, csv, lmfit, matplotlib, pandas, scipy, numpy, fnmatch, sys, math
import sklearn.utils
from Definitions import *
from calibratewindow import Ui_CalibrateWindow
from isotopewindow import Ui_IsotopeWindow


def LoadReference(self):
    #This bit loads a new file and calls the files useful_phase and phase_fits_bank to find clusters in the data
    refFile, _filter = QtWidgets.QFileDialog.getOpenFileName(ui, 'Load Reference File', "data", "Text files (*.txt)")
    if refFile == "":
        string = "reference"
        ShowBox(string)
    else:
        global rxs, rxserr, rys, ryserr, rips, rxkeep, rykeep, rX, rnum, rlabels, rclusters, xCenter, yCenter
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
        radius, dradius, phi, dphi = Calculator(rxs, rxserr, rys, ryserr, cluster_of_interest, xCenter, yCenter)
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
        radius, dradius, phi, dphi = Calculator(mxs, mxserr, mys, myserr, cluster_of_interest, xCenter, yCenter)
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
    radius, dradius, phi, dphi = Calculator(rxs, rxserr, rys, ryserr, index, xCenter, yCenter)
    ui.refRadius.setText(str(radius)+" ("+str(dradius)+")")
    ui.refPhi.setText(str(phi)+" ("+str(dphi)+")")
    #If the other plot is loaded, recalculate the frequency
    text = ui.measPhi.text()
    if text != "":
        Enter()


def measCluster(index):
    #Recalculate the radius and angle of the plot for the selected cluster
    ui.measRadius.clear()
    ui.measPhi.clear()
    radius, dradius, phi, dphi = Calculator(mxs, mxserr, mys, myserr, index, xCenter, yCenter)
    ui.measRadius.setText(str(radius)+" ("+str(dradius)+")")
    ui.measPhi.setText(str(phi)+" ("+str(dphi)+")")
    #If the other plot is loaded, recalculate the frequency
    text = ui.refPhi.text()
    if text != "":
        Enter()


def Enter():
    #When the "Calculate" button is clicked, check that both files are loaded
    #then calculate the frequency
    global measTime
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
            try: measTime
            except NameError: measTime = "Missing"
            if measTime == "Missing":
                msg = QtWidgets.QMessageBox()
                title = "Missing accumulation time"
                message = "No accumulation time has been entered. Please enter an accumulation time."
                msg.setWindowTitle(title)
                msg.setText(message)
                msg.exec_()
            else:
                mindex = ui.measClusterSelect.currentIndex()
                N, theta, dtheta, frequency, dfrequency = Frequency(rxs, rxserr, rys, ryserr, rindex, mxs, mxserr, mys, myserr, mindex, expFreq, measTime, xCenter, yCenter)
                ui.N.setText(str(N))
                ui.Frequency.setText(str(frequency) + " (" + str(dfrequency) +")")
                ui.Theta.setText(str(theta) + " (" + str(dtheta) + ")")
def AddN():
    #Recalculate the frequency using the new N
    global measTime
    text = ui.N.text()
    newN = int(text)+1
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
            try: measTime
            except NameError: measTime = "Missing"
            if measTime == "Missing":
                msg = QtWidgets.QMessageBox()
                title = "Missing accumulation time"
                message = "No accumulation time has been entered. Please enter an accumulation time."
                msg.setWindowTitle(title)
                msg.setText(message)
                msg.exec_()
            else:
                mindex = ui.measClusterSelect.currentIndex()
                newTheta, newDtheta, newFrequency, newDfrequency = AddSubN(rxs, rxserr, rys, ryserr, rindex, mxs, mxserr, mys, myserr, mindex, expFreq, measTime, xCenter, yCenter, newN)
                ui.N.setText(str(newN))
                ui.Frequency.setText(str(newFrequency) + " (" + str(newDfrequency) +")")
                ui.Theta.setText(str(newTheta) + " (" + str(newDtheta) + ")")

def SubtractN():
    #Recalculate the frequency using the new N
    global measTime
    text = ui.N.text()
    newN = int(text)-1
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
            try: measTime
            except NameError: measTime = "Missing"
            if measTime == "Missing":
                msg = QtWidgets.QMessageBox()
                title = "Missing accumulation time"
                message = "No accumulation time has been entered. Please enter an accumulation time."
                msg.setWindowTitle(title)
                msg.setText(message)
                msg.exec_()
            else:
                mindex = ui.measClusterSelect.currentIndex()
                newTheta, newDtheta, newFrequency, newDfrequency = AddSubN(rxs, rxserr, rys, ryserr, rindex, mxs, mxserr, mys, myserr, mindex, expFreq, measTime, xCenter, yCenter, newN)
                ui.N.setText(str(newN))
                ui.Frequency.setText(str(newFrequency) + " (" + str(newDfrequency) +")")
                ui.Theta.setText(str(newTheta) + " (" + str(newDtheta) + ")")
    
            

def ShowBox(string):
    #The error mesage for missing files
    msg = QtWidgets.QMessageBox()
    title = "Missing "+string+" file"
    message = "No "+string+" file is selected. Please select a "+string+" file."
    msg.setWindowTitle(title)
    msg.setText(message)
    msg.exec_()

def MeasurementSelect(self):
    #The widget for changing information about the measurement,
    #such as the species of interest
    global iw
    iw = Ui_IsotopeWindow()
    iw.Nuclide.setText(measNuclide)
    iw.Charge.setText(str(measCharge))
    iw.Nuclide.returnPressed.connect(AcceptMeasurement)
    iw.Charge.returnPressed.connect(AcceptMeasurement)
    iw.acceptButton.clicked.connect(AcceptMeasurement)
    iw.cancelButton.clicked.connect(CancelMeasurement)
    iw.exec_()

def CalibrateSelect(self):
    #The widget for changing information about the calibration,
    #such as the species of interest
    global cw
    cw = Ui_CalibrateWindow()
    cw.Nuclide.setText(calibNuclide)
    cw.Charge.setText(str(calibCharge))
    cw.freqC.setText(str(calibFreqC))
    cw.freqPlus.setText(str(calibFreqPlus))
    cw.freqMinus.setText(str(calibFreqMinus))
    cw.xCenter.setText(str(xCenter))
    cw.yCenter.setText(str(yCenter))
    cw.xCenter.returnPressed.connect(AcceptCalibration)
    cw.yCenter.returnPressed.connect(AcceptCalibration)
    cw.Nuclide.returnPressed.connect(AcceptCalibration)
    cw.Charge.returnPressed.connect(AcceptCalibration)
    cw.freqCCalc.clicked.connect(CalibrateCalcC)
    cw.freqPlusCalc.clicked.connect(CalibrateCalcPlus)
    cw.freqMinusCalc.clicked.connect(CalibrateCalcMinus)
    cw.acceptButton.clicked.connect(AcceptCalibration)
    cw.cancelButton.clicked.connect(CancelCalibration)
    cw.exec_()

def CalibrateCalcC(self):
    #These three functions recalculate a frequency in the calibration file
    #when a button is pushed
    newFreqPlus = float(cw.freqPlus.text())
    newFreqMinus = float(cw.freqMinus.text())
    newFreqC = newFreqPlus + newFreqMinus
    cw.freqC.clear()
    cw.freqC.setText(str(newFreqC))

def CalibrateCalcPlus(self):
    #These three functions recalculate a frequency in the calibration file
    #when a button is pushed
    newFreqC = float(cw.freqC.text())
    newFreqMinus = float(cw.freqMinus.text())
    newFreqPlus = newFreqC - newFreqMinus
    cw.freqPlus.clear()
    cw.freqPlus.setText(str(newFreqPlus))

def CalibrateCalcMinus(self):
    #These three functions recalculate a frequency in the calibration file
    #when a button is pushed
    newFreqPlus = float(cw.freqPlus.text())
    newFreqC = float(cw.freqC.text())
    newFreqMinus = newFreqC - newFreqPlus
    cw.freqMinus.clear()
    cw.freqMinus.setText(str(newFreqMinus))

def AcceptCalibration():
    #When the "accept" button is clicked on the calibration widget,
    #get the new information, print it to the file, and pass it along
    newNuclide = cw.Nuclide.text()
    newCharge = cw.Charge.text()
    newFreqC = cw.freqC.text()
    newFreqPlus = cw.freqPlus.text()
    newFreqMinus = cw.freqMinus.text()
    newXCenter = cw.xCenter.text()
    newYCenter = cw.yCenter.text()
    
    try:
        calibFile = open('Calibration.xml', 'r')
        calibData = calibFile.read()
        calibData = re.sub(calibNuclide, newNuclide, calibData)
        calibData = re.sub("<charge>"+str(calibCharge)+"</charge>", "<charge>"+newCharge+"</charge>", calibData)
        calibData = re.sub(str(calibFreqC), newFreqC, calibData)
        calibData = re.sub(str(calibFreqPlus), newFreqPlus, calibData)
        calibData = re.sub(str(calibFreqMinus), newFreqMinus, calibData)
        calibFile.close()
        calibFile = open('Calibration.xml', 'w')
        calibFile.write(calibData)
        calibFile.close()
        NewCalibrationInfo(newNuclide, newCharge, newFreqC, newFreqPlus, newFreqMinus, newXCenter, newYCenter)
    except FileNotFoundError:
        string = "calibration"
        ShowBox(string)

    cw.close()
    

def NewCalibrationInfo(newNuclide, newCharge, newFreqC, newFreqPlus, newFreqMinus, newXCenter, newYCenter):
    #This changes the global calibration variables and recalculates
    #the reference and measurement angles
    global calibNuclide, calibCharge, calibFreqC, calibFreqPlus, calibFreqMinus, calibMass, xCenter, yCenter
    calibNuclide = newNuclide
    calibCharge = int(newCharge)
    calibFreqC = float(newFreqC)
    calibFreqPlus = float(newFreqPlus)
    calibFreqMinus = float(newFreqMinus)
    calibMass = CalibrationMass(calibNuclide, calibCharge)
    xCenter = float(newXCenter)
    yCenter = float(newYCenter)
    text = ui.refPhi.text()
    if text != "":
        cluster_of_interest = ui.refClusterSelect.currentIndex()
        radius, dradius, phi, dphi = Calculator(rxs, rxserr, rys, ryserr, cluster_of_interest, xCenter, yCenter)
        ui.refRadius.setText(str(radius)+" ("+str(dradius)+")")
        ui.refPhi.setText(str(phi)+" ("+str(dphi)+")")
    text = ui.measPhi.text()
    if text != "":
        cluster_of_interest = ui.measClusterSelect.currentIndex()
        radius, dradius, phi, dphi = Calculator(mxs, mxserr, mys, myserr, cluster_of_interest, xCenter, yCenter)
        ui.measRadius.setText(str(radius)+" ("+str(dradius)+")")
        ui.measPhi.setText(str(phi)+" ("+str(dphi)+")")
    text = ui.Theta.text()
    if text != "":
        Enter()

def CancelCalibration():
    #Close the calibration widget without doing anything if the "cancel"
    #button is clicked
    cw.close()

def AcceptMeasurement():
    #Get the new information from the "measurement" widget and
    #save it in the file
    newMeasNuclide = iw.Nuclide.text()
    newMeasCharge = iw.Charge.text()
    newMeasTime = iw.tAcc.text()
    try:
        measFile = open('Mass.xml', 'r')
        measData = measFile.read()
        measData = re.sub('<mi0 q="'+str(measCharge)+'" m="'+measNuclide, '<mi0 q="'+str(newMeasCharge)+'" m="'+newMeasNuclide, measData)
        measFile.close()
        measFile = open('Mass.xml', 'w')
        measFile.write(measData)
        measFile.close()
        if newMeasTime == "":
            msg = QtWidgets.QMessageBox()
            title = "Missing accumulation time"
            message = "No accumulation time has been entered. Please enter an accumulation time."
            msg.setWindowTitle(title)
            msg.setText(message)
            msg.exec_()
        else:
            NewMeasurementInfo(newMeasNuclide, newMeasCharge, newMeasTime)
            iw.close()
            text = ui.measPhi.text()
            if text != "":
                text = ui.refPhi.text()
                if text != "":
                    Enter()
    except FileNotFoundError:
        string = "measurement"
        ShowBox(string)
   

def NewMeasurementInfo(newMeasNuclide, newMeasCharge, newMeasTime):
    #Change the measurement global variables and recalculate the expected
    #frequency of the measured ion
    global measNuclide, measCharge, measTime, expFreq
    measNuclide = newMeasNuclide
    measCharge = int(newMeasCharge)
    measTime = float(newMeasTime)
    ui.Species.setText(measNuclide)
    expFreq = ExpectedFrequency(calibMass, calibFreqC, measNuclide, measCharge)

def CancelMeasurement():
    #Close the measurement widget without doing anything if the "cancel"
    #button is clicked
    iw.close()

    
def CalibrateInfo(self):
    #Read in the information from the calibrate file before starting
    global calibNuclide, calibCharge, calibFreqC, calibFreqPlus, calibFreqMinus, calibMass, xCenter, yCenter
    calibNuclide = "1K39"
    calibCharge = 1
    calibFreqC = 3688955.2387
    calibFreqPlus = 3686369.6998
    calibFreqMinus = 2585.5389
    xCenter = -2
    yCenter = -2
    try:
        calibFile = open('Calibration.xml', 'r')
        calibData = calibFile.readlines()
        calibFile.close()
        calibNuclide = (calibData[1].split('<nuclide>')[1]).split('</nuclide>')[0]
        calibCharge = int((calibData[2].split('<charge>')[1]).split('</charge>')[0])
        calibFreqC = float((calibData[4].split('<freq>')[1]).split('</freq>')[0])
        calibFreqPlus = float((calibData[12].split('<freq>')[1]).split('</freq>')[0])
        calibFreqMinus = float((calibData[20].split('<freq>')[1]).split('</freq>')[0])

    except FileNotFoundError:
        string = "calibration"
        ShowBox(string)

    calibMass = CalibrationMass(calibNuclide, calibCharge)

def MeasInfo(self):
    #Read in the info from the measurement file before starting
    global measNuclide, measCharge, measTime, expFreq
    measNuclide = "1K39"
    measCharge = 1
    try:
        measFile = open('Mass.xml', 'r')
        measData = measFile.readlines()
        measFile.close()
        measNuclide = (measData[2].split('m="')[1]).split('"/>')[0]
        measCharge = int((measData[2].split('q="')[1]).split('"')[0])

    except FileNotFoundError:
        string = "measurement"
        ShowBox(string)
    ui.Species.setText(measNuclide)

    expFreq = ExpectedFrequency(calibMass, calibFreqC, measNuclide, measCharge)

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
    CalibrateInfo(MainWindow)
    MeasInfo(MainWindow)
    MainWindow.show()

    #When the "calculate" button is clicked, go do stuff
    ui.EnterButton.clicked.connect(Enter)
    ui.nPlus.clicked.connect(AddN)
    ui.nMinus.clicked.connect(SubtractN)

    #When a combobox is used, recalculate the information for that file (not yet implemented)
    ui.refClusterSelect.activated.connect(refCluster)
    ui.measClusterSelect.activated.connect(measCluster)

    #When the menu bar is used to load files, go do stuff
    ui.actionLoad_New_Reference.triggered.connect(LoadReference)
    ui.actionLoad_New_Measurement.triggered.connect(LoadMeasurement)
    ui.actionExit.triggered.connect(Exit)
    ui.actionCalibrate.triggered.connect(CalibrateSelect)
    ui.actionMeasurement.triggered.connect(MeasurementSelect)

    ui.sys.exit(app.exec_())
