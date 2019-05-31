# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widget.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Widget(object):
    def setupUi(self, Widget):
        Widget.setObjectName("Widget")
        Widget.resize(300, 60)
        self.layoutWidget = QtWidgets.QWidget(Widget)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 281, 53))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(1, 1, 11, 11)
        self.verticalLayout.setSpacing(1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.EnterName = QtWidgets.QLineEdit(self.layoutWidget)
        self.EnterName.setObjectName("EnterName")
        self.horizontalLayout.addWidget(self.EnterName)
        self.EnterButton = QtWidgets.QPushButton(self.layoutWidget)
        self.EnterButton.setDefault(False)
        self.EnterButton.setFlat(False)
        self.EnterButton.setObjectName("EnterButton")
        self.horizontalLayout.addWidget(self.EnterButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.lineEdit = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit.setEnabled(True)
        self.lineEdit.setFocusPolicy(QtCore.Qt.TabFocus)
        self.lineEdit.setInputMethodHints(QtCore.Qt.ImhNone)
        self.lineEdit.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.lineEdit.setPlaceholderText("")
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)

        self.retranslateUi(Widget)
        self.EnterButton.clicked.connect(self.Submit)
        QtCore.QMetaObject.connectSlotsByName(Widget)

    def Submit(self):
        name = self.EnterName.text()

        if name == "":
            self.lineEdit.setText("What is your name?")
        else:
            self.lineEdit.setText("Hello, "+name+"!")

    def retranslateUi(self, Widget):
        _translate = QtCore.QCoreApplication.translate
        Widget.setWindowTitle(_translate("Widget", "Widget"))
        self.label.setText(_translate("Widget", "My name is:"))
        self.EnterButton.setText(_translate("Widget", "Enter"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Widget = QtWidgets.QWidget()
    ui = Ui_Widget()
    ui.setupUi(Widget)
    Widget.show()
    sys.exit(app.exec_())
