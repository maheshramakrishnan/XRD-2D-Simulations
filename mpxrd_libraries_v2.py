# -*- coding: utf-8 -*-
"""
Created on Sat Apr  2 11:44:04 2022

MPXRD Libraries: Contains additional structures and functions used in the 
    calculation of powder diffraction patterns.

Available functions:
    1) showOrigin(plotHandle,int,int): Draws a '+' symbol at the point specified
      by (x,y) in the plot with handle p1.
    2) drawBox(plotHandle,int,int,int,int): Draws a rectangular box between 
      coordinates (x1,y1) and (x2,y2) in the plot with handle p1.
      
Dictionaries:
    1) refl_dict: Contains list of allowed refections for every space group.
             

@author: mahram
"""
import numpy as np
import pyqtgraph as pg

def showOrigin(p1,x,y):
    xrange = np.linspace(x-2,x+2,10)
    yrange = np.linspace(y-2,y+2,10)
    xarray = np.linspace(x,x,10)
    yarray = np.linspace(y,y,10)
    p1.plot(xarray,yrange, pen=(0,0,0),size=10)
    p1.plot(xrange, yarray, pen=(0,0,0),size=10)
    
def drawBox(p1,x1,x2,y1,y2):
    xrange = np.linspace(x1,x2,10)
    yrange = np.linspace(y1,y2,10)
    x1array = np.linspace(x1,x1,10)
    x2array = np.linspace(x2,x2,10)
    y1array = np.linspace(y1,y1,10)
    y2array = np.linspace(y2,y2,10)
    p1.plot(x1array,yrange, pen=(255,0,0),width=3)
    p1.plot(x2array,yrange, pen=(255,0,0),width=3)
    p1.plot(xrange, y1array, pen=(255,0,0),width=3)
    p1.plot(xrange, y2array, pen=(255,0,0),width=3)
    p1.plot(xrange, (y2array+y1array)/2, pen=(0,0,0),width=10)
    p1.plot(xrange, (y2array+y1array)/2+1, pen=(0,0,0),width=10)
    p1.plot(xrange, (y2array+y1array)/2-1, pen=(0,0,0),width=10)
    p1.plot(xrange, (y2array+y1array)/2+1.5, pen=(0,0,0),width=10)
    p1.plot(xrange, (y2array+y1array)/2-1.5, pen=(0,0,0),width=10)
    
def drawCircle(p1,x1,x2,y1,y2):
    sp = pg.scatterPlotItem()    
    p1.addItem(sp)

# Space group dict

spaceGroups = {'P1':1, 'P-1':2, 'P2':3, 'P2_1':4, 'C2':5, 'Pm':6, 
               'P2/m':11, 'P2_1/m':11, 'P222':16, 'P2_1 2_1 2_1':19,
               'Pnma':62, 'P4':75, 'I4':79,
               'P4/mmm':123, 'P4/nmm':129, 'P4_2/mmc':131, 
               'P3':143, 'R3':146, 'P-3':147, 
               'R-3m':166, 'P6':168, 'P63/mmc':194,
               'P432':207, 'P-43m':215, 'F-43m':216, 'Pm-3m':221, 'Pn-3n':222, 'Fd-3m': 227}

    
# Functions to check reflection conditions

def reflCond_1(h,k,l):
    return 1
def reflCond_2(h,k,l):
    return 1
def reflCond_3(h,k,l):
    return 1

def reflCond_4(h,k,l):
    if h==0 and l==0 and (k%2)!=0:
        return 0
    return 1
def reflCond_5(h,k,l):
    if k==0 and l==0 and ((h)%2)!=0:
        return 0
    if h==0 and l==0 and ((k)%2)!=0:
        return 0
    if l==0 and ((h+k)%2)!=0:
        return 0
    if h==0 and ((k)%2)!=0:
        return 0
    if k==0 and ((h)%2)!=0:
        return 0
    if ((h+k)%2)!=0:
        return 0
    return 1


def reflCond_6(h,k,l):
    return 1
def reflCond_10(h,k,l):
    return 1

def reflCond_11(h,k,l):
    if h==0 and l==0 and (k%2)!=0:
        return 0
    return 1

def reflCond_16(h,k,l):
    return 1

def reflCond_19(h,k,l):
    if h==0 and l==0 and (k%2)!=0:
        return 0
    elif h==0 and k==0 and (l%2)!=0:
        return 0
    elif k==0 and l==0 and (h%2)!=0:
        return 0
    return 1

