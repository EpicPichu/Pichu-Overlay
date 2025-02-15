# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test2.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineView

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(818, 439)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")

        self.html_display = QWebEngineView(self.centralwidget)
        self.html_display.setMinimumSize(QtCore.QSize(800, 400))
        #self.html_display.setResizeMode(QtQuickWidgets.QQuickWidget.SizeRootObjectToView)
        self.html_display.setObjectName("html_display")

        self.gridLayout.addWidget(self.html_display, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 818, 21))
        self.menubar.setObjectName("menubar")
        self.menuMenu = QtWidgets.QMenu(self.menubar)
        self.menuMenu.setObjectName("menuMenu")
        self.menuSet_Client = QtWidgets.QMenu(self.menuMenu)
        self.menuSet_Client.setObjectName("menuSet_Client")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.actionLunar_Client = QtWidgets.QAction(MainWindow)
        self.actionLunar_Client.setCheckable(False)
        self.actionLunar_Client.setObjectName("actionCustom")
        self.actionCustom = QtWidgets.QAction(MainWindow)
        self.actionCustom.setCheckable(False)
        self.actionCustom.setObjectName("actionCustom")
        self.actionBadlion_Client = QtWidgets.QAction(MainWindow)
        self.actionBadlion_Client.setCheckable(False)
        self.actionBadlion_Client.setObjectName("actionBadlion_Client")
        self.actionVanilla_Launcher = QtWidgets.QAction(MainWindow)
        self.actionVanilla_Launcher.setCheckable(False)
        self.actionVanilla_Launcher.setObjectName("actionVanilla_Launcher")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionTutorial = QtWidgets.QAction(MainWindow)
        self.actionTutorial.setObjectName("actionTutorial")
        self.actionGithub = QtWidgets.QAction(MainWindow)
        self.actionGithub.setObjectName("actionGithub")
        self.actionVersion = QtWidgets.QAction(MainWindow)
        self.actionVersion.setEnabled(False)
        self.actionVersion.setObjectName("actionVersion")
        self.actionDiscord = QtWidgets.QAction(MainWindow)
        self.actionDiscord.setObjectName("actionDiscord")
        self.menuSet_Client.addAction(self.actionLunar_Client)
        self.menuSet_Client.addAction(self.actionBadlion_Client)
        self.menuSet_Client.addAction(self.actionVanilla_Launcher)
        self.menuSet_Client.addAction(self.actionCustom)
        self.menuMenu.addAction(self.menuSet_Client.menuAction())
        self.menuMenu.addSeparator()
        self.menuMenu.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionTutorial)
        self.menuHelp.addAction(self.actionDiscord)
        self.menuHelp.addAction(self.actionGithub)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionVersion)
        self.menubar.addAction(self.menuMenu.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuMenu.setTitle(_translate("MainWindow", "Menu"))
        self.menuSet_Client.setTitle(_translate("MainWindow", "Set Client"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionLunar_Client.setText(_translate("MainWindow", "Lunar Client"))
        self.actionBadlion_Client.setText(_translate("MainWindow", "Badlion Client"))
        self.actionVanilla_Launcher.setText(_translate("MainWindow", "Vanilla Launcher"))
        self.actionCustom.setText(_translate("MainWindow", "Custom"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionTutorial.setText(_translate("MainWindow", "Tutorial"))
        self.actionGithub.setText(_translate("MainWindow", "Github"))
        self.actionVersion.setText(_translate("MainWindow", "Version"))
        self.actionDiscord.setText(_translate("MainWindow", "Discord"))
from PyQt5 import QtQuickWidgets
