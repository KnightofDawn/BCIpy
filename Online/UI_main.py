# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'BCI.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(798, 550)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.graph = PlotWidget(self.centralwidget)
        self.graph.setGeometry(QtCore.QRect(30, 80, 721, 241))
        self.graph.setObjectName("graph")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(390, 30, 131, 31))
        self.textEdit.setObjectName("textEdit")
        self.title = QtWidgets.QLabel(self.centralwidget)
        self.title.setGeometry(QtCore.QRect(40, 20, 211, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.title.setFont(font)
        self.title.setScaledContents(False)
        self.title.setObjectName("title")
        self.user = QtWidgets.QLabel(self.centralwidget)
        self.user.setGeometry(QtCore.QRect(290, 40, 101, 21))
        self.user.setObjectName("user")
        self.graph_2 = PlotWidget(self.centralwidget)
        self.graph_2.setGeometry(QtCore.QRect(30, 360, 721, 101))
        self.graph_2.setObjectName("graph_2")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(610, 30, 89, 25))
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 798, 28))
        self.menubar.setObjectName("menubar")
        self.menuOperation = QtWidgets.QMenu(self.menubar)
        self.menuOperation.setObjectName("menuOperation")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionConnect = QtWidgets.QAction(MainWindow)
        self.actionConnect.setObjectName("actionConnect")
        self.actionDisconnect = QtWidgets.QAction(MainWindow)
        self.actionDisconnect.setObjectName("actionDisconnect")
        self.menuOperation.addAction(self.actionConnect)
        self.menuOperation.addAction(self.actionDisconnect)
        self.menubar.addAction(self.menuOperation.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.textEdit.setHtml(_translate("MainWindow",
                                         "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                         "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                         "p, li { white-space: pre-wrap; }\n"
                                         "</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
                                         "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">default</p></body></html>"))
        self.title.setText(_translate("MainWindow", "BCI Control Platform"))
        self.user.setText(_translate("MainWindow", "User Name:"))
        self.pushButton.setText(_translate("MainWindow", "Screen"))
        self.menuOperation.setTitle(_translate("MainWindow", "Opt"))
        self.actionConnect.setText(_translate("MainWindow", "Connect"))
        self.actionDisconnect.setText(_translate("MainWindow", "Disconnect"))


from pyqtgraph import PlotWidget
