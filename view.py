"""An example of how to use models and views in PyQt4.
Model/view documentation can be found at
http://doc.qt.nokia.com/latest/model-view-programming.html.
"""
import sys, os

from PyQt4 import QtGui, QtCore
from libraries.mainwindow_ui import Ui_MainWindow

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Qt4Agg')
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)

PROG_NAME = 'SISView'
PROG_VERSION = '0.9'


#from PyQt4.QtGui import (QApplication, QColumnView, QFileSystemModel,
#                         QSplitter, QTreeView)
#from PyQt4.QtCore import QDir, Qt

class RawSis():
    
    def __init__(self, filename, scale=None):
        
        im0, im1, im, raw = self.readsis(filename)
        if scale is not None:
            self.scale = scale
        else:
            self.scale = 2**16/10.0#1.0
        
        self.im0 = im0/self.scale
        self.im1 = im1/self.scale
        self.im_full  = im/self.scale
        self.raw = raw/self.scale
        
    
    def readsis(self,filename):
        f = open(filename, 'rb')  #apre in binario
        rawdata = np.fromfile(f,'H').astype(int)
        f.close()
        
        width=rawdata[6]  # N cols
        height=rawdata[5] # N rows
        #rispetto ad octave, gli indici cambiano (python is 0-based)
        image = rawdata[-width*height : ]
        image.resize(height,width)
        im0 = image[:height//2, :]
        im1 = image[height//2:, :]
        
        return im0, im1, image, rawdata #, image.shape

class Main(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, ):
        super(Main, self).__init__()
        self.cwd = os.getcwd()
        self.currentSis = None
        
        self.setupUi(self)
        self.setWindowTitle(PROG_NAME+' '+PROG_VERSION)
        self.setupToolbar()
        self.rewriteTreeView()
        self.rewritePlotWidget()
        self.connectActions()
        
    def setupToolbar(self,):
        font = QtGui.QFont()
        font.setPointSize(10)
        self.toolBar.setFont(font)
        self.toolBar.setStyleSheet('QToolBar{spacing:6px;}')
        self.colormapLabel = QtGui.QLabel(self.toolBar)
        self.colormapLabel.setText('Colormap')
        self.colormapLabel.setFont(font)
        self.toolBar.addWidget(self.colormapLabel)
        self.colormapComboBox = QtGui.QComboBox(self.toolBar)
        self.colormapComboBox.setFont(font)
        self.colormapComboBox.addItems(plt.colormaps())
        self.toolBar.addWidget(self.colormapComboBox)
        self.toolBar.addSeparator()
        self.vminLabel = QtGui.QLabel(self.toolBar)
        self.vminLabel.setText('Vmin')
        self.vminLabel.setFont(font)
        self.toolBar.addWidget(self.vminLabel)
        self.vminDoubleSpinBox = QtGui.QDoubleSpinBox(self.toolBar)
        self.toolBar.addWidget(self.vminDoubleSpinBox)
        self.vmaxLabel = QtGui.QLabel(self.toolBar)
        self.vmaxLabel.setText('Vmax')
        self.vmaxLabel.setFont(font)
        self.toolBar.addWidget(self.vmaxLabel)
        self.vmaxDoubleSpinBox = QtGui.QDoubleSpinBox(self.toolBar)
        self.vmaxDoubleSpinBox.setValue(2.0)
        self.toolBar.addWidget(self.vmaxDoubleSpinBox)
        self.toolBar.addSeparator()

        
    def rewriteTreeView(self,):
        self.model = QtGui.QFileSystemModel()
        self.model.setRootPath(QtCore.QDir.rootPath())
        self.treeView.setModel(self.model)
        self.treeView.setRootIndex(self.model.index(QtCore.QDir.homePath()))
        pass
    
    def rewritePlotWidget(self,):
        self.figure0, self.ax0 = plt.subplots(1,1,)#figsize=(6,6))
        self.ax0.plot(np.random.rand(10))
        self.figure0.set_facecolor('none')
        self.canvas0 = FigureCanvas(self.figure0)
        self.toolbar0 = NavigationToolbar(self.canvas0, self, coordinates=False)
        self.toolbar0.setOrientation(QtCore.Qt.Horizontal)
        self.plotLayout0.addWidget(self.canvas0)
        self.plotLayout0.addWidget(self.toolbar0)
        self.canvas0.draw()
        
        self.figure1, self.ax1 = plt.subplots(1,1,)#figsize=(6,6))
        self.ax1.plot(np.random.rand(11))
        self.figure1.set_facecolor('none')
        self.canvas1 = FigureCanvas(self.figure1)
        self.toolbar1 = NavigationToolbar(self.canvas1, self, coordinates=False)
        self.toolbar1.setOrientation(QtCore.Qt.Horizontal)
        self.plotLayout1.addWidget(self.canvas1)
        self.plotLayout1.addWidget(self.toolbar1)
        self.canvas1.draw()
        
    
    def connectActions(self):
        self.actionOpen_Folder.triggered.connect(self.openFolder)
        self.treeView.doubleClicked.connect(self.openSis)
        self.colormapComboBox.currentIndexChanged.connect(lambda: self.replot(self.currentSis))
        self.vminDoubleSpinBox.valueChanged.connect(lambda: self.replot(self.currentSis))
        self.vmaxDoubleSpinBox.valueChanged.connect(lambda: self.replot(self.currentSis))
        self.actionToggle0 = self.dockWidget0.toggleViewAction()
        self.actionToggle1 = self.dockWidget1.toggleViewAction()
        self.menuView.addAction(self.actionToggle0)
        self.menuView.addAction(self.actionToggle1)
        pass
    
    def openFolder(self,):
        folder = QtGui.QFileDialog.getExistingDirectory(self, caption='Open folder',
                                                        directory=QtCore.QDir.homePath())
        self.treeView.setRootIndex(self.model.index(folder))
                
    def openSis(self, index):
        path = self.model.filePath(index)
        if os.path.isfile(path) and path.endswith('.sis'):
            self.currentSis = path
            self.replot(path)
            
    def replot(self, path):
        if path is not None:
            dic = {'cmap': self.colormapComboBox.currentText(),
                   'vmin': self.vminDoubleSpinBox.value(),
                   'vmax': self.vmaxDoubleSpinBox.value(),}
            sis = RawSis(path)
            self.ax0.cla()
            self.ax1.cla()
            self.ax0.imshow(sis.im0, **dic)
            self.ax1.imshow(sis.im1, **dic)
            self.canvas0.draw()
            self.canvas1.draw()
        else:
            print('path is None')
        
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    main = Main()
    main.show()
    status = app.exec_()

    sys.exit(status)