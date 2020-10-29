from matplotlib.pyplot import figure, show
import numpy
figsrc = figure()

axsrc = figsrc.add_subplot(121, xlim=(0,1), ylim=(0,1), autoscale_on=False)
axzoom = figsrc.add_subplot(122, xlim=(0.45,0.55), ylim=(0.4,.6),
                                                autoscale_on=False)
axsrc.set_title('LMB to zoom in, RMB to zoom out')
axzoom.set_title('zoom window')
x,y,s,c = numpy.random.rand(4,200)
s *= 200

axsrc.scatter(x,y,s,c)
axzoom.scatter(x,y,s,c)

def onpress(event):
    if event.button==1: 
        zoomIn()
    elif event.button==3:
        zoomOut()

def zoomIn():
    aw, ah = figsrc.canvas.get_width_height()
    aw *= 1.2
    ah *= 1.2
    figsrc.canvas.resize(aw, ah)
    figsrc.canvas.draw()

def zoomOut():
    aw, ah = figsrc.canvas.get_width_height()
    if (aw !=0) and (ah != 0):
        aw /= 1.2
        ah /= 1.2
        figsrc.canvas.resize(aw, ah)
        figsrc.canvas.draw()


figsrc.canvas.mpl_connect('button_press_event', onpress)
show()