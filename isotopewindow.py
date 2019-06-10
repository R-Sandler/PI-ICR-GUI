from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_IsotopeWindow(QtGui.QDialog):
    import sys
    def __init__(self, parent=None):
        super(Ui_IsotopeWindow, self).__init__(parent)
        self.setupUi(self)

    def setupUi(self, IsotopeWindow):
        IsotopeWindow.setObjectName("IsotopeWindow")
        IsotopeWindow.resize(230, 200)
        self.label = QtWidgets.QLabel(IsotopeWindow)
        self.label.setGeometry(QtCore.QRect(10, 10, 47, 20))
        self.label.setObjectName("label")
        self.Nuclide = QtWidgets.QLineEdit(IsotopeWindow)
        self.Nuclide.setGeometry(QtCore.QRect(50, 10, 60, 20))
        self.Nuclide.setObjectName("Nuclide")
        self.label_2 = QtWidgets.QLabel(IsotopeWindow)
        self.label_2.setGeometry(QtCore.QRect(130, 10, 47, 20))
        self.label_2.setObjectName("label_2")
        self.Charge = QtWidgets.QLineEdit(IsotopeWindow)
        self.Charge.setGeometry(QtCore.QRect(170, 10, 50, 20))
        self.Charge.setObjectName("Charge")
        self.label_3 = QtWidgets.QLabel(IsotopeWindow)
        self.label_3.setGeometry(QtCore.QRect(10, 40, 47, 20))
        self.label_3.setObjectName("label_3")
        self.acceptButton = QtWidgets.QPushButton(IsotopeWindow)
        self.acceptButton.setGeometry(QtCore.QRect(10, 80, 210, 50))
        self.acceptButton.setObjectName("acceptButton")
        self.cancelButton = QtWidgets.QPushButton(IsotopeWindow)
        self.cancelButton.setGeometry(QtCore.QRect(10, 140, 210, 50))
        self.cancelButton.setObjectName("cancelButton")
        self.tAcc = QtWidgets.QLineEdit(IsotopeWindow)
        self.tAcc.setGeometry(QtCore.QRect(50, 40, 130, 20))
        self.tAcc.setObjectName("tAcc")


        self.retranslateUi(IsotopeWindow)
        QtCore.QMetaObject.connectSlotsByName(IsotopeWindow)

    def retranslateUi(self, IsotopeWindow):
        _translate = QtCore.QCoreApplication.translate
        IsotopeWindow.setWindowTitle(_translate("IsotopeWindow", "Measurement"))
        self.label.setText(_translate("IsotopeWindow", "Nuclide"))
        self.label_2.setText(_translate("IsotopeWindow", "Charge"))
        self.label_3.setText(_translate("IsotopeWindow", "t acc"))
        self.acceptButton.setText(_translate("IsotopeWindow", "Accept"))
        self.cancelButton.setText(_translate("IsotopeWindow", "Cancel"))
