# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\calibratewindow.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


#class Ui_CalibrateWindow(object):
class Ui_CalibrateWindow(QtGui.QDialog):
    def __init__(self, parent=None):
        super(Ui_CalibrateWindow, self).__init__(parent)
        self.setupUi(self)
        
    def setupUi(self, CalibrateWindow):
        CalibrateWindow.setObjectName("CalibrateWindow")
        CalibrateWindow.resize(230, 150)
        self.label = QtWidgets.QLabel(CalibrateWindow)
        self.label.setGeometry(QtCore.QRect(10, 10, 47, 20))
        self.label.setObjectName("label")
        self.Nuclide = QtWidgets.QLineEdit(CalibrateWindow)
        self.Nuclide.setGeometry(QtCore.QRect(50, 10, 60, 20))
        self.Nuclide.setObjectName("Nuclide")
        self.label_2 = QtWidgets.QLabel(CalibrateWindow)
        self.label_2.setGeometry(QtCore.QRect(130, 10, 47, 20))
        self.label_2.setObjectName("label_2")
        self.Charge = QtWidgets.QLineEdit(CalibrateWindow)
        self.Charge.setGeometry(QtCore.QRect(170, 10, 50, 20))
        self.Charge.setObjectName("Charge")
        self.label_3 = QtWidgets.QLabel(CalibrateWindow)
        self.label_3.setGeometry(QtCore.QRect(10, 60, 47, 20))
        self.label_3.setObjectName("label_3")
        self.freqCCalc = QtWidgets.QPushButton(CalibrateWindow)
        self.freqCCalc.setGeometry(QtCore.QRect(50, 60, 20, 20))
        self.freqCCalc.setObjectName("freqCCalc")
        self.label_4 = QtWidgets.QLabel(CalibrateWindow)
        self.label_4.setGeometry(QtCore.QRect(10, 90, 47, 20))
        self.label_4.setObjectName("label_4")
        self.freqPlusCalc = QtWidgets.QPushButton(CalibrateWindow)
        self.freqPlusCalc.setGeometry(QtCore.QRect(50, 90, 20, 20))
        self.freqPlusCalc.setObjectName("freqPlusCalc")
        self.freqMinusCalc = QtWidgets.QPushButton(CalibrateWindow)
        self.freqMinusCalc.setGeometry(QtCore.QRect(50, 120, 20, 20))
        self.freqMinusCalc.setObjectName("freqMinusCalc")
        self.label_5 = QtWidgets.QLabel(CalibrateWindow)
        self.label_5.setGeometry(QtCore.QRect(10, 120, 47, 20))
        self.label_5.setObjectName("label_5")
        self.freqC = QtWidgets.QLineEdit(CalibrateWindow)
        self.freqC.setGeometry(QtCore.QRect(90, 60, 130, 20))
        self.freqC.setObjectName("freqC")
        self.freqPlus = QtWidgets.QLineEdit(CalibrateWindow)
        self.freqPlus.setGeometry(QtCore.QRect(90, 90, 130, 20))
        self.freqPlus.setObjectName("freqPlus")
        self.freqMinus = QtWidgets.QLineEdit(CalibrateWindow)
        self.freqMinus.setGeometry(QtCore.QRect(90, 120, 130, 20))
        self.freqMinus.setObjectName("freqMinus")

        self.retranslateUi(CalibrateWindow)
        QtCore.QMetaObject.connectSlotsByName(CalibrateWindow)

    def retranslateUi(self, CalibrateWindow):
        _translate = QtCore.QCoreApplication.translate
        CalibrateWindow.setWindowTitle(_translate("CalibrateWindow", "Dialog"))
        self.label.setText(_translate("CalibrateWindow", "Nuclide"))
        self.label_2.setText(_translate("CalibrateWindow", "Charge"))
        self.label_3.setText(_translate("CalibrateWindow", "nu c"))
        self.freqCCalc.setText(_translate("CalibrateWindow", "C"))
        self.label_4.setText(_translate("CalibrateWindow", "nu +"))
        self.freqPlusCalc.setText(_translate("CalibrateWindow", "C"))
        self.freqMinusCalc.setText(_translate("CalibrateWindow", "C"))
        self.label_5.setText(_translate("CalibrateWindow", "nu -"))


