#!/usr/bin/python2
# -*- coding: utf-8 -*-
#
# Copyright (C) 2016  Carmelo Mordini
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
import sys, os
from PyQt4 import QtGui, QtCore

import numpy as np
try:
    import pyfftw.interfaces.scipy_fftpack as fftpack
except ImportError:
    try:
        import scipy.fftpack as fftpack
    except ImportError:
        fftpack = np.fft
fft2, fftshift = fftpack.fft2, fftpack.fftshift
import matplotlib
from matplotlib.pyplot import colormaps
matplotlib.use(u'Qt4Agg')

from libraries.libsis import RawSis
from libraries.mainwindow_ui import Ui_MainWindow

PROG_NAME = u'SISView'
PROG_COMMENT = u'A tool for a quick visualization of .sis files'
PROG_VERSION = u'0.9.2'


#from PyQt4.QtGui import (QApplication, QColumnView, QFileSystemModel,
#                         QSplitter, QTreeView)
#from PyQt4.QtCore import QDir, Qt


class Main(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, ):
        super(Main, self).__init__()
        self.cwd = os.getcwdu()
        self.currentSis = None
        self.fft_flag = None
        self.currentFolder = None
        self.dockAreasDict = {'Top': QtCore.Qt.TopDockWidgetArea, 'Right': QtCore.Qt.RightDockWidgetArea}
        
        self.setupUi(self)
        self.tableWidget.setupUi(self)
        self.plotWidget0.setupUi(self)
        self.plotWidget1.setupUi(self)
        
        self.setWindowTitle(PROG_NAME+u' '+PROG_VERSION)
        self.setupToolbar()
        self.rewriteTreeView()
