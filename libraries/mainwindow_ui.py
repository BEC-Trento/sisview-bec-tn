# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Mon Jun  6 20:22:16 2016
#      by: PyQt4 UI code generator 4.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 600)
        font = QtGui.QFont()
        font.setPointSize(10)
        MainWindow.setFont(font)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.treeView = QtGui.QTreeView(self.centralwidget)
        self.treeView.setObjectName(_fromUtf8("treeView"))
        self.verticalLayout.addWidget(self.treeView)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuView = QtGui.QMenu(self.menubar)
        self.menuView.setObjectName(_fromUtf8("menuView"))
        MainWindow.setMenuBar(self.menubar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        MainWindow.insertToolBarBreak(self.toolBar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.dockWidget0 = QtGui.QDockWidget(MainWindow)
        self.dockWidget0.setObjectName(_fromUtf8("dockWidget0"))
        self.plotWidget0 = QtGui.QWidget()
        self.plotWidget0.setObjectName(_fromUtf8("plotWidget0"))
        self.plotLayout0 = QtGui.QVBoxLayout(self.plotWidget0)
        self.plotLayout0.setObjectName(_fromUtf8("plotLayout0"))
        self.dockWidget0.setWidget(self.plotWidget0)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockWidget0)
        self.dockWidget1 = QtGui.QDockWidget(MainWindow)
        self.dockWidget1.setObjectName(_fromUtf8("dockWidget1"))
        self.plotWidget1 = QtGui.QWidget()
        self.plotWidget1.setObjectName(_fromUtf8("plotWidget1"))
        self.plotLayout1 = QtGui.QVBoxLayout(self.plotWidget1)
        self.plotLayout1.setObjectName(_fromUtf8("plotLayout1"))
        self.dockWidget1.setWidget(self.plotWidget1)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockWidget1)
        self.actionOpen_Folder = QtGui.QAction(MainWindow)
        self.actionOpen_Folder.setObjectName(_fromUtf8("actionOpen_Folder"))
        self.menuFile.addAction(self.actionOpen_Folder)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuView.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "SISView", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.menuView.setTitle(_translate("MainWindow", "View", None))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar", None))
        self.dockWidget0.setWindowTitle(_translate("MainWindow", "Im0", None))
        self.dockWidget1.setWindowTitle(_translate("MainWindow", "Im1", None))
        self.actionOpen_Folder.setText(_translate("MainWindow", "Open Folder", None))

