import numpy as np
import math as m
import sys
import fnmatch
from scipy import *
import pandas as pd
import re
import csv
import lmfit
import matplotlib.pyplot as plt
from lmfit.models import GaussianModel
from lmfit.models import SkewedGaussianModel
from lmfit.models import VoigtModel
from lmfit.models import QuadraticModel
from lmfit.models import ExponentialGaussianModel
from sklearn.cluster import MeanShift
from PyQt5 import QtCore, QtGui, QtWidgets

def Calculator(xs, xserr, ys, yserr, cluster_of_interest, xCenter, yCenter):

    radius = np.sqrt(np.square(xs[cluster_of_interest]-xCenter)+np.square(ys[cluster_of_interest]-yCenter))
    radius = round(radius, 3)
    radius_uncertainty = np.sqrt(np.square(xserr[cluster_of_interest])+np.square(yserr[cluster_of_interest]))
    radius_uncertainty = round(radius_uncertainty, 3)

    angle = m.atan2(yCenter-ys[cluster_of_interest],xCenter-xs[cluster_of_interest])
    angle_uncertainty = 1/(np.square(yCenter-ys[cluster_of_interest])+np.square(xCenter-xs[cluster_of_interest]))*np.sqrt(np.square(xCenter-xs[cluster_of_interest])*np.square(0.05)+np.square(xs[cluster_of_interest]-xCenter)*np.square(yserr[cluster_of_interest])+np.square(ys[cluster_of_interest]-yCenter)*np.square(0.05)+np.square(yCenter-ys[cluster_of_interest])*np.square(xserr[cluster_of_interest]))
    angle = round(angle, 3)
    angle_uncertainty = round(angle_uncertainty, 3)
    #print(rxs)

    return radius, radius_uncertainty, angle, angle_uncertainty

def Frequency(rxs, rxserr, rys, ryserr, rindex, mxs, mxserr, mys, myserr, mindex, frequency_guess, time, xCenter, yCenter):

    #frequency_guess = 781283.9864
    #time = 345009

    rot_time = 1000000/frequency_guess
    N = int(round(time/rot_time))
    radius = np.sqrt(np.square(mxs[mindex]-xCenter)+np.square(mys[mindex]-yCenter))
    
    theta = m.atan2(yCenter-mys[mindex],xCenter-mxs[mindex])-m.atan2(yCenter-rys[rindex],xCenter-rxs[rindex])
    theta_uncertainty = 1/(np.square(yCenter-mys[mindex])+np.square(xCenter-mxs[mindex]))*np.sqrt(np.square(xCenter-mxs[mindex])*np.square(0.05)+np.square(mxs[mindex]-xCenter)*np.square(myserr[mindex])+np.square(mys[mindex]-yCenter)*np.square(0.05)+np.square(yCenter-mys[mindex])*np.square(mxserr[mindex]))
    if theta<0:
        theta = theta+2*pi
        N = N-1
    frequency = (theta+2*pi*N)/(2*pi*time*0.000001)
    frequency_uncertainty = np.sqrt(np.square(rys[rindex]*rxserr[rindex])+np.square(rxs[rindex]*ryserr[rindex])+np.square(rxs[rindex]*ryserr[rindex])+np.square(rys[rindex]*rxserr[rindex]))/(2*pi*radius*radius*time*0.000001)

    theta = round(theta, 3)
    theta_uncertainty = round(theta_uncertainty, 3)
    frequency = round(frequency, 4)
    frequency_uncertainty = round(frequency_uncertainty, 4)
    return N, theta, theta_uncertainty, frequency, frequency_uncertainty

def AddSubN(rxs, rxserr, rys, ryserr, rindex, mxs, mxserr, mys, myserr, mindex, frequency_guess, time, xCenter, yCenter, newN):

    
    newRadius = np.sqrt(np.square(mxs[mindex]-xCenter)+np.square(mys[mindex]-yCenter))
    
    newTheta = m.atan2(yCenter-mys[mindex],xCenter-mxs[mindex])-m.atan2(yCenter-rys[rindex],xCenter-rxs[rindex])
    newTheta_uncertainty = 1/(np.square(yCenter-mys[mindex])+np.square(xCenter-mxs[mindex]))*np.sqrt(np.square(xCenter-mxs[mindex])*np.square(0.05)+np.square(mxs[mindex]-xCenter)*np.square(myserr[mindex])+np.square(mys[mindex]-yCenter)*np.square(0.05)+np.square(yCenter-mys[mindex])*np.square(mxserr[mindex]))
    if newTheta<0:
        newTheta = newTheta+2*pi
        newN = newN-1
    newFrequency = (newTheta+2*pi*newN)/(2*pi*time*0.000001)
    newFrequency_uncertainty = np.sqrt(np.square(rys[rindex]*rxserr[rindex])+np.square(rxs[rindex]*ryserr[rindex])+np.square(rxs[rindex]*ryserr[rindex])+np.square(rys[rindex]*rxserr[rindex]))/(2*pi*newRadius*newRadius*time*0.000001)
    
    newTheta = round(newTheta, 3)
    newTheta_uncertainty = round(newTheta_uncertainty, 3)
    newFrequency = round(newFrequency, 4)
    newFrequency_uncertainty = round(newFrequency_uncertainty, 4)
    
    return newTheta, newTheta_uncertainty, newFrequency, newFrequency_uncertainty
    

