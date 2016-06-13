# -*- coding: utf-8 -*-
"""
Created on Sun May 24 01:46:57 2015

@author: carmelo
"""
from PyQt4 import QtCore, QtGui

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gs
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)



class PlotQWidget(QtGui.QWidget):
    
    def __init__(self, *args, **kwargs):
        super(PlotQWidget, self).__init__(*args, **kwargs)
        
    def setupUi(self, setMainWindow):
        self.mainWindow = setMainWindow
        self.lims = None
        
        self.plotLayout = QtGui.QVBoxLayout(self)
        
        self.nameLabel = QtGui.QLabel(self)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nameLabel.sizePolicy().hasHeightForWidth())
        self.nameLabel.setSizePolicy(sizePolicy)
#        self.nameLabel.setText('ciao')
        self.plotLayout.addWidget(self.nameLabel)
        
#        self.figure, self.ax = plt.subplots(1,1, figsize=(18,6))
        self.figure = plt.figure(figsize=(18,6))
        self.gridspec = gs.GridSpec(2, 2, width_ratios=[1,2], height_ratios=[4,1])
        self.ax = self.figure.add_subplot(self.gridspec[1])
        
        self.ax_y = self.figure.add_subplot(self.gridspec[0], sharey=self.ax)
        self.ax_x = self.figure.add_subplot(self.gridspec[3], sharex=self.ax)
        
        self.figure.set_facecolor('none')
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self, coordinates=False)
        self.toolbar.setOrientation(QtCore.Qt.Horizontal)
        self.plotLayout.addWidget(self.canvas)
        self.plotLayout.addWidget(self.toolbar)
        
        self.setLayout(self.plotLayout)
        self.canvas.draw()
        
    def replot(self, image, dic={}, name=None):
        if name is not None:
            self.nameLabel.setText(name)
        if self.isVisible():
            if self.lims is None:
#                print('lims is None')
                self.ax.cla()              
#                self.ax.axis('off')
                self.im = self.ax.imshow(image, **dic)
                self.lims = (self.ax.get_xlim(), self.ax.get_ylim())
#                print(self.lims)
            else:
                self.lims = (self.ax.get_xlim(), self.ax.get_ylim())
#                print(self.lims)
#                self.ax.cla()              
#                self.ax.axis('off')
                self.im.set_data(image)
                self.im.set_cmap(dic['cmap'])
                self.im.norm.vmin = dic['vmin']
                self.im.norm.vmax = dic['vmax']
                self.ax.set_xlim(*self.lims[0])
                self.ax.set_ylim(*self.lims[1])
            int_x = image.sum(0)
            int_y = image.sum(1)
            self.ax_x.cla()
            self.ax_y.cla()
            self.ax_x.plot(np.arange(len(int_x)), int_x)
            self.ax_y.plot(int_y, np.arange(len(int_y)))
            self.canvas.draw()

               
        
