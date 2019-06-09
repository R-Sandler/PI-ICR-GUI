from numpy import *
from scipy import *
from math import *
import pandas as pd
#from useful_stuff import *
import re
import lmfit


#name = 'sis_on_full_bias_1-7_notrp.lmf.txt'

new_blue = '#3F5D7D'

def position(name, length):
    a = pd.read_csv(name, sep = '\t', header = None, names = ['chan', 'count', 'time', 'trig'], comment = '#')#, comment = '#', header = 0)#, nrows = 10)   
    chan = array(a['chan'])
    time = array(a['time'])
    trig = array(a['trig'])

    x1, x2, y1, y2 = [],[],[],[]
    if length == 0:
        for i in xrange(len(chan)):
            t = trig[i]
            if chan[i] ==1 and chan[i+1]==2 and  chan[i+2]==3 and chan[i+3] ==4 and trig[i+2]==t and trig[i+3] == t:
            #if (chan[i]+chan[i+1] + chan[i+2] + chan[i+3]) == 10  and trig[i+3] == t:
                x1.append(time[i])
                x2.append(time[i+1])
                y1.append(time[i+2])
                y2.append(time[i+3])
    if length != 0:
        for i in xrange(0,length):
            t = trig[i]
            if chan[i] ==1 and chan[i+1]==2 and  chan[i+2]==3 and chan[i+3] ==4 and trig[i+2]==t and trig[i+3] == t:
            #if (chan[i]+chan[i+1] + chan[i+2] + chan[i+3]) == 10  and trig[i+3] == t:
                x1.append(time[i])
                x2.append(time[i+1])
                y1.append(time[i+2])
                y2.append(time[i+3])


    x1 = array(x1)
    x2 = array(x2)
    y1 = array(y1)
    y2 = array(y2)

    xpos = (x1-x2)/2.0
    ypos = (y1-y2)/2.0

    return xpos, ypos, x1, x2, y1, y2, trig

def poswithcuts(name, length):
    a = pd.read_csv(name, sep = '\t', header = None, names = ['chan', 'count', 'time', 'trig'], comment = '#')#, comment = '#', header = 0)#, nrows = 10)
    chan = array(a['chan'])
    time = array(a['time'])
    trig = array(a['trig'])

    x1, x2, y1, y2 = [],[],[],[]
    if length == 0:
        for i in xrange(len(chan)):
            t = trig[i]
            if chan[i] ==1 and chan[i+1]==2 and  chan[i+2]==3 and chan[i+3] ==4 and trig[i+2]==t and trig[i+3] == t:
            #if (chan[i]+chan[i+1] + chan[i+2] + chan[i+3]) == 10  and trig[i+3] == t:
                x1.append(time[i])
                x2.append(time[i+1])
                y1.append(time[i+2])
                y2.append(time[i+3])

    if length != 0:
        for i in xrange(0,length):
            t = trig[i]
            if chan[i] ==1 and chan[i+1]==2 and  chan[i+2]==3 and chan[i+3] ==4 and trig[i+2]==t and trig[i+3] == t:
            #if (chan[i]+chan[i+1] + chan[i+2] + chan[i+3]) == 10  and trig[i+3] == t:
                x1.append(time[i])
                x2.append(time[i+1])
                y1.append(time[i+2])
                y2.append(time[i+3])



    x1 = array(x1)
    x2 = array(x2)
    y1 = array(y1)
    y2 = array(y2)

    sumx = x1 + x2
    sumy = y1 + y2

    diffxy = x1+x2-y1-y2

    X1,X2,Y1,Y2 = [],[],[],[]

    for i in range(len(sumx)):
        if sumx[i]<25.0 and sumx[i] > 12.0 and sumy[i]<25.0 and sumy[i] > 12.0 and diffxy[i] < 1.5 and diffxy[i]> 0.0:
            X1.append(x1[i])
            X2.append(x2[i])
            Y1.append(y1[i])
            Y2.append(y2[i])

    X1 = array(X1)
    X2 = array(X2)
    Y1 = array(Y1)
    Y2 = array(Y2)

    xpos = (x1-x2)*1.32/2.0
    ypos = (y1-y2)*1.43/2.0

    XPOS = (X1-X2)*1.32/2.0
    YPOS = (Y1-Y2)*1.43/2.0

    return XPOS, YPOS, diffxy, sumx, sumy# x1, x2, y1, y2, trig
