# -*- coding: utf-8 -*-
"""
Development of interactive version started on Tue Jan 11 21:01:00 2022
@author: mahesh.ramakrishnan@hotmail.com

Goal: Simulates the powder diffraction rings (customised to EIGER 1M detector). 
    Interactive viewing of the detector image for various positions. 
    Cannot handle detector rotations for the time being. 
    Upgradable to any detector dimensions. The intermodule gap however remains 
    that of EIGER 1M.

Relation to PONI:
    x = PONI1
    y = PONI2 - detectorHeight

Hexagonal lattice : gamma = 120
Monoclinic lattice : unique axis 'b', beta != 90 deg

Version history: 
    + v0.X.X: Rudimentary trial versions
    + v1.0 :(20220330) Can simulate the detector image for orthorhombic systems. User 
           needs to input the lattice a,b,c, energy and detector x, y, D (interactive)
    + v1.1 :(20220401) Added hkl index for each ring in the image. 
    + v1.2 : Corrected for tth range (0,90) in forward scattering geometry. Implemented 
            updation based on changing a,b,c and Energy.         
    + v1.3 : d_hkl for hexagonal and monoclinic lattices included. Updation of 
            lattice related functions only on clicking calculate button. Reflection
            condition functions (in library) linked. Addition of new space groups 
            only needs the corresponding dict entry and hkl check function.
    + v1.4: Simple bug fixes.
    + v1.5: Includes check for lattice parameters input by user, with a cross-check
            to the given space group. Calculated hkl, tth are displayed in a console widget.
    + v1.6: Uses the spread function of the lines due to geometry.  
    + v1.7: Introduced mouse movement tracking, display absolute q, 
            trying to extract hkl based on position.
    + v1.8: Displays PONI parameters based on detector dimensions and x,y,D. Triclinic 
            systems included.
    + v1.9: Nothing special. Few more space groups and library version 3.        
                   
"""

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.console
import numpy as np
import mpxrd_libraries_v4 as mpxrd_lib
import math

app = QtGui.QApplication([])

# Set up UI widgets
win = pg.QtGui.QWidget()
win.setWindowTitle('Powder XRD Simulation')
layout = pg.QtGui.QGridLayout()
win.setLayout(layout)
layout.setContentsMargins(0, 0, 0, 0)

# Setting detector distances

xLabel = pg.QtGui.QLabel('Detector X (mm):')
layout.addWidget(xLabel, 0, 0)
xSpin = pg.SpinBox(value=15, step=1, bounds=[0, 500], delay=0, int=True)
#xSpin.resize(40, 20)
layout.addWidget(xSpin, 0, 1)

yLabel = pg.QtGui.QLabel('Detector Y (mm):')
layout.addWidget(yLabel, 1, 0)
ySpin = pg.SpinBox(value=55, step=1, bounds=[0, 500], delay=0, int=True)
#ySpin.resize(40, 20)
layout.addWidget(ySpin, 1, 1)

dLabel = pg.QtGui.QLabel('Detector Normal Distance (mm):')
layout.addWidget(dLabel, 2, 0)
dSpin = pg.SpinBox(value=150, step=1, bounds=[0, 1000], delay=0, int=True)
#dSpin.resize(40, 20)
layout.addWidget(dSpin, 2, 1)


# Setting energy

eLabel = pg.QtGui.QLabel('Energy (eV):')
layout.addWidget(eLabel, 3, 0)
eSpin = pg.SpinBox(value=12000.0, step=100, bounds=[2000, 50000], delay=0, int=False)
#eSpin.resize(40, 20)
layout.addWidget(eSpin, 3, 1)

# Setting up detector dimensions and PONI
detWLabel = pg.QtGui.QLabel('Detector Width (mm):')
layout.addWidget(detWLabel,4,0)
detWLine = pg.Qt.QtGui.QLineEdit('79.9')
layout.addWidget(detWLine,4,1)

detHLabel = pg.QtGui.QLabel('Detector Height (mm):')
layout.addWidget(detHLabel,5,0)
detHLine = pg.Qt.QtGui.QLineEdit('77.2')
layout.addWidget(detHLine,5,1)

# Ring labels ON/OFF Checkbox
labelCheckBox = QtGui.QCheckBox('Show ring labels')
layout.addWidget(labelCheckBox,6,0)