#        self.rewritePlotWidget()
        self.connectActions()
        
    def setupToolbar(self,):
        font = QtGui.QFont()
        font.setPointSize(10)
        self.toolBar.setFont(font)
        self.toolBar.setStyleSheet(u'QToolBar{spacing:6px;}')
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.actionBack = QtGui.QAction(self.toolBar)
        self.actionBack.setIcon(QtGui.QIcon(u":/icons/Back-icon.png"))
        self.actionBack.setObjectName(u"actionBack")
        self.actionBack.setIconText(u"Back")      
        self.toolBar.addAction(self.actionBack)
        self.toolBar.addSeparator()
        self.colormapLabel = QtGui.QLabel(self.toolBar)
        self.colormapLabel.setText(u'Colormap')
        self.colormapLabel.setFont(font)
        self.toolBar.addWidget(self.colormapLabel)
        self.colormapComboBox = QtGui.QComboBox(self.toolBar)
        self.colormapComboBox.setFont(font)
        self.colormapComboBox.addItems(colormaps())
        self.colormapComboBox.setCurrentIndex(106)
        self.toolBar.addWidget(self.colormapComboBox)
        self.toolBar.addSeparator()
        self.vminLabel = QtGui.QLabel(self.toolBar)
        self.vminLabel.setText(u'Vmin')
        self.vminLabel.setFont(font)
        self.toolBar.addWidget(self.vminLabel)
        self.vminDoubleSpinBox = QtGui.QDoubleSpinBox(self.toolBar)
        self.toolBar.addWidget(self.vminDoubleSpinBox)
        self.vmaxLabel = QtGui.QLabel(self.toolBar)
        self.vmaxLabel.setText(u'Vmax')
        self.vmaxLabel.setFont(font)
        self.toolBar.addWidget(self.vmaxLabel)
        self.vmaxDoubleSpinBox = QtGui.QDoubleSpinBox(self.toolBar)
        self.vmaxDoubleSpinBox.setValue(2.0)
        self.toolBar.addWidget(self.vmaxDoubleSpinBox)
        self.toolBar.addSeparator()
        self.fftLabel = QtGui.QLabel(self.toolBar)
        self.fftLabel.setText(u'FFT plot')
        self.fftLabel.setFont(font)
        self.toolBar.addWidget(self.fftLabel)
        self.fftComboBox = QtGui.QComboBox(self.toolBar)
        self.fftComboBox.setFont(font)
        self.fftComboBox.addItems([u'None', u'Im0', u'Im1'])
        self.fftComboBox.setCurrentIndex(0)
        self.toolBar.addWidget(self.fftComboBox)
        self.toolBar.addSeparator()

        
    def rewriteTreeView(self,):
        self.model = QtGui.QFileSystemModel()
        self.model.setRootPath(QtCore.QDir.rootPath())
        self.treeView.setModel(self.model)
        self.header = self.treeView.header()
        self.header.hideSection(1)
        self.header.setResizeMode(0, QtGui.QHeaderView.ResizeToContents)
        ROOT = sys.argv[1] if len(sys.argv) > 1 else os.getcwdu() #QtCore.QDir.homePath()
        self.currentFolder = str(ROOT)
        self.treeView.setRootIndex(self.model.index(ROOT))
        pass
        
    
    def connectActions(self):
        self.actionOpen_Folder.triggered.connect(self.openFolder)
        self.treeView.activated.connect(self.openSis)
        self.treeView.activated.connect(self.openCsv)
        self.treeView.doubleClicked.connect(self.goToFolder)
        self.colormapComboBox.currentIndexChanged.connect(lambda: self.replot(self.currentSis))
        self.fftComboBox.currentIndexChanged.connect(self.set_fft_flag)        
        self.vminDoubleSpinBox.valueChanged.connect(lambda: self.replot(self.currentSis))
        self.vmaxDoubleSpinBox.valueChanged.connect(lambda: self.replot(self.currentSis))
        self.actionTop.triggered.connect(lambda: self.dock_to_area(self.actionTop.text()))
        self.actionRight.triggered.connect(lambda: self.dock_to_area(self.actionRight.text()))
        self.actionDetatch_All.triggered.connect(self.dock_detatch_all)
        self.actionToggle0 = self.dockWidget0.toggleViewAction()
        self.actionToggle1 = self.dockWidget1.toggleViewAction()
        self.menuView.addAction(self.actionToggle0)
        self.menuView.addAction(self.actionToggle1)
        self.actionInfo.triggered.connect(self.infoBox)
        self.actionQuit.triggered.connect(QtGui.qApp.quit)
        self.actionBack.triggered.connect(self.goBackFolder)
        pass
    
    def dock_to_area(self, pos):
        # positions seem to be: left = 1, right = 2, top = ?
        for dock in [self.dockWidget0, self.dockWidget1]:
            dock.setFloating(False)
            self.addDockWidget(self.dockAreasDict[str(pos)], dock)
        self.showMaximized()
            
    def dock_detatch_all(self):
        for dock in [self.dockWidget0, self.dockWidget1]:
            dock.setFloating(True)
        self.showNormal()
    
    def openFolder(self,):
        folder = QtGui.QFileDialog.getExistingDirectory(self, caption=u'Open folder',
                                                        directory=QtCore.QDir.homePath())
        self.currentFolder = str(folder)
        self.treeView.setRootIndex(self.model.index(folder))
    
    def goToFolder(self, index):
        path = str(self.model.filePath(index))
        if os.path.isdir(path):
            self.currentFolder = path
            self.treeView.setRootIndex(self.model.index(path))
            
    def goBackFolder(self):
        parent = os.path.abspath(os.path.join(self.currentFolder, os.pardir))
        print parent
        self.currentFolder = parent
        self.treeView.setRootIndex(self.model.index(parent))
        pass
            
    def openCsv(self, index):
        path = str(self.model.filePath(index))
        name = os.path.split(path)[1]
        if os.path.isfile(path) and path.endswith(u'.csv'):
            print path
            self.csvLabel.setText(u'Display CSV: ' + name)
            self.tableWidget.displayCSV(path)

    def openSis(self, index):
        path = str(self.model.filePath(index))
        if os.path.isfile(path) and path.endswith(u'.sis'):
            self.currentSis = path
            print u'Directly opened ', self.currentSis
            self.replot(path)
            
    def set_fft_flag(self,):
        self.fft_flag = self.fftComboBox.currentText()
        self.replot(self.currentSis)
        
    def replot(self, path):
    #TODO: ASSOLUTAMENTE da implementare in modo che NON debba ricalcolare
    # la FFT ogni volta che plotta, come invece sta facendo ora!
        if path is not None:
            dic_img = {'cmap': str(self.colormapComboBox.currentText()),
                       'vmin': self.vminDoubleSpinBox.value(),
                       'vmax': self.vmaxDoubleSpinBox.value(),}
            dic_fft = {'cmap': 'jet',
                       'vmin': 0,
                       'vmax': 3,}
#            print(self.colormapComboBox.currentText())
            sis = RawSis(path)
            name = os.path.split(path)[1]
            if self.fft_flag == u'Im0':
                images = [sis.im0, fftshift(np.log10(np.abs(fft2(sis.im0))))]
                dicts = [dic_img, dic_fft]
            elif self.fft_flag == u'Im1':
                images = [fftshift(np.log10(np.abs(fft2(sis.im1)))), sis.im1]
                dicts = [dic_fft, dic_img]
            else:
                images = [sis.im0, sis.im1]
                dicts = [dic_img, dic_img]
            for j, plotw in enumerate([self.plotWidget0, self.plotWidget1]):
                plotw.replot(images[j], dicts[j], name)
        else:
            print u'path is None'
            
            
    def infoBox(self,):
        QtGui.QMessageBox.about(self, PROG_NAME, PROG_COMMENT+u'\n v. '+PROG_VERSION)
        
if __name__ == u'__main__':
    app = QtGui.QApplication(sys.argv)
    main = Main()
#    main.show()
    main.showMaximized()
    status = app.exec_()

    sys.exit(status)
