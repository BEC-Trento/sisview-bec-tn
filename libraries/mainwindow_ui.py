# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Fri Jun 10 14:51:19 2016
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
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/lens.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.fileTreeLabel = QtGui.QLabel(self.centralwidget)
        self.fileTreeLabel.setObjectName(_fromUtf8("fileTreeLabel"))
        self.verticalLayout.addWidget(self.fileTreeLabel)
        self.treeView = QtGui.QTreeView(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeView.sizePolicy().hasHeightForWidth())
        self.treeView.setSizePolicy(sizePolicy)
        self.treeView.setObjectName(_fromUtf8("treeView"))
        self.treeView.header().setCascadingSectionResizes(True)
        self.treeView.header().setStretchLastSection(True)
        self.verticalLayout.addWidget(self.treeView)
        self.csvLabel = QtGui.QLabel(self.centralwidget)
        self.csvLabel.setObjectName(_fromUtf8("csvLabel"))
        self.verticalLayout.addWidget(self.csvLabel)
        self.tableWidget = CsvQTableWidget(self.centralwidget)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.verticalLayout.addWidget(self.tableWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuView = QtGui.QMenu(self.menubar)
        self.menuView.setObjectName(_fromUtf8("menuView"))
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        MainWindow.setMenuBar(self.menubar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.dockWidget0 = QtGui.QDockWidget(MainWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dockWidget0.sizePolicy().hasHeightForWidth())
        self.dockWidget0.setSizePolicy(sizePolicy)
        self.dockWidget0.setObjectName(_fromUtf8("dockWidget0"))
        self.plotWidget0 = PlotQWidget()
        self.plotWidget0.setObjectName(_fromUtf8("plotWidget0"))
        self.dockWidget0.setWidget(self.plotWidget0)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockWidget0)
        self.dockWidget1 = QtGui.QDockWidget(MainWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dockWidget1.sizePolicy().hasHeightForWidth())
        self.dockWidget1.setSizePolicy(sizePolicy)
        self.dockWidget1.setObjectName(_fromUtf8("dockWidget1"))
        self.plotWidget1 = PlotQWidget()
        self.plotWidget1.setObjectName(_fromUtf8("plotWidget1"))
        self.dockWidget1.setWidget(self.plotWidget1)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockWidget1)
        self.actionOpen_Folder = QtGui.QAction(MainWindow)
        self.actionOpen_Folder.setObjectName(_fromUtf8("actionOpen_Folder"))
        self.actionInfo = QtGui.QAction(MainWindow)
        self.actionInfo.setObjectName(_fromUtf8("actionInfo"))
        self.actionQuit = QtGui.QAction(MainWindow)
        self.actionQuit.setObjectName(_fromUtf8("actionQuit"))
        self.menuFile.addAction(self.actionOpen_Folder)
        self.menuFile.addAction(self.actionQuit)
        self.menuHelp.addAction(self.actionInfo)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "SISView", None))
        self.fileTreeLabel.setText(_translate("MainWindow", "File Tree View", None))
        self.csvLabel.setText(_translate("MainWindow", "Display CSV", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.menuView.setTitle(_translate("MainWindow", "View", None))
        self.menuHelp.setTitle(_translate("MainWindow", "Help", None))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar", None))
        self.dockWidget0.setWindowTitle(_translate("MainWindow", "Im0", None))
        self.dockWidget1.setWindowTitle(_translate("MainWindow", "Im1", None))
        self.actionOpen_Folder.setText(_translate("MainWindow", "Open Folder", None))
        self.actionOpen_Folder.setShortcut(_translate("MainWindow", "Ctrl+O", None))
        self.actionInfo.setText(_translate("MainWindow", "Info", None))
        self.actionInfo.setShortcut(_translate("MainWindow", "F11", None))
        self.actionQuit.setText(_translate("MainWindow", "Quit", None))
        self.actionQuit.setShortcut(_translate("MainWindow", "Ctrl+Q", None))

from libraries.csvqtablewidget import CsvQTableWidget
from libraries.plotqwidget import PlotQWidget
import resources_rc