poni = pg.QtGui.QLabel('PONI1 = %0.2f; PONI2 = %0.2f' %(xSpin.value(),ySpin.value()+float(detHLine.text())))
poniFont = poni.font()
poniFont.setBold(True)
poniFont.setPointSize(11)
poni.setFont(poniFont)
layout.addWidget(poni, 6, 1)

# Setting crystal lattice

aLabel = pg.QtGui.QLabel('Crystal a (Å):')
layout.addWidget(aLabel, 0, 2)
aSpin = pg.SpinBox(value=4.15, step=0.1, bounds=[2, 50], delay=0, int=False)
aSpin.resize(40, 20)
layout.addWidget(aSpin, 0, 3)

bLabel = pg.QtGui.QLabel('Crystal b (Å):')
layout.addWidget(bLabel, 1, 2)
bSpin = pg.SpinBox(value=4.15, step=0.1, bounds=[2, 50], delay=0, int=False)
bSpin.resize(40, 20)
layout.addWidget(bSpin, 1, 3)

cLabel = pg.QtGui.QLabel('Crystal c (Å):')
layout.addWidget(cLabel, 2, 2)
cSpin = pg.SpinBox(value=4.15, step=0.1, bounds=[2, 50], delay=0, int=False)
cSpin.resize(40, 20)
layout.addWidget(cSpin, 2, 3)

alpLabel = pg.QtGui.QLabel('alpha (deg):')
layout.addWidget(alpLabel, 3, 2)
alpSpin = pg.SpinBox(value=90, step=1, bounds=[60, 150], delay=0, int=False)
alpSpin.resize(40, 20)
layout.addWidget(alpSpin, 3, 3)

betLabel = pg.QtGui.QLabel('beta (deg):')
layout.addWidget(betLabel, 4, 2)
betSpin = pg.SpinBox(value=90, step=1, bounds=[60, 150], delay=0, int=False)
betSpin.resize(40, 20)
layout.addWidget(betSpin, 4, 3)

gamLabel = pg.QtGui.QLabel('gamma (deg):')
layout.addWidget(gamLabel, 5, 2)
gamSpin = pg.SpinBox(value=90, step=1, bounds=[60, 150], delay=0, int=False)
gamSpin.resize(40, 20)
layout.addWidget(gamSpin, 5, 3)


# Defining the space group drop down list and calculate button

sgLabel = pg.QtGui.QLabel('Space group')
layout.addWidget(sgLabel, 6, 2)
sgBox = pg.ComboBox()
sgBox.setItems(mpxrd_lib.spaceGroups)
sgBox.setValue(221)
sgBox.resize(40, 20)
layout.addWidget(sgBox, 6, 3)
N_sg = len(mpxrd_lib.spaceGroups)

cButton = QtGui.QPushButton('Calculate')
cButton.resize(80,20)
layout.addWidget(cButton,9,2)

message = pg.QtGui.QLabel('Powder ring simulation')
messageFont = message.font()
messageFont.setBold(True)
messageFont.setPointSize(12)
message.setFont(messageFont)
layout.addWidget(message, 11, 2, 1, 2)


# Setting the console widget
consInitText = 'Starting powder diffraction simulation. Found '+str(N_sg)+' space groups in library.\n'
cons = pyqtgraph.console.ConsoleWidget(text=consInitText)
layout.addWidget(cons, 17, 0, 3, 4)


# Setting the plot widget

w = pg.GraphicsLayoutWidget()
layout.addWidget(w, 7, 0, 10, 2)
w.resize(1000, 1500)
w.ci.setBorder((50, 50, 100))
w.setBackground((255,250,250))

p1 = w.addPlot(title="Detector Image")
p1.setAspectLocked(1.0)

myPen = pg.mkPen(color = (5,20,220), width=2)
myPen.setWidth(1.5)

vb = p1.vb
infoLabel = pg.QtGui.QLabel('Mouse pointer info:')
layout.addWidget(infoLabel, 12, 2, 1, 2)

#legend = p1.addLegend(offset=(300, 30))
#leg1 = legend.setParentItem(p1)
#legend.show()

theta = np.linspace(0,2*np.pi,num=100)
xx = np.linspace(0,1,num=100)
yy = np.linspace(0,1,num=100)

