# -*- coding: utf-8 -*-

import numpy as np

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