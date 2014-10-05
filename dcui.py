# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DropletCommander.ui'
#
# Created: Sat Oct  4 12:19:39 2014
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 801, 551))
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.West)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setObjectName("tabWidget")
        self.tabDroplets = QtWidgets.QWidget()
        self.tabDroplets.setObjectName("tabDroplets")
        self.pushButton = QtWidgets.QPushButton(self.tabDroplets)
        self.pushButton.setGeometry(QtCore.QRect(20, 220, 85, 26))
        self.pushButton.setObjectName("pushButton")
        self.treeDroplets = QtWidgets.QTreeWidget(self.tabDroplets)
        self.treeDroplets.setGeometry(QtCore.QRect(10, 10, 661, 191))
        self.treeDroplets.setMinimumSize(QtCore.QSize(661, 0))
        self.treeDroplets.setMaximumSize(QtCore.QSize(661, 16777215))
        self.treeDroplets.setObjectName("treeDroplets")
        self.treeDroplets.header().setCascadingSectionResizes(False)
        self.treeDroplets.header().setDefaultSectionSize(200)
        self.treeDroplets.header().setMinimumSectionSize(16)
        self.treeDroplets.header().setStretchLastSection(True)
        self.tabWidget.addTab(self.tabDroplets, "")
        self.tabSettings = QtWidgets.QWidget()
        self.tabSettings.setObjectName("tabSettings")
        self.btnSaveApiKey = QtWidgets.QPushButton(self.tabSettings)
        self.btnSaveApiKey.setGeometry(QtCore.QRect(20, 80, 85, 26))
        self.btnSaveApiKey.setObjectName("btnSaveApiKey")
        self.layoutWidget = QtWidgets.QWidget(self.tabSettings)
        self.layoutWidget.setGeometry(QtCore.QRect(23, 32, 581, 29))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.txtApiKey = QtWidgets.QLineEdit(self.layoutWidget)
        self.txtApiKey.setObjectName("txtApiKey")
        self.horizontalLayout_2.addWidget(self.txtApiKey)
        self.tabWidget.addTab(self.tabSettings, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 25))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.menuFile.addAction(self.actionQuit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Get Droplets"))
        self.treeDroplets.headerItem().setText(0, _translate("MainWindow", "Droplet"))
        self.treeDroplets.headerItem().setText(1, _translate("MainWindow", "IP address"))
        self.treeDroplets.headerItem().setText(2, _translate("MainWindow", "Region"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabDroplets), _translate("MainWindow", "Droplets"))
        self.btnSaveApiKey.setText(_translate("MainWindow", "Save API Key"))
        self.label_3.setText(_translate("MainWindow", "API Key: "))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabSettings), _translate("MainWindow", "Settings"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionQuit.setShortcut(_translate("MainWindow", "Alt+Q"))