####
#def poswithtof(name, length, *args):
#    a = pd.read_csv(name, sep = '\t', header = None, names = ['chan', 'count', 'time', 'trig'], comment = '#')#, comment = '#', header = 0)#, nrows = 10)
#    chan = array(a['chan'])
#    time = array(a['time'])
#    trig = array(a['trig'])
#
#    x1, x2, y1, y2, tof, trigger = [],[],[],[],[], []
#    if length == 0:
#        for i in xrange(len(chan)):
#            t = trig[i]
#            if chan[i] ==1 and chan[i+1]==2 and chan[i+2]==3 and chan[i+3] ==4 and chan[i+4] == 7 and trig[i+2]==t and trig[i+4] == t:
#            #if (chan[i]+chan[i+1] + chan[i+2] + chan[i+3]) == 10  and trig[i+3] == t:
#                x1.append(time[i])
#                x2.append(time[i+1])
#                y1.append(time[i+2])
#                y2.append(time[i+3])
#                tof.append(time[i+4])
#                trigger.append(trig[i])
#                maxt = t
#
#    if length != 0:
#        for i in xrange(0,length):
#            t = trig[i]
#            if chan[i] ==1 and chan[i+1]==2 and chan[i+2]==3 and chan[i+3] ==4 and chan[i+4] == 7 and trig[i+2]==t and trig[i+4] == t:
#            #if (chan[i]+chan[i+1] + chan[i+2] + chan[i+3]) == 10  and trig[i+3] == t:
#                x1.append(time[i])
#                x2.append(time[i+1])
#                y1.append(time[i+2])
#                y2.append(time[i+3])
#                tof.append(time[i+4])
#                maxt = t
#                trigger.append(trig[i])
#
#
#
#    x1 = array(x1)
#    x2 = array(x2)
#    y1 = array(y1)
#    y2 = array(y2)
#    tof = array(tof)
#
#    sumx = x1 + x2
#    sumy = y1 + y2
#
#    diffxy = x1+x2-y1-y2
#
#    X1,X2,Y1,Y2, TOF, TRIGGER = [],[],[],[],[],[]
#
#    if len(args)<1:
#        for i in range(len(sumx)):
#            if tof[i] < -50000.0 and tof[i]>-90000.0:
#            #if sumx[i]<47.0 and sumx[i] > 44.0 and sumy[i]<47.0 and sumy[i] > 44.0 and diffxy[i] < 2.0 and diffxy[i]> 0.0:
#                X1.append(x1[i])
#                X2.append(x2[i])
#                Y1.append(y1[i])
#                Y2.append(y2[i])
#                TOF.append(tof[i])
#                TRIGGER.append(trigger[i])
#    if len(args)==2.0:
#        for i in range(len(sumx)):
#            if tof[i] < args[1] and tof[i] > args[0]:
#                X1.append(x1[i])
#                X2.append(x2[i])
#                Y1.append(y1[i])
#                Y2.append(y2[i])
#                TOF.append(tof[i])
#                TRIGGER.append(trigger[i])
#
#    if len(args)==3.0:
#        ioncut = args[2]
#        X1t, X2t, Y1t,Y2t, TOFt, TRIGERt = [],[],[],[],[],[]
#        for i in range(len(sumx)):
#            if tof[i] < args[1] and tof[i] > args[0]:
#                X1t.append(x1[i])
#                X2t.append(x2[i])
#                Y1t.append(y1[i])
#                Y2t.append(y2[i])
#                TOF.append(tof[i])
#                TRIGGER.append(trigger[i])
#        X1t = array(X1t)
#        X2t = array(X2t)
#        Y1t = array(Y1t)
#        Y2t = array(Y2t)
#        xx,yy,xx2,yy2 = [],[],[],[]
#        unique_temp = unique(TRIGGER)
#        for i in range(len(unique_temp)):
#            val = where(TRIGGER == unique_temp[i])[0]
#            xx.append((X1t[val]))
#            xx2.append((X2t[val]))
#            yy.append((Y1t[val]))
#            yy2.append((Y2t[val]))
#            
#        XCUT1 = {'%i'%i:[] for i in range(1,15)}
#        XCUT2 = {'%i'%i:[] for i in range(1,15)}
#        YCUT1 = {'%i'%i:[] for i in range(1,15)}
#        YCUT2 = {'%i'%i:[] for i in range(1,15)}
#
#        for i in range(len(xx)):
#            for j in range(1,15):
#                if len(xx[i]) == j:
#                       XCUT1['%i'%j].extend(xx[i])
#                       XCUT2['%i'%j].extend(xx2[i])
#                       YCUT1['%i'%j].extend(yy[i])
#                       YCUT2['%i'%j].extend(yy2[i])
#
#        xcuts, ycuts = [],[]
#        for i in range(1,ioncut):
#            X1.extend(XCUT1['%i'%i])
#            X2.extend(XCUT2['%i'%i])
#            Y1.extend(YCUT1['%i'%i])
#            Y2.extend(YCUT2['%i'%i])
#            
#    X1 = array(X1)
#    X2 = array(X2)
#    Y1 = array(Y1)
#    Y2 = array(Y2)
#
#    xpos = (x1-x2)*1.29/2.0#*1.32/2.0
#    ypos = (y1-y2)*1.31/2.0#1.43/2.0
#
#    XPOS = (X1-X2)*1.29/2.0#*1.32/2.0
#    YPOS = (Y1-Y2)*1.31/2.0#*1.43/2.0
#
#    SUMX = X1+X2
#    SUMY = Y1+Y2
#
#    TRIG = around(TRIGGER, decimals = 1)
#
#    return XPOS, YPOS, TOF, SUMX, SUMY, tof, maxt, TRIG# x1, x2, y1, y2, trig
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
    #return df2