def reflCond_62(h,k,l):
    if h==0 and l==0 and (k%2)!=0:
        return 0
    elif h==0 and k==0 and (l%2)!=0:
        return 0
    elif k==0 and l==0 and (h%2)!=0:
        return 0
    elif h==0 and (k+l)%2!=0:
        return 0
    elif l==0 and (h%2)!=0:
        return 0
    return 1

def reflCond_75(h,k,l):
    return 1

def reflCond_79(h,k,l):
    if k==0 and l==0 and ((h)%2)!=0:
        return 0
    if h==0 and k==0 and ((l)%2)!=0:
        return 0
    if h==k and ((l)%2)!=0:
        return 0
    if h==0 and ((k+l)%2)!=0:
        return 0
    if l==0 and ((h+k)%2)!=0:
        return 0
    if ((h+k+l)%2)!=0:
        return 0
    return 1

def reflCond_123(h,k,l):
    return 1

def reflCond_129(h,k,l):
    if k==0 and l==0 and (h%2)!=0:
        return 0
    elif l==0 and (h+k)%2!=0:
        return 0
    return 1

def reflCond_131(h,k,l):
    if h==k and (l%2)!=0:
        return 0
    if h==0 and k==0 and (l)%2!=0:
        return 0
    return 1

def reflCond_143(h,k,l):
    return 1

def reflCond_146(h,k,l):
    if (-h+k+l)%3!=0 and (h-k+l)%3!=0:
        return 0
    if ((h-k)%3!=0 or (-h+k)%3!=0) and l==0:
        return 0
    if h==k and (l%3)!=0:
        return 0
    if h==-k and (h+l)%3!=0:
        return 0
    if h==k==0 and (l%3)!=0:
        return 0
    if h==-k and l==0 and (h)%3!=0:
        return 0
    return 1


def reflCond_147(h,k,l):
    return 1

def reflCond_166(h,k,l):
    if (-h+k+l)%3!=0 and (h-k+l)%3!=0:
        return 0
    if ((h-k)%3!=0 or (-h+k)%3!=0) and l==0:
        return 0
    if h==k and (l%3)!=0:
        return 0
    if h==-k and (h+l)%3!=0:
        return 0
    if h==k==0 and (l%3)!=0:
        return 0
    return 1

def reflCond_168(h,k,l):
    return 1

def reflCond_194(h,k,l):
    if h==k and l%2!=0:
        return 0
    return 1

def reflCond_207(h,k,l):
    return 1

def reflCond_215(h,k,l):
    return 1

def reflCond_216(h,k,l):
    
    if h==k==0 and (l%2)!=0:
        return 0
    if k==l==0 and (h%2)!=0:
        return 0
    if l==h==0 and (k%2)!=0:
        return 0
    if h==k and ((h+l)%2)!=0:
        return 0
    if k==l and ((k+h)%2)!=0:
        return 0
    if l==h and ((l+k)%2)!=0:
        return 0
    if h==0 and ((k%2)!=0 or (l%2)!=0):
        return 0
    if k==0 and ((l%2)!=0 or (h%2)!=0):
        return 0
    if l==0 and ((h%2)!=0 or (k%2)!=0):
        return 0
    if (h+k)%2!=0 or (k+l)%2!=0 or (l+h)%2!=0:
        return 0
    return 0    

def reflCond_221(h,k,l):
    return 1

def reflCond_222(h,k,l):
    if h==0 and (k+l)%2!=0:
        return 0
    elif k==0 and (l+h)%2!=0:
        return 0
    elif l==0 and (h+k)%2!=0:
        return 0
    elif h==k and l%2!=0:
        return 0
    elif k==l and h%2!=0:
        return 0
    elif l==h and k%2!=0:
        return 0
    elif k==0 and l==0 and h%2!=0:
        return 0
    elif l==0 and h==0 and k%2!=0:
        return 0
    elif h==0 and k==0 and l%2!=0:
        return 0
    else:
        return 1  

def reflCond_227(h,k,l):
    
    if h==k==0 and (l%4)!=0:
        return 0
    elif k==l==0 and (h%4)!=0:
        return 0
    elif l==h==0 and (k%4)!=0:
        return 0
    elif h==k and (h+l)%2!=0:
        return 0
    elif k==l and (k+h)%2!=0:
        return 0
    elif l==h and (l+k)%2!=0:
        return 0
    elif h==0 and ((k+l)%4!=0 or (k%2)!=0 or (l%2)!=0):
        return 0
    elif k==0 and ((l+h)%4!=0 or (l%2)!=0 or (h%2)!=0):
        return 0
    elif l==0 and ((h+k)%4!=0 or (h%2)!=0 or (k%2)!=0):
        return 0
    elif (h+k)%2!=0 or (k+l)%2!=0 or (l+h)%2!=0:
        return 0
    return 1    