# -*- coding: utf-8 -*-

from PyQt4 import QtCore

class Signaler(QtCore.QObject):
    update = QtCore.pyqtSignal(tuple)
    pass

class ROI:
    def __init__(self, axes, x01=None, y01=None, picker_radius=5, **line_kwargs):
        self.lock = None  # only one can be animated at a time
        self.axes = axes
        self.figure = self.axes.figure
        self.canvas = self.figure.canvas
        self.autosetxy(x01, y01)
        
        defaults = dict(color='white', lw=1, picker=picker_radius)
        defaults.update(line_kwargs)
        self.lx0 = self.axes.axvline(self.x0, **defaults)
        self.lx1 = self.axes.axvline(self.x1, **defaults)
        self.ly0 = self.axes.axhline(self.y0, **defaults)
        self.ly1 = self.axes.axhline(self.y1, **defaults)

        self.press = None
        self.background = None
        self.cids = None
        self.signaler = Signaler()
        
        self.slice_rows = slice(None, None)
        self.slice_cols = slice(None, None)
        
        self.connect()
#        self.set_visible(True)
        
#    def set_visible(self, visible):
#        if visible:
#            self.rect.set_visible(bool(visible))
#            self.connect()
#        else:
#            self.disconnect()
#            self.rect.set_visible(bool(visible))
        
    def autosetxy(self, X, Y):
        if X is None:
            x0, x1 = self.axes.get_xlim()
            self.x0 = x0 + 0.2*(x1 - x0)
            self.x1 = x1 - 0.2*(x1 - x0)
        else:
            self.x0, self.x1 = X
        if Y is None:
            y0, y1 = self.axes.get_ylim()
            self.y0 = y0 + 0.2*(y1 - y0)
            self.y1 = y1 - 0.2*(y1 - y0)
        else:
            self.y0, self.y1 = Y

    def connect(self):
        self.cids = []
        self.cids.append(self.canvas.mpl_connect('pick_event', self.on_pick)) 
        self.cids.append(self.canvas.mpl_connect('button_press_event', self.on_press)) 
        self.cids.append(self.canvas.mpl_connect('motion_notify_event', self.on_motion))
        print('Actions connected')
        
    def on_press(self, event):
        print('mouse clicked')
        self.signaler.update.emit((self.slice_rows, self.slice_cols))
        pass

    def on_pick(self, event):
        print('pick')
        thisline = event.artist
        print('thisline: ', thisline)
        if self.lock is None:
            self.lock = thisline
            print('lock was None, now is ', thisline)
#            xdata, ydata = thisline.get_data()
#            self.press = xdata, ydata, event.xdata, event.ydata
            # draw everything but the selected rectangle and store the pixel buffer
            thisline.set_animated(True)
            self.canvas.draw()
            self.background = self.canvas.copy_from_bbox(self.axes.bbox)
            # now redraw just the rectangle
            self.axes.draw_artist(thisline)
            # and blit just the redrawn area
            self.canvas.blit(self.axes.bbox)
        elif self.lock == thisline:
            self.lock = None
            print('lock set back to none')
            # turn off the rect animation property and reset the background
            thisline.set_animated(False)
            self.background = None    
            # redraw the full figure
            self.canvas.draw()
            print('line {} moved to {}'.format(thisline, thisline.get_data()))
            self.update_values()
            print('new values: ', self.x0, self.x1, self.y1, self.y0)
            self.signaler.update.emit((self.slice_rows, self.slice_cols))
                

    def on_motion(self, event):
        if event.inaxes != self.axes: return
        if self.lock is None:
            return
        else:
            line = self.lock        
        self.position = event.xdata, event.ydata
        self.update_line(line)
        # restore the background region
        self.canvas.restore_region(self.background)
        # redraw just the current line
        self.axes.draw_artist(line)
        # blit just the redrawn area
        self.canvas.blit(self.axes.bbox)
        
    def update_line(self, line):
        xdata, ydata = line.get_data()
        xpress, ypress = self.position
        if ydata[0] == ydata[1]: #horizontal line
            line.set_ydata([ypress, ypress])
        elif xdata[0] == xdata[1]: #vertical line
            line.set_xdata([xpress, xpress])
            
    def update_values(self,):
        self.x0 = int(self.lx0.get_xdata()[0])
        self.x1 = int(self.lx1.get_xdata()[0])
        self.y0 = int(self.ly0.get_ydata()[0])
        self.y1 = int(self.ly1.get_ydata()[0])
        self.slice_cols = slice(min(self.x0, self.x1), max(self.x0, self.x1))
        self.slice_rows = slice(min(self.y0, self.y1), max(self.y0, self.y1))
        
        

    def disconnect(self):
        for cid in self.cids:
            self.canvas.mpl_disconnect(cid)
            
            
if __name__ == '__main__':
    import matplotlib.pyplot as plt
    
    fig, ax = plt.subplots() 
    roi = ROI(ax, color='black')

                