##def poswithtof(name, tlow, thigh, *args):
##    data = pd.read_csv(name, sep = '\t', names = ['chan', 'count', 'time', 'trig'], comment = '#')
##
##    source = "".join(array(array(data.chan.values,int),str))
##    pattern = "12347"
##    c = source.count(pattern)
##    res = [m.start() for m in re.finditer(pattern,source)]
##
##    df = [data.iloc[i:i+5] for i in res]
##
##    h = pd.concat(df,keys=res).reset_index()
##    h.columns = ["num1","num2","chan","count","time","trig"]
##
##    df = pd.DataFrame([])
##
##    df["x1"] = h.set_index("num1").query("chan==1").time
##    df["x2"] = h.set_index("num1").query("chan==2").time
##    df["y1"] = h.set_index("num1").query("chan==3").time
##    df["y2"] = h.set_index("num1").query("chan==4").time
##    df["tof"] = h.set_index("num1").query("chan==7").time
##    df["trig"] = h.set_index("num1").query("chan==7").trig
##
##    df = df.query('%f<tof<%f'%(tlow,thigh))
##    df['trig'] = df.trig.round(decimals = 1)
##    
##    df = df.reset_index().set_index("trig")
##    df["ips"] = df.reset_index().groupby("trig").trig.count()
##    df = df.reset_index().set_index('num1')
##
##    if len(args) == 1:
##        df = df.query('ips < %i'%args[0])
##
##    df2 = pd.DataFrame(columns = ['xpos', 'ypos'])
##    
##    XPOS = (df['x1'].values - df['x2'].values)*1.29/2.0        
##    YPOS = (df['y1'].values - df['y2'].values)*1.31/2.0
##    
##    SUMX = df['x1'].values + df['x2'].values
##    SUMY = df['y1'].values + df['y2'].values
##    
##    DIFFXY = SUMX - SUMY
##
##    TRIG = df['trig'].values
##    
##    TOF = df['tof'].values
##    IPS = df['ips'].values
##    
##    df2['xpos'] = XPOS
##    df2['ypos'] = YPOS
##    df2['tof'] = TOF
##    df2['trig'] = TRIG
##    df2['sumx'] = SUMX
##    df2['sumy'] = SUMY
##    df2['ips'] = IPS
##    
##    return XPOS,YPOS,TOF,SUMX,SUMY,TRIG, df2

