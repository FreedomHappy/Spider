# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sqt.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1081, 549)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.SingleBt = QtWidgets.QPushButton(self.centralwidget)
        self.SingleBt.setGeometry(QtCore.QRect(219, 52, 71, 23))
        self.SingleBt.setObjectName("SingleBt")
        self.urlLine = QtWidgets.QLineEdit(self.centralwidget)
        self.urlLine.setGeometry(QtCore.QRect(80, 53, 133, 20))
        self.urlLine.setObjectName("urlLine")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(32, 52, 42, 16))
        self.label.setObjectName("label")
        self.urlpool = QtWidgets.QListWidget(self.centralwidget)
        self.urlpool.setGeometry(QtCore.QRect(30, 90, 261, 411))
        self.urlpool.setObjectName("urlpool")
        self.Top250Bt = QtWidgets.QPushButton(self.centralwidget)
        self.Top250Bt.setGeometry(QtCore.QRect(310, 10, 75, 23))
        self.Top250Bt.setObjectName("Top250Bt")
        self.nowplayingBt = QtWidgets.QPushButton(self.centralwidget)
        self.nowplayingBt.setGeometry(QtCore.QRect(310, 50, 75, 23))
        self.nowplayingBt.setObjectName("nowplayingBt")
        self.movinfopool = QtWidgets.QListWidget(self.centralwidget)
        self.movinfopool.setGeometry(QtCore.QRect(310, 90, 351, 411))
        self.movinfopool.setObjectName("movinfopool")
        self.updateBt = QtWidgets.QPushButton(self.centralwidget)
        self.updateBt.setGeometry(QtCore.QRect(460, 50, 75, 23))
        self.updateBt.setObjectName("updateBt")
        self.commentpool = QtWidgets.QListWidget(self.centralwidget)
        self.commentpool.setGeometry(QtCore.QRect(685, 90, 381, 411))
        self.commentpool.setObjectName("commentpool")
        self.commentBt = QtWidgets.QPushButton(self.centralwidget)
        self.commentBt.setGeometry(QtCore.QRect(690, 50, 75, 23))
        self.commentBt.setObjectName("commentBt")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1081, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Spider"))
        self.SingleBt.setText(_translate("MainWindow", "爬取"))
        self.urlLine.setText(_translate("MainWindow", "请输入电影URL"))
        self.urlLine.selectAll()
        self.urlLine.setFocus()
        self.label.setText(_translate("MainWindow", "电影URL"))
        self.Top250Bt.setText(_translate("MainWindow", "Top250"))
        self.nowplayingBt.setText(_translate("MainWindow", "正在上映"))
        self.updateBt.setText(_translate("MainWindow", "刷新"))
        self.commentBt.setText(_translate("MainWindow", "爬取评论"))

