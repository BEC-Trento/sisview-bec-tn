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
from __future__ import division
#from io import open

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
        with open(filename, 'rb') as f:  #apre in binario
            rawdata = np.fromfile(f, 'H').astype(int)
                
        width=rawdata[6]  # N cols
        height=rawdata[5] # N rows
        #rispetto ad octave, gli indici cambiano (python is 0-based)
        image = rawdata[-width*height : ]
        image.resize(height,width)
        im0 = image[:height//2, :]
        im1 = image[height//2:, :]
        
        return im0, im1, image, rawdata #, image.shape