##def poswithtof(name, tlow, thigh):
##    def clean_hit(group):
##        match = array_equal(group.chan.values, [1,2,3,4,7]) or array_equal(group.chan.values, [1,2,3,4, 7, 8]) 
##        return match
##        
##    
##    data = pd.read_csv(name, sep = '\t', names = ['chan', 'count', 'time', 'trig'], comment = '#')
##    
##    
##    temp_data = data.groupby('trig')
##    
##    data = data.set_index('trig')
##    
##    data['clean_temp'] = temp_data.chan.count() == 5   # and -40000 < temp_data.chan.values == 7 < -15000 
##    data['clean_temp2'] = temp_data.chan.count() == 6 
##    data = data.query('(clean_temp or clean_temp2) == True').reset_index()
##    
##    temp_data = data.groupby('trig')
##    data = data.set_index('trig')
##    
##    data['valid'] = temp_data.apply(clean_hit)
##    #data['diff'] = data.trig.diff()
##    
##    data = data.query('valid == True')# and '%f < time < %f'%(tlow,thigh))
##    
##    
##    #
##    data['x1'] = data.query('chan==1').time
##    data['x2'] = data.query('chan==2').time
##    data['y1'] = data.query('chan==3').time
##    data['y2'] = data.query('chan==4').time
##    data['tof'] = data.query('chan==7').time
##    
##    data = data.reset_index().drop_duplicates('trig').drop(["chan","count","time","valid","clean_temp", "clean_temp2"], axis =1)
##    
##    data = data.query('%f<tof<%f'%(tlow,thigh))
##    
##    XPOS = (data['x1'].values - data['x2'].values)*1.29/2.0        
##    YPOS = (data['y1'].values - data['y2'].values)*1.31/2.0
##    
##    SUMX = data['x1'].values + data['x2'].values
##    SUMY = data['y1'].values + data['y2'].values
##    
##    DIFFXY = SUMX - SUMY
##
##    TRIG = data['trig'].values
##    
##    TOF = data['tof'].values
##    
##    return XPOS,YPOS,TOF,SUMX,SUMY,TRIG, data

def cuts(xpos, ypos, xg,yg, radius):
    xdata, ydata = [],[]
    for i in range(len(xpos)):
        if (xpos[i]-xg)**2 < (radius**2 - (ypos[i] -yg)**2) and (ypos[i]-yg)**2 < (radius**2 - (xpos[i] - xg)**2):
            xdata.append(xpos[i])
            ydata.append(ypos[i])

    return xdata, ydata


def xycuts(xpos, ypos, xg,yg,radius, numbin):
    xdata, ydata = [],[]
    for i in range(len(xpos)):
        if (xpos[i]-xg)**2 < (radius**2 - (ypos[i] -yg)**2) and (ypos[i]-yg)**2 < (radius**2 - (xpos[i] - xg)**2):
            xdata.append(xpos[i])
            ydata.append(ypos[i])

    xhist, xbins = histogram(xdata, bins = numbin)
    xwidth = xbins[1] - xbins[0]
    xcenter = (xbins[:-1] + xbins[1:])/2.0


    yhist, ybins = histogram(ydata, bins = numbin)
    ywidth = ybins[1] - ybins[0]
    ycenter = (ybins[:-1] + ybins[1:])/2.0
