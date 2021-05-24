# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interface.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(806, 367)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setMinimumSize(QtCore.QSize(0, 40))
        self.pushButton.setMaximumSize(QtCore.QSize(16777215, 20))
        self.pushButton.setObjectName("pushButton")
        self.gridLayout_2.addWidget(self.pushButton, 3, 1, 1, 1)
        self.spinBox = QtWidgets.QSpinBox(self.frame)
        self.spinBox.setMinimumSize(QtCore.QSize(0, 40))
        self.spinBox.setMinimum(1)
        self.spinBox.setObjectName("spinBox")
        self.gridLayout_2.addWidget(self.spinBox, 3, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setMinimumSize(QtCore.QSize(0, 30))
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 16))
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setMaximumSize(QtCore.QSize(16777215, 16))
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 0, 1, 1, 1)
        self.comboBox = QtWidgets.QComboBox(self.frame)
        self.comboBox.setMinimumSize(QtCore.QSize(0, 40))
        self.comboBox.setMaximumSize(QtCore.QSize(350, 16777215))
        self.comboBox.setObjectName("comboBox")
        self.gridLayout_2.addWidget(self.comboBox, 1, 1, 1, 1)
        self.search_key = QtWidgets.QLineEdit(self.frame)
        self.search_key.setMinimumSize(QtCore.QSize(300, 40))
        self.search_key.setMaximumSize(QtCore.QSize(350, 16777215))
        self.search_key.setObjectName("search_key")
        self.gridLayout_2.addWidget(self.search_key, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 2, 0, 1, 1)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 806, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "SEARCH"))
        self.label_2.setText(_translate("MainWindow", "Search key:"))
        self.label_3.setText(_translate("MainWindow", "Country:"))
        self.search_key.setPlaceholderText(_translate("MainWindow", "Search key"))
        self.label.setText(_translate("MainWindow", "Number of Results:"))

