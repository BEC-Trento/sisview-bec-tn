# -*- coding: utf-8 -*-
"""
Created on Sun May 24 01:46:57 2015

@author: carmelo
"""
import PySide
from PySide import QtCore, QtGui

import numpy as np
from matplotlib.cm import get_cmap

import pyqtgraph as pg

pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')

class MyImageView(pg.ImageView):
    def __init__(self, *args, **kwargs):
        super(MyImageView, self).__init__(*args, **kwargs)
        self.ui.menuBtn.setFixedWidth(50)
        self.ui.roiBtn.setFixedWidth(50)
        
        self.roi.setSize(300)
        pass


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
        self.imView = MyImageView(view=pg.PlotItem())
        self.histogram = self.imView.getHistogramWidget()

        self.plotLayout.addWidget(self.imView)
        self.setLayout(self.plotLayout)
        self.setParams()
        
    def setParams(self,):
        pass
        
    def replot_here(self, image, name=None,):
        if name is not None:
            self.nameLabel.setText(name)
        if self.isVisible():
            self.imView.setImage(image.T)
#        cmap_name = dic['cmap']
#        levels = (dic['vmin'], dic['vmax'])
#        self.setLevels(levels)
#        self.setCmap(cmap_name)
            
    def setLevels(self, levels):
        if self.isVisible():
            self.imView.setLevels(*levels)
    
    def setCmap(self, cmap_name):
#        if self.isVisible():
            print('setting cmap')
            cmap = get_cmap(cmap_name)
            cmap_array = np.array([cmap(j) for j in range(cmap.N)])
            cmap_pg = pg.ColorMap(np.arange(cmap.N)/cmap.N, cmap_array)
            self.histogram.gradient.setColorMap(cmap_pg)

               
         
               
if __name__ == '__main__':
    import sys, os
    from readsis import RawSis
    
    
    app = QtGui.QApplication(sys.argv)
    
    file = '../data/2015-03-04/images/20150304-data-0010.sis'
    image = RawSis(file).im0
    cmap_name = 'gist_stern'
    levels = (0,2)
    
    win = QtGui.QMainWindow()
    plotw = PlotQWidget()
    plotw.setupUi(win)
    plotw.setVisible(True)
    
    print(plotw.histogram.width())
    plotw.replot_here(image, os.path.split(file)[1])
    plotw.setCmap(cmap_name)
    plotw.setLevels(levels)
    
    win.setCentralWidget(plotw)
    win.setWindowTitle('pyqtgraph example: ImageViewColor')
    win.showMaximized()  #raisethe IndexError
    
    status = app.exec_()

    sys.exit(status)