##    xhist = plt.hist(xdata, numbin, color = 'orange', edgecolor = 'white')
##    centerx = (xhist[1][:-1] + xhist[1][1:])/2.0
##
##    yhist = plt.hist(ydata, numbin, color = 'blue', edgecolor = 'white')
##    centery = (yhist[1][:-1] + yhist[1][1:])/2.0
##
    #xfit = gauss(min(xcenter), max(xcenter), xg, fwhm, xcenter, xhist, sqrt(xhist))

    return xcenter, xhist, xwidth, ycenter, yhist, ywidth

    ##return centerx, xhist[0], centery, yhist[0]


def histph(data, numbin):
    xhist, xbins = histogram(data, bins = numbin)
    xwidth = xbins[1] - xbins[0]
    xcenter = (xbins[:-1] + xbins[1:])/2.0
    plt.bar(xcenter, xhist, width = xwidth, alpha = 0.8, color = 'orange', edgecolor = 'white')

    return xhist

def gaussph(xmin, xmax,cg,dg, x, y, err):
    def gaussfit(params,x,y,err):
        a = params['a'].value
        b=params['b'].value
        c=params['c'].value
        d=params['d'].value

        function = a*exp(-(x-b)**2/(2*c**2))+d# + a2*exp(-(x-b2)**2/(2*c2**2)) + d # + a3*exp(-(x-b3)**2/(2*c3**2))+d
        resids = function-y
        weighted = sqrt(resids**2/err**2)
        return weighted

    xnew,ynew,errnew = [],[],[]
    for i in range(len(x)):
        if x[i] < xmax and x[i] > xmin:
            xnew.append(x[i])
            ynew.append(y[i])
            errnew.append(err[i])

    xnew = array(xnew)
    ynew = array(ynew)
    errnew = array(errnew)

    params = lmfit.Parameters()
    params.add('a', value = max(ynew), vary = True)
    params.add('b', value = xnew[list(ynew).index(max(ynew))], vary = True)
    params.add('c', value = cg, vary = True)
    params.add('d', value = dg, vary = False)


    fit = lmfit.minimize(gaussfit, params, args = (xnew,ynew, errnew), method = 'leastsq')

    lmfit.report_errors(params)

    a = params['a'].value
    b = params['b'].value
    berr = params['b'].stderr
    c = params['c'].value
    d = params['d'].value

    xfit = arange(xmin,xmax,0.02)
    yfit = a*exp(-(xfit-b)**2/(2*c**2))+d # + a2*exp(-(xfit-b2)**2/(2*c2**2)) + d # + a3*exp(-(xfit-b3)**2/(2*c3**2))+d
    plt.plot(xfit,yfit,'b-')
    return b, berr

def xyplot(xdata, ydata, xguess, yguess, radius, bins, width):
    DATA = xycuts(xdata, ydata, xguess, yguess, radius, bins)
    plt.subplot(121)
    fit1 = gauss(xguess - radius, xguess + radius, xguess, width, DATA[0], DATA[1], sqrt(DATA[1]))
    plt.bar(DATA[0]-DATA[2]/2.0, DATA[1], width = DATA[2], alpha = 0.8, color = 'orange', edgecolor = 'white')
    plt.xlabel('xpos (mm)')
    plt.subplot(122)
    fit2 = gauss(yguess - radius, yguess + radius, yguess, width, DATA[3], DATA[4], sqrt(DATA[4]))
    plt.bar(DATA[3]-DATA[5]/2.0, DATA[4], width = DATA[5], alpha = 0.8, color = 'blue', edgecolor = 'white')
    plt.xlabel('ypos (mm)')
    plt.show()

    return fit1[0], fit1[1], fit2[0], fit2[1]####, fit1[2]


def tofcut(xpos, ypos, TOF, xg,yg, radius):
    xdata, ydata, tof = [],[],[]
    for i in range(len(xpos)):
        if (xpos[i]-xg)**2 < (radius**2 - (ypos[i] -yg)**2) and (ypos[i]-yg)**2 < (radius**2 - (xpos[i] - xg)**2):
            xdata.append(xpos[i])
            ydata.append(ypos[i])
            tof.append(TOF[i])
    return xdata, ydata, tof