def CalibrationMass(calibNuclide, calibCharge):
    try:
        AMEFile = open('ame2016.txt', 'r')
        AMEData = AMEFile.readlines()
        for i in range(0,len(AMEData)):
            AMEData[i] = AMEData[i].split("\t")
        AMEFile.close()


        #if calibNuclide.find(":")>-1:
            #The nuclide is actually a molecule. Crap
        for i in range(0, len(calibNuclide)):
            if calibNuclide[i].isalpha():
                speciesStart = i
                if calibNuclide[i+1].isalpha():
                    speciesEnd = i+2
                else:
                    speciesEnd = i+1

        calibCount = int(calibNuclide[0:speciesStart])
        calibSpecies = calibNuclide[speciesStart:speciesEnd]
        calibNucleons = calibNuclide[speciesEnd:len(calibNuclide)]

        for i in range(0, len(AMEData)):
            if AMEData[i][2] == calibSpecies:
                if AMEData[i][1] == calibNucleons:
                    calibME = float(AMEData[i][3])

        calibNucleons = float(calibNucleons)           
        calibMass = round(calibCount/calibCharge*(calibNucleons+(calibME/931494.0954)),8)

    except FileNotFoundError:
        msg = QtWidgets.QMessageBox()
        title = "Missing AME file"
        message = "No AME file found. Please check that there is an AME file."
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec_()
        calibMass = 38.963706487

    return calibMass

def ExpectedFrequency(calibMass, calibFreqC, measNuclide, measCharge):
    try:
        AMEFile = open('ame2016.txt', 'r')
        AMEData = AMEFile.readlines()
        for i in range(0,len(AMEData)):
            AMEData[i] = AMEData[i].split("\t")
        AMEFile.close()

        #if calibNuclide.find(":")>-1:
            #The nuclide is actually a molecule. Crap
        for i in range(0, len(measNuclide)):
            if measNuclide[i].isalpha():
                speciesStart = i
                if measNuclide[i+1].isalpha():
                    speciesEnd = i+2
                else:
                    speciesEnd = i+1
        measCount = int(measNuclide[0:speciesStart])
        measSpecies = measNuclide[speciesStart:speciesEnd]
        measNucleons = measNuclide[speciesEnd:len(measNuclide)]

        for i in range(0, len(AMEData)):
            if AMEData[i][2] == measSpecies:
                if AMEData[i][1] == measNucleons:
                    measME = float(AMEData[i][3])

        measNucleons = float(measNucleons)
        measMass = round(measCount/measCharge*(measNucleons+(measME/931494.0954)),8)
        expFreq = calibFreqC*calibMass/measMass
    except FileNotFoundError:
        msg = QtWidgets.QMessageBox()
        title = "Missing AME file"
        message = "No AME file found. Please check that there is an AME file."
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec_()
        expFreq = 3688955.2387
    return expFreq

