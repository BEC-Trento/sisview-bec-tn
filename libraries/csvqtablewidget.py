# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
"""
Created on Sun May 24 01:46:57 2015

@author: carmelo
"""
from PyQt4 import QtCore, QtGui
import os, csv

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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.setWindowModality(QtCore.Qt.WindowModal)
        Dialog.resize(236, 300)
        Dialog.setAutoFillBackground(False)
        self.verticalLayout_3 = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.scrollArea = QtGui.QScrollArea(Dialog)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 216, 243))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.verticalLayout = QtGui.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_3.addWidget(self.scrollArea)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout_3.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Select visible columns", None))


class CsvQTableWidget(QtGui.QTableWidget):
    
    def __init__(self, *args, **kwargs):
        super(CsvQTableWidget, self).__init__(*args, **kwargs)
        
    def setupUi(self, setMainWindow):
        self.mainWindow = setMainWindow
        self.CSVName = ''
        self.imagesPath = ''
        self.setVisibleDialog = None
        self.setVisibleList = None
        self.headers = None
        self.fids = None
        self.standardVisibleColumnIndices = [1,126,127,128,129,130,131,132]
#        self.standardVisibleColumnIndices = [1,2,12,60,70,119,120,126,127,128,129,130,131,132]
        horizHeader = self.horizontalHeader()
        horizHeader.setStretchLastSection(True)
        horizHeader.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        horizHeader.customContextMenuRequested.connect(self.horizHeaderMenu)
        horizHeader.setResizeMode(QtGui.QHeaderView.ResizeToContents)
        vertHeader = self.verticalHeader()
        vertHeader.setStretchLastSection(True)
        self.cellDoubleClicked.connect(self.sisPlot)
        
    def horizHeaderMenu(self, pos):
        columnIndex = self.horizontalHeader().logicalIndexAt(pos)
#        print('column(%d)' % columnIndex)
        self.clickedColumn = columnIndex
        menu = QtGui.QMenu()
        actionHideColumn = QtGui.QAction('Hide', self)
        actionHideColumn.triggered.connect(
                lambda x: self.hideColumn(columnIndex))
        menu.addAction(actionHideColumn)
        actionPop = QtGui.QAction('Set Visible Columns', self)
        actionPop.triggered.connect(self.popDialog)
        menu.addAction(actionPop)
        menu.exec_(QtGui.QCursor.pos())
    
    def sisPlot(self, row, col):
        name = self.item(row, 1).text()
        print(name)
        if name.endswith('.sis'):
            path = os.path.join(self.imagesPath, name)
            self.mainWindow.replot(path)
        
    def setColumnsVis(self):
        for j, value in enumerate(self.setVisibleList):
            self.setColumnHidden(j, not value)
    
    def popDialog(self):
        self.setVisibleDialog = SetVisibleColumnsDialog(self)
        self.setVisibleDialog.show()
        
    def displayCSV(self, fileName):           
#        fileName = QtGui.QFileDialog.getOpenFileName(self,'Open file', filter='CSV file (*.csv)', directory='/home/carmelo/master-thesis/data')
        root, self.CSVName = os.path.split(fileName)
        self.imagesPath = os.path.join(root, 'images')
#        self.tabWidget.setTabText(0, os.path.split(fileName)[1])
        with open(fileName, "r") as fileInput:
            rows = [row for row in csv.reader(fileInput)]
            self.headers = rows[0]
            table = rows[1:]
            self.fids = [r[0] for r in table] #lista con i FileId
            self.setRowCount(len(table))
            self.setColumnCount(len(self.headers))
            self.setHorizontalHeaderLabels(self.headers)
            self.setVerticalHeaderLabels(self.fids)
            for i, row in enumerate(table):
                for j, col in enumerate(row):
                    item = QtGui.QTableWidgetItem(col)
                    item.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.setItem(i, j, item)
        self.setVisibleList = [False for j in range(len(self.headers))]
        for j in self.standardVisibleColumnIndices:
            self.setVisibleList[j] = True
        self.setColumnsVis()

class SetVisibleColumnsDialog(QtGui.QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.parent = parent
        self.checkBoxList = []
        checkboxnames = parent.headers
        vislist = self.parent.setVisibleList
        for name, val in zip(checkboxnames, vislist):
            checkBox = QtGui.QCheckBox(self)
            checkBox.setObjectName('checkbox_'+name)
            checkBox.setText(name)
            checkBox.setChecked(val)
            self.verticalLayout.addWidget(checkBox)
            self.checkBoxList.append(checkBox)
        self.buttonBox.accepted.connect(self.updateVisibleColumns)
    
    def updateVisibleColumns(self):
        vislist = [box.isChecked() for box in self.checkBoxList]
        self.parent.setVisibleList = vislist
        self.parent.setColumnsVis()
        
        
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer/columns_dialog.ui'
#
# Created: Mon May 25 10:15:09 2015
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!