def gaussfitplot(xmin,xmax,bg,cg,data,numbin, clr):
##    xhist, xbins = histogram(data, bins = numbin, range = (xmin,xmax))
##    xwidth = xbins[1] - xbins[0]
##    xcenter = (xbins[:-1] + xbins[1:])/2.0
##    fit = gauss(xmin,xmax, bg,cg,xcenter, xhist, sqrt(xhist))
##    plt.bar(xcenter-xwidth/2.0, xhist, width = xwidth, alpha = 0.6, linewidth = 0, color = clr)
##
    xbins = plt.hist(data, bins = numbin, range = (xmin,xmax), alpha = 0.6, color = clr, histtype = 'stepfilled')
    xcenter = (xbins[1][:-1] + xbins[1][1:])/2.0
    fit = gauss(xmin,xmax, bg,cg, xcenter, xbins[0], sqrt(xbins[0]))
    return fit[0], fit[1]


def connect(a,b):
    x = array([a[0], b[0]+a[0]])
    y = array([a[1], b[1]+a[1]])
    plt.plot(x,y, 'b-')
    plt.text(b[0]/2, b[1]/2, '%ls' %(round(linalg.norm(b),2)))
    return 0

def findphi(ref, fin):
    det = ref[0]*fin[1] - fin[0]*ref[1]
    dot = ref[0]*fin[0] + ref[1]*fin[1]
    lenref = linalg.norm(ref)
    lenfin = linalg.norm(fin)
    phi = atan2(det,dot)
    if phi < 0:
        phi = phi + 2*pi
    return phi

def findphiplus(ref,fin,referr,finerr):
    det = ref[0]*fin[1] - fin[0]*ref[1]
    dot = ref[0]*fin[0] + ref[1]*fin[1]
    lenref = linalg.norm(ref)
    lenfin = linalg.norm(fin)
    phi = atan2(det,dot) 
    if phi < 0:
        phi = phi + 2*pi
    errphi = sqrt(lenref**4 * ((fin[0]*finerr[1])**2 + (fin[1]*finerr[0])**2) + lenfin**4 *((ref[0]*referr[1])**2 + (ref[1]*referr[0])**2))/ (lenref*lenfin)**2
    return phi, errphi

def findphiminus(ref,fin,referr,finerr):
    det = ref[0]*fin[1] - fin[0]*ref[1]
    dot = ref[0]*fin[0] + ref[1]*fin[1]
    lenref = linalg.norm(ref)
    lenfin = linalg.norm(fin)
    phi = -atan2(det,dot)
    if phi < 0:
        phi = phi + 2*pi
    errphi = sqrt(lenref**4 * ((fin[0]*finerr[1])**2 + (fin[1]*finerr[0])**2) + lenfin**4 *((ref[0]*referr[1])**2 + (ref[1]*referr[0])**2))/ (lenref*lenfin)**2
    return phi, errphi


def findphiwminus(ref, fin):
    det = ref[0]*fin[1] - fin[0]*ref[1]
    dot = ref[0]*fin[0] + ref[1]*fin[1]
    phi = -atan2(det,dot)
    if phi < 0:
        phi = phi + 2*pi
    return phi