def poswithtof(name, tlow, thigh, *args):

    data = pd.read_csv(name, sep = '\t', names = ['chan', 'count', 'time', 'trig'], comment = '#')

    source = "".join(array(array(data.chan.values,int),str))
    pattern = "12347"
    c = source.count(pattern)
    res = [m.start() for m in re.finditer(pattern,source)]

    df = [data.iloc[i:i+5] for i in res]

    h = pd.concat(df,keys=res).reset_index()
    h.columns = ["num1","num2","chan","count","time","trig"]

    df = pd.DataFrame([])

    df["x1"] = h.set_index("num1").query("chan==1").time
    df["x2"] = h.set_index("num1").query("chan==2").time
    df["y1"] = h.set_index("num1").query("chan==3").time
    df["y2"] = h.set_index("num1").query("chan==4").time
    df["tof"] = h.set_index("num1").query("chan==7").time
    df["trig"] = h.set_index("num1").query("chan==7").trig
    df['sumx'] = df['x1'] + df['x2']
    df['sumy'] = df['y1'] + df['y2']

    df = df.query('%f<tof<%f'%(tlow,thigh))
    df = df.query('45 < sumx < 48 and 44 < sumy < 47')

    #df['trig'] = df.trig.round(decimals = 1)

    df = df.reset_index().set_index("trig")
    df["ips"] = df.reset_index().groupby("trig").trig.count()
    df = df.reset_index().set_index('num1')

    if len(args) == 1:
        df = df.query('ips < %i'%args[0])

    df2 = pd.DataFrame(columns = ['xpos', 'ypos'])

    XPOS = (df['x1'].values - df['x2'].values)*1.29/2.0        
    YPOS = (df['y1'].values - df['y2'].values)*1.31/2.0

    SUMX = df['sumx'].values
    SUMY = df['sumy'].values

    DIFFXY = SUMX - SUMY

    #TRIG = df['trig'].values

    TOF = df['tof'].values
    IPS = df['ips'].values

    df2['xpos'] = XPOS
    df2['ypos'] = YPOS
    df2['tof'] = TOF
    #df2['trig'] = TRIG
    df2['sumx'] = SUMX
    df2['sumy'] = SUMY
    df2['ips'] = IPS

    return XPOS,YPOS,TOF,SUMX,SUMY,df2


def cluster_spots(xdata,ydata, radius, *args):

    if len(args) == 0:
        binnum = len(xdata)/100.0
    if len(args) == 1:
        binnum = args[0] * len(xdata)/100.0
    ms = MeanShift(bin_seeding = True, min_bin_freq = binnum, cluster_all = False, bandwidth = radius) # was 3.5 bandwidth
    
    X = []
    for i in range(len(xdata)):
        X.append([xdata[i], ydata[i]])

    X = array(X)
    ms.fit(X)
    labels = ms.labels_
    cluster_center = ms.cluster_centers_
    n_clusters_ = len(unique(labels)) - (1 if -1 in labels else 0)

    xstuff, ystuff = {},{}
    ips = []
    
    for i in range(0,n_clusters_):
        xstuff['%i'%i] = X[labels == i][:,0]
        ystuff['%i'%i] = X[labels == i][:,1]
        ips.append(len(xstuff['%i'%i]))

    xs = []
    xserr = []
    ys = []
    yserr = []
    ips = []
    
    clust_ind = arange(0,n_clusters_)

    def numbins(x):
        IQR  = percentile(x,75) - percentile(x,25)
        h = 2*IQR/(len(x)**(1.0/3.0))
        num = ceil((max(x) - min(x))/ (h))
        return num


    for i in range(0,len(clust_ind)):
        xcut = []
        ycut = []
        for j in range(len(labels)):
            if labels[j] == clust_ind[i]:
                xcut.append(xdata[j])
                ycut.append(ydata[j])
        widthx = max(xcut) - min(xcut)
        widthy = max(ycut) - min(ycut)
        xfit = gaussmodel(min(xcut)-0.1*widthx, max(xcut)+0.1*widthx, xcut, numbins(xcut), 'cadetblue')
        yfit = gaussmodel(min(ycut)-0.1*widthy, max(ycut)+0.1*widthy, ycut, numbins(ycut), 'darkorange')
        xs.append(xfit[0])
        xserr.append(xfit[1])
        ys.append(yfit[0])
        yserr.append(yfit[1])
        ips.append(len(xcut))


    xkeep, ykeep = [],[]
    for i in range(len(labels)):
        if labels[i] > -1:
            xkeep.append(X[i][0])
            ykeep.append(X[i][1])
    return xs, xserr, ys, yserr, ips, xkeep, ykeep, X, n_clusters_, labels, cluster_center

def gaussmodel(xmin,xmax,data,numbin, *args):#clr):
    if len(args) == 0:
        clr = new_blue
    if len(args) == 1:
        clr = args[0]
    #xbins = plt.hist(data, bins = numbin, range = (xmin,xmax), alpha = 0.6, color = clr, histtype = 'stepfilled')
    xbins = plt.hist(data, bins = 6, range = (xmin,xmax), alpha = 0.6, color = clr, histtype = 'stepfilled')
    xcenter = (xbins[1][:-1] + xbins[1][1:])/2.0
    mod = GaussianModel()
    pars = mod.guess(xbins[0], x = xcenter)
    fit = mod.fit(xbins[0], x = xcenter, params = pars, method = 'leastsq')
    #print fit.fit_report()
    xfit = arange(xmin,xmax, 0.01)
    #plt.plot(xfit, fit.eval(x=xfit), 'k-')
    return fit.params['center'].value, fit.params['center'].stderr
