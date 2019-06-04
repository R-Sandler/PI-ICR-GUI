import numpy as np
import math as m
import sys
import fnmatch
from scipy import *
import pandas as pd
import re
import lmfit
import matplotlib.pyplot as plt
from lmfit.models import GaussianModel
from lmfit.models import SkewedGaussianModel
from lmfit.models import VoigtModel
from lmfit.models import QuadraticModel
from lmfit.models import ExponentialGaussianModel
from sklearn.cluster import MeanShift

def Calculator(xs, xserr, ys, yserr, cluster_of_interest):


    xs[0]=xs[cluster_of_interest]
    xserr[0]=xserr[cluster_of_interest]
    ys[0]=ys[cluster_of_interest]
    yserr[0]=yserr[cluster_of_interest]

    radius = np.sqrt(np.square(xs[0]+1.94)+np.square(ys[0]-3.77))
    radius = round(radius, 3)
    radius_uncertainty = np.sqrt(np.square(xserr[0])+np.square(yserr[0]))
    radius_uncertainty = round(radius_uncertainty, 3)

    angle = m.atan2(3.77-ys[0],-1.94-xs[0])
    angle_uncertainty = 1/(np.square(3.77-ys[0])+np.square(-1.94-xs[0]))*np.sqrt(np.square(-1.94-xs[0])*np.square(0.05)+np.square(xs[0]+1.94)*np.square(yserr[0])+np.square(ys[0]-3.77)*np.square(0.05)+np.square(3.77-ys[0])*np.square(xserr[0]))
    angle = round(angle, 3)
    angle_uncertainty = round(angle_uncertainty, 3)

    return radius, radius_uncertainty, angle, angle_uncertainty

def Frequency(refAngle, drefAngle, measAngle, dmeasAngle, radius):
    frequency_guess = 781283.9864
    time = 345009

    rot_time = 1000000/frequency_guess
    N = int(round(time/rot_time))
    theta = measAngle-refAngle
    if theta<0:
        theta = theta+2*pi
        N = N-1
    frequency = (theta+2*pi*N)/(2*pi*time*0.000001)
    frequency_uncertainty = np.sqrt(np.square(drefAngle)+np.square(dmeasAngle))
    frequency = round(frequency, 4)
    frequency_uncertainty = round(frequency_uncertainty, 4)

    return N, theta, frequency, frequency_uncertainty

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
