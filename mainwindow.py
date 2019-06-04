# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg
from useful_phase import *
from phase_fits_bank import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("PI-ICR Analysis")
        MainWindow.resize(1500, 1000)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        #self.frame = QtWidgets.QFrame(self.centralWidget)
        #self.frame.setGeometry(QtCore.QRect(20, 10, 301, 301))
        #self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        #self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        #self.frame.setObjectName("frame")
        self.frame_2 = QtWidgets.QFrame(self.centralWidget)
        self.frame_2.setGeometry(QtCore.QRect(350, 10, 301, 301))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.refClusterSelect = QtWidgets.QComboBox(self.centralWidget)
        self.refClusterSelect.setGeometry(QtCore.QRect(20, 540, 500, 22))
        self.refClusterSelect.setObjectName("refClusterSelect")
        self.measClusterSelect = QtWidgets.QComboBox(self.centralWidget)
        self.measClusterSelect.setGeometry(QtCore.QRect(880, 540, 500, 22))
        self.measClusterSelect.setObjectName("measClusterSelect")
        self.refPhi = QtWidgets.QLineEdit(self.centralWidget)
        self.refPhi.setGeometry(QtCore.QRect(220, 570, 200, 20))
        self.refPhi.setObjectName("refPhi")
        self.measPhi = QtWidgets.QLineEdit(self.centralWidget)
        self.measPhi.setGeometry(QtCore.QRect(1080, 570, 200, 20))
        self.measPhi.setObjectName("measPhi")
        self.label = QtWidgets.QLabel(self.centralWidget)
        self.label.setGeometry(QtCore.QRect(100, 570, 71, 20))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralWidget)
        self.label_2.setGeometry(QtCore.QRect(960, 570, 71, 20))
        self.label_2.setObjectName("label_2")
        self.refRadius = QtWidgets.QLineEdit(self.centralWidget)
        self.refRadius.setGeometry(QtCore.QRect(220, 600, 200, 20))
        self.refRadius.setObjectName("refRadius")
        self.measRadius = QtWidgets.QLineEdit(self.centralWidget)
        self.measRadius.setGeometry(QtCore.QRect(1080, 600, 200, 20))
        self.measRadius.setObjectName("measRadius")
        self.label_3 = QtWidgets.QLabel(self.centralWidget)
        self.label_3.setGeometry(QtCore.QRect(100, 600, 71, 20))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralWidget)
        self.label_4.setGeometry(QtCore.QRect(960, 600, 71, 20))
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
        self.actionLoad_New_Reference = fileMenu.addAction("Load New Reference")
        self.actionLoad_New_Measurement = fileMenu.addAction("Load New Measurement")

        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        self.refGraph = pg.PlotWidget(self.centralWidget)
        self.refGraph.setObjectName("refGraph")
        self.refGraph.setGeometry(QtCore.QRect(20, 30, 500, 500))


        self.retranslateUi(MainWindow)
        self.actionLoad_New_Reference.triggered.connect(self.LoadReference)
        self.actionLoad_New_Measurement.triggered.connect(self.LoadMeasurement)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def LoadReference(self):
        self.refClusterSelect.clear()
        refFile, _filter = QtWidgets.QFileDialog.getOpenFileName(self.centralWidget, 'Load Reference File', "data", "Text files (*.txt)")
        rXPOS,rYPOS,rTOF,rSUMX,rSUMY,rdf2 = poswithtof(refFile, -35000, -25000)
        rxs, rxserr, rys, ryserr, rips, rxkeep, rykeep, X, num, labels, clusters = cluster_spots(rXPOS, rYPOS, 1, 1)
        ClusterList = []
        for i in range(0,num):
            ClusterList.append(str(i))
        self.refClusterSelect.addItems(ClusterList)
        self.CreatePlot(X, labels, clusters)
        

    def LoadMeasurement(self):
        self.measClusterSelect.clear()
        measFile, _filter = QtWidgets.QFileDialog.getOpenFileName(self.centralWidget, 'Load Measurement File', "data", "Text files (*.txt)")
        mXPOS,mYPOS,mTOF,mSUMX,mSUMY,mdf2 = poswithtof(measFile, -35000, -25000)
        mxs, mxserr, mys, myserr, mips, mxkeep, mykeep = cluster_spots(mXPOS, mYPOS, 1, 0.5)
        Clusters = []
        for i in range(0,len(mxs)):
            Clusters.append(str(i))
        self.measClusterSelect.addItems(Clusters)

    def CreatePlot(self, data, labels, clusters):
        #L = [1,2,3,4,5]
        #self.refGraph.plot(L)
        #colors = ['blue', 'salmon', 'darkorange', 'cadetblue', 'sage', 'yellow', 'green', 'black', 'cyan', 'indianred', 'chartreuse', 'seagreen', 'purple', 'aliceblue']
        colors = ['b', 'r', 'g', 'c', 'y', 'm', 'w']
        self.refGraph.setXRange(-13,7, padding=0)
        self.refGraph.setYRange(-6,14, padding=0)
        for k, col in zip(unique(labels), colors):
        #self.refGraph.plot(X[0,0], X[0,1], pen = None, symbol='o')
        #for k in range(0,len(X)):
            my = labels == k
            #self.refGraph.plot(data[k, 0], data[k, 1], symbol='o', symbolBrush = colors[k])
            self.refGraph.plot(data[my,0], data[my,1], pen=None, symbol='o', symbolBrush = colors[k])
            #self.refGraph.plot([k],[k+1], symbol='o', symbolBrush=colors[k])
        #for i in range(0,num):
        #    plt.text(-12,10 - i,'%s: %.1f%%'%(colors[i],100.0*ips[i]/sum(ips)))
        #plt.text(-12,12, 'total:%i'%sum(ips))
        self.refGraph.plot(clusters[:,0], clusters[:,1], pen=None, symbol='o', symbolSize=10, symbolBrush = 'k')
        #plot.show()



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

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QWidget()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