#
def ellipse_fit(xraw,yraw,hg,kg,ag,bg, thetaguess):
    def ell_fit(params, x,y):
        h = params['h'].value
        k = params['k'].value
        a = params['a'].value
        b = params['b'].value
        theta = params['theta'].value
        
        function = (a*b)**2 - (b**2)*((x-h)*cos(theta) + (y-k)*sin(theta))**2 - (a**2)*((x-h)*sin(theta) - (y-k)*cos(theta))**2
        
        resids = function
        
        return resids
    
    params = lmfit.Parameters()
    params.add('h', value = hg, vary = True)
    params.add('k', value = kg, vary = True)
    params.add('a', value = ag, vary = True)
    params.add('b', value = bg, vary = True)
    params.add('theta',value = thetaguess*pi/180.0, vary = True)
    
    fit = lmfit.minimize(ell_fit, params, args = (xraw,yraw), method = 'leastsq')
    
    lmfit.report_errors(fit)
    
    a = fit.params['a'].value
    aerr = fit.params['a'].stderr
    b = fit.params['b'].value
    berr = fit.params['b'].stderr
    h = fit.params['h'].value
    herr = fit.params['h'].stderr
    k = fit.params['k'].value
    kerr = fit.params['k'].stderr
    theta = fit.params['theta'].value
    therr = fit.params['theta'].stderr
    
    #phir = arange(0, 2*pi, 0.01)
    #xfit = h + a*cos(phir)*cos(theta) -b*sin(phir)*sin(theta)
    #yfit = k + a*cos(phir)*sin(theta) + b*sin(phir)*cos(theta)
    
    #return xfit,yfit,h,herr,k,kerr,a,aerr,b,berr, theta, therr
    return h,herr,k,kerr,a,aerr,b,berr, theta, therr
    
def ringfit(xraw,yraw,xg,yg,rg):
            
    def circlefit(params,x,y):
        a = params['a'].value
        b=params['b'].value
        r=params['r'].value

        #function = (r - sqrt((x-a)**2 + (y-b)**2))**2# + a2*exp(-(x-b2)**2/(2*c2**2)) + d # + a3*exp(-(x-b3)**2/(2*c3**2))+d
        function = (r**2 - (x-a)**2 - (y-b)**2)
        resids = function
        #weighted = sqrt(resids**2/err**2)
        return resids

    params = lmfit.Parameters()
    params.add('a', value = xg)
    params.add('b', value = yg)
    params.add('r', value = rg)

    fit = lmfit.minimize(circlefit, params, args = (xraw,yraw), method = 'leastsq')

    lmfit.report_fit(fit)

    a = fit.params['a'].value
    aerr = fit.params['a'].stderr
    b = fit.params['b'].value
    berr = fit.params['b'].stderr
    r = fit.params['r'].value
    rerr = fit.params['r'].stderr

    phir = arange(-pi, pi, 0.01)
    xfit = r*cos(phir) + a
    yfit = r*sin(phir) + b

    return a,aerr,b,berr,r,rerr, xfit,yfit


def centerofthree(xs,ys):
    slope1 = (ys[1]-ys[0])/(xs[1]-xs[0])
    slope2 = (ys[2]-ys[1])/(xs[2]-xs[1])

    midx1 = (xs[1]+xs[0])/2
    midy1 = (ys[1]+ys[0])/2

    midx2 = (xs[2]+xs[1])/2
    midy2 = (ys[2]+ys[1])/2

    inv1 = -1/slope1
    inv2 = -1/slope2

    xar = arange(-18,18, 0.1)

    yyy1 = inv1*xar + (midy1-inv1*midx1)
    yyy2 = inv2*xar + (midy2-inv2*midx2)
    yyy = slope1*xar + (ys[0] - slope1*xs[0])

    var1 = array([[1, -inv1], [1, -inv2]])
    var2 = array([(midy1-inv1*midx1), (midy2-inv2*midx2)])

    ycentt = linalg.solve(var1,var2)[0]
    xcentt = linalg.solve(var1,var2)[1]

    radius_circ = sqrt((xs[0] - xcentt)**2 + (ys[0] - ycentt)**2)
    phi_range = arange(0,2*pi, 0.01)
    xcirc = radius_circ*sin(phi_range) + xcentt
    ycirc = radius_circ*cos(phi_range) + ycentt

    return xcentt, ycentt, xcirc, ycirc, radius_circ

def IQR(dist):
    return percentile(dist, 75) - percentile(dist, 25)