p1.setYRange(78.8+ySpin.value(),ySpin.value())
p1.setXRange(-38.9-xSpin.value(),38.9-xSpin.value())
mpxrd_lib.drawBox(p1,-38.9-xSpin.value(),38.9-xSpin.value(),78.8+ySpin.value(),ySpin.value())
darray = []
harray = []
karray = []
larray = []

def recalculate():
    darray.clear()
    harray.clear()
    karray.clear()
    larray.clear()
    a = aSpin.value()
    b = bSpin.value()
    c = cSpin.value()
    alp = alpSpin.value()
    bet = betSpin.value()
    gam = gamSpin.value()
    al = alp*np.pi/180
    be = bet*np.pi/180
    ga = gam*np.pi/180
    
    if input_check(a, b, c, alp, bet, gam) == 0:
        return 0
    cons.write('\n Recalculating diffraction rings for new lattice..\n')
    for h in range(0,9):
        for k in range(0,9):
            for l in range(0,9):
                if h+k+l>0:
                    hkl_func = 'mpxrd_lib.reflCond_'+str(sgBox.value())
                    if eval(hkl_func)(h,k,l):
                        if alp == 90 and bet == 90 and gam == 90:
                            d_hkl = 1/np.sqrt(np.square(h/a)+np.square(k/b)+np.square(l/c))
                        elif alp == bet == 90 and gam == 120:
                            d_hkl = 1/np.sqrt((1.3333/np.square(a))*(np.square(h)+np.square(k)+h*k)+np.square(l/c))
                        elif alp == gam == 90 and bet != 90:
                            d_hkl = 1/np.sqrt(np.square(1/np.sin(be))*(np.square(h/a)+np.square(l/c)-2*h*l*np.cos(be)/(a*c))+np.square(k/b))
                        elif bet != 90 and alp != 90 and gam !=90:
                            V = a*b*c*np.sqrt(1-np.square(np.cos(al))-np.square(np.cos(be))-np.square(np.cos(ga))+2*np.cos(al)*np.cos(be)*np.cos(ga))
                            S11 = np.square(b*c*np.sin(al))
                            S22 = np.square(a*c*np.sin(be))
                            S33 = np.square(a*b*np.sin(ga))
                            S12 = a*b*np.square(c)*(np.cos(al)*np.cos(be)-np.cos(ga))
                            S23 = b*c*np.square(a)*(np.cos(be)*np.cos(ga)-np.cos(al))
                            S13 = c*a*np.square(b)*(np.cos(ga)*np.cos(al)-np.cos(be))
                            d_hkl = V/np.sqrt(S11*h*h+S22*k*k+S33*l*l+2*S12*h*k+2*S23*k*l+2*S13*h*l)
                        darray.append(d_hkl)
                        harray.append(h)
                        karray.append(k)
                        larray.append(l)
    update()
              
def mouseMoved(evt):
    pos = evt[0]  ## using signal proxy turns original arguments into a tuple
    if p1.sceneBoundingRect().contains(pos):
        mousePoint = vb.mapSceneToView(pos)
        mx = mousePoint.x()
        my = mousePoint.y()
        r_calc = np.sqrt(mx*mx+my*my)
        tan_tth = np.divide(r_calc,dSpin.value())
        th = np.arctan(tan_tth)/2
        tth_deg = 2*th*180/np.pi
        #tth = 2*np.arcsin(wavelength/(2*darray[i]))
        #d=lambda/2sin(th)
        wavelength = 12398/eSpin.value()
        d_calc = np.divide(wavelength,2*np.sin(th))
        q_calc = np.divide(4*np.pi*np.sin(th),wavelength)
        infoLabel.setText("x=%0.2f, y=%0.2f, \n tth=%0.2f,  q= %0.3f Å-1" % (mx, my,tth_deg,q_calc))
        for i in range(0,len(darray)):
            if math.isclose(d_calc, darray[i], rel_tol = 0.005):
                infoLabel.setText("x=%0.1f,y=%0.1f,\n tth=%0.2f, q= %0.3f Å-1\nhkl = %0.0f %0.0f %0.0f" % (mx, my, tth_deg, q_calc, harray[i], karray[i], larray[i]))
    
