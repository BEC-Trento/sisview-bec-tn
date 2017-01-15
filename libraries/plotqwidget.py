"""
Copyright (C) 2017 Carmelo Mordini

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
# -*- coding: utf-8 -*-
"""
Created on Sun May 24 01:46:57 2015

@author: carmelo
"""
from PyQt4 import QtCore, QtGui

import numpy as np
import matplotlib.pyplot as plt


from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)


class PlotQWidget(QtGui.QWidget):
    
    def __init__(self, *args, **kwargs):
        super(PlotQWidget, self).__init__(*args, **kwargs)
        
    def setupUi(self, setMainWindow):
        self.mainWindow = setMainWindow
        self.image = None
        self.lims = None
        self.roi = None
        
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
#        self.gridspec = gs.GridSpec(2, 2, width_ratios=[1,4], height_ratios=[4,1])
#        self.ax = self.figure.add_subplot(self.gridspec[1])
        self.ax = self.figure.add_subplot(111)
        self.ax.axis('off')
        self.im = self.ax.imshow(np.random.rand(10,10), cmap='gray')
#        self.ax_y = self.figure.add_subplot(self.gridspec[0], sharey=self.ax)
#        self.ax_x = self.figure.add_subplot(self.gridspec[3], sharex=self.ax)        
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
        self.roi = None
        self.image = image
        if 1:#self.isVisible():
            if self.lims is None:
                print('lims is None')
                self._plotdata(dic)
                self.lims = (self.ax.get_xlim(), self.ax.get_ylim())
#                print(self.lims)
            else:
                print(self.lims)
                self.lims = (self.ax.get_xlim(), self.ax.get_ylim())
#                print('newlims: ', self.lims)
#                print(self.ax.get_xlim())
#                self.ax.set_xlim(0, image.shape[1])
#                self.ax.set_ylim(image.shape[0], 0)
                self._plotdata(dic)
                self.ax.set_xlim(*self.lims[0])
                self.ax.set_ylim(*self.lims[1])
        self.canvas.draw()

    def _plotdata(self, dic={}):
        image = self.image
#        self.im.set_data(image)        
#        self.im.norm.vmin = dic['vmin']
#        self.im.norm.vmax = dic['vmax']
#        self.im.set_cmap(dic['cmap'])
        self.ax.cla()
        self.ax.axis('off')
        self.ax.imshow(image, **dic)

        
    

               
        