def project_phase(xdata, ydata, cent):
    phicoord = []
    rcoord = []
    for i in range(len(xdata)):
        if xdata[i] >= cent[0] and ydata[i] >=cent[1]:
            tank = (ydata[i] - cent[1])/(xdata[i] - cent[0])
            phicoord.append(atan(tank))
            rcoord.append(sqrt((ydata[i]-cent[1])**2 + (xdata[i] - cent[0])**2))
        if xdata[i] < cent[0] and ydata[i]>cent[1]:
            tank = (ydata[i] - cent[1])/(xdata[i] - cent[0])
            phicoord.append(atan(tank) + pi)
            rcoord.append(sqrt((ydata[i]-cent[1])**2 + (xdata[i] - cent[0])**2))
        if xdata[i] < cent[0] and ydata[i]<cent[1]:
            tank = (ydata[i] - cent[1])/(xdata[i] - cent[0])
            phicoord.append(atan(tank) + pi)
            rcoord.append(sqrt((ydata[i]-cent[1])**2 + (xdata[i] - cent[0])**2))
        if xdata[i] > cent[0] and ydata[i]<cent[1]:
            tank = (ydata[i] - cent[1])/(xdata[i] - cent[0])
            phicoord.append(atan(tank) + 2*pi)
            rcoord.append(sqrt((xdata[i]-cent[1])**2 + (ydata[i] - cent[0])**2))
 
    phicoord = array(phicoord)
    phicoord = phicoord* 180.0/pi
    
    return phicoord, rcoord

def radphase(xdata, ydata, cent):
    phicoord = []
    rcoord = []
    for i in range(len(xdata)):
        if xdata[i] >= cent[0] and ydata[i] >=cent[1]:
            tank = (ydata[i] - cent[1])/(xdata[i] - cent[0])
            phicoord.append(atan(tank))
            rcoord.append(sqrt((ydata[i]-cent[1])**2 + (xdata[i] - cent[0])**2))
        if xdata[i] < cent[0] and ydata[i]>cent[1]:
            tank = (ydata[i] - cent[1])/(xdata[i] - cent[0])
            phicoord.append(atan(tank) + pi)
            rcoord.append(sqrt((ydata[i]-cent[1])**2 + (xdata[i] - cent[0])**2))
        if xdata[i] < cent[0] and ydata[i]<cent[1]:
            tank = (ydata[i] - cent[1])/(xdata[i] - cent[0])
            phicoord.append(atan(tank) + pi)
            rcoord.append(sqrt((ydata[i]-cent[1])**2 + (xdata[i] - cent[0])**2))
        if xdata[i] > cent[0] and ydata[i]<cent[1]:
            tank = (ydata[i] - cent[1])/(xdata[i] - cent[0])
            phicoord.append(atan(tank) + 2*pi)
            rcoord.append(sqrt((xdata[i]-cent[1])**2 + (ydata[i] - cent[0])**2))

    rcoord = array(rcoord)
    phicoord = array(phicoord)
    df = pd.DataFrame(columns = ['r'])
    df['r'] = rcoord
    df['phi'] = phicoord *180/pi
    df['phirad'] = phicoord 
    
    return df

def plot2d(xpos, ypos):
    xedges = arange(-20,20,0.25)
    yedges = arange(-20,20, 0.25)
    
    #set_num = setnum[index]
    #stamp = start[index]
    
    H, xedges, yedges = histogram2d(xpos, ypos, bins = (xedges,yedges))
    H = rot90(H)
    H = flipud(H)
    ions = ma.masked_where(H == 0, H)
    
    plt.subplot(111, aspect = 'equal')
    plt.pcolormesh(xedges,yedges, ions, cmap = 'viridis')
    plt.xlabel('x [mm]')
    plt.ylabel('y [mm]')
    plt.grid()
    plt.xlim(-10,5)
    plt.ylim(-5,10)
    plt.show()
    
    return ions
    
def startstop(filename):
    temp = pd.read_csv(filename, nrows = 2, skiprows = arange(0,17), header = None)
    strtemp = str(temp[0])
    start = strtemp[17:42]  #was 41
    stop = strtemp[59:83]
    return start,stop


def cyclen(n, t, angle):
    frange = []
    nrange = arange(n-3,n+3)
    for i in range(len(nrange)):
        frange.append((angle + 2*pi*nrange[i])/(2*pi*t))
        
    return frange