def update():
    cons.write('\n Updating plot with new geometry..\n\n')
    wavelength = 12398/eSpin.value()
    d_prev=0
    toggle_pos = 0
    p1.clear()
    p1.setYRange(float(detHLine.text())+ySpin.value(),ySpin.value())
    p1.setXRange(-float(detWLine.text())/2-xSpin.value(),float(detHLine.text())/2-xSpin.value())
    mpxrd_lib.drawBox(p1,-float(detWLine.text())/2-xSpin.value(),float(detHLine.text())/2-xSpin.value(),float(detHLine.text())+ySpin.value(),ySpin.value())
    cons.write('Plotting rings with [hkl,tth]:\n')
    for i in range(0,len(darray)):
        if wavelength/(2*darray[i]) >= 1:
            continue
        tth = 2*np.arcsin(wavelength/(2*darray[i]))
        if tth > 1.57:
            continue
        tan_tth = np.tan(tth)
        d = np.absolute(dSpin.value()*tan_tth)
        xx = np.multiply(d,np.cos(theta))
        yy = np.multiply(d,np.sin(theta))
        if darray[i] != d_prev:
            p1.plot(yy,xx, pen = myPen, name=str(tth))
            hklString = str(harray[i])+str(karray[i])+str(larray[i])
            tthString = str(round(tth*180/3.1416,2))
            statusString = '[' + hklString + ', ' + tthString + ']; \t'
            cons.write(statusString)
            if labelCheckBox.checkState():
                t1 = pg.TextItem(str(harray[i])+str(karray[i])+str(larray[i]),color='k',border=1,fill=(250,250,250))
                p1.addItem(t1)
                if toggle_pos == 0:
                    t1.setPos(xx[60],yy[60])
                    toggle_pos += 1
                elif toggle_pos == 1:
                    t1.setPos(xx[65],yy[65])
                    toggle_pos += 1
                else:
                    t1.setPos(xx[70],yy[70])
                    toggle_pos = 0
                
        d_prev = darray[i]    
    mpxrd_lib.showOrigin(p1,-xSpin.value(),ySpin.value())                
    poni.setText('PONI1 = %0.2f; PONI2 = %0.2f' %(xSpin.value(),ySpin.value()+float(detHLine.text())))
    win.show()

def input_check(a,b,c,alp,bet,gam):
    messageText = 'Input error. Check lattice parameters!\n Monoclinic: beta!=90\n Hexagonal gamma=120'
    spgr = sgBox.value()
    checkValue = True
    if a==b==c and alp==bet==gam==90 and 195<=spgr<=230:
        messageText = 'Calculating rings for cubic lattice'
    elif a==b and alp==bet==gam==90 and 75<=spgr<=142:
        messageText = 'Calculating rings for tetragonal lattice'
    elif c==b and alp==bet==gam==90 and 75<=spgr<=142:
        messageText = 'Calculating rings for tetragonal lattice'
    elif a==c and alp==bet==gam==90 and 75<=spgr<=142:
        messageText = 'Calculating rings for tetragonal lattice'
    elif alp==bet==gam==90 and 16<=spgr<=74:
        messageText = 'Calculating rings for orthorhombic lattice'
    elif a==b and alp==bet==90 and gam==120 and 143<=spgr<=194:
        messageText = 'Calculating rings for hexagonal lattice'
    elif alp==gam==90 and bet!=90 and 3<=spgr<=15:
        messageText = 'Calculating rings for monoclinic lattice'
    elif alp!=90 and bet!=90 and gam!=90 and spgr<=2:
        messageText = 'Calculating rings for Triclinic lattice'
    else:
        checkValue = False
    
    message.setText(messageText)
    
    return checkValue

# Set up graphics
#v = w.addViewBox()
#v.setAspectLocked()

#baseLine = pg.PolyLineROI([[0, 0], [1, 0], [1.5, 1], [2, 0], [3, 0]], pen=(0, 255, 0, 100), movable=False)
#v.addItem(baseLine)
#fc = pg.PlotCurveItem(pen=(255, 255, 255, 200), antialias=True)
#v.addItem(fc)
#v.autoRange()

recalculate()
cButton.clicked.connect(recalculate)

xSpin.valueChanged.connect(update)
ySpin.valueChanged.connect(update)
dSpin.valueChanged.connect(update)
eSpin.valueChanged.connect(update)
detHLine.textChanged.connect(update)
detWLine.textChanged.connect(update)
labelCheckBox.stateChanged.connect(update)
proxy = pg.SignalProxy(p1.scene().sigMouseMoved, rateLimit=60, slot=mouseMoved)


## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()