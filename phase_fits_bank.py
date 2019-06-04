from numpy import*
import lmfit
import matplotlib.pyplot as plt
from lmfit.models import GaussianModel
from lmfit.models import SkewedGaussianModel
from lmfit.models import VoigtModel
from lmfit.models import QuadraticModel
from lmfit.models import ExponentialGaussianModel
from sklearn.cluster import MeanShift
#import probfit
#import iminuit
new_blue = '#3F5D7D'
##amefile = 'C:/Users/Rodney/Documents/cpt/mass_data/ame_all_masses.txt'
##
##
##def getfreq(A, element, q, *args):
##    ameN = genfromtxt(amefile, usecols = 0)
##    ameZ = genfromtxt(amefile, usecols = 1)
##    ameA = genfromtxt(amefile, usecols = 2)
##    ameEl = genfromtxt(amefile, usecols = 3, dtype = str)
##    mass = genfromtxt(amefile, usecols = 4)
##    mass_err = genfromtxt(amefile, usecols = 5)
##    length = len(args)
##    index = where((ameA == A) & (ameEl == element))
##    if length == 0:
##        mass_nuclide = mass[index][0]
##        mcs = mass[(where((ameA == 133) & (ameEl == 'Cs')))][0]
##        wcs = 657844.5
##        me = 548.579909
##        wc_nuclide = q*wcs * (mcs - me) / (mass_nuclide - q*me)
##        wplus_nuclide = wc_nuclide - 1593.0
##    if length > 0:
##        index2 = {}
##        mass_nuclide = mass[index][0]
##        for i in range(0,length/2):
##            index2['%i'%i] = where((ameA == args[0::2][i]) & (ameEl == args[1::2][i]))
##            mass_nuclide += mass[index2['%i'%i]][0]
##
##        mcs = mass[(where((ameA == 133) & (ameEl == 'Cs')))][0]
##        wcs = 657844.5
##        me = 548.579909
##        wc_nuclide = q*wcs * (mcs - me) / (mass_nuclide - q*me)
##        wplus_nuclide = wc_nuclide - 1593.0
##    return wc_nuclide, wplus_nuclide, mass_nuclide#, length


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
    
def twogauss_fit(data, xmin, xmax,numbins, bg,b2g,cg, *args):
    if len(args) == 1:
        tflag = args[0]
    if len(args) == 0:
        tflag = False
    clr = 'indianred'
    xbins = plt.hist(data, bins = numbins, range = (xmin,xmax), color = clr, histtype = 'stepfilled')
    xcenter = (xbins[1][:-1] + xbins[1][1:])/2.0
    def twogaussfit(params,x,y,err):
        a = params['a'].value
        b=params['b'].value
        c=params['c'].value
        d=params['d'].value

        a2=params['a2'].value
        b2=params['b2'].value
        c2=params['c2'].value

        function = a*exp(-(x-b)**2/(2*c**2)) + a2*exp(-(x-b2)**2/(2*c2**2)) + d # + a3*exp(-(x-b3)**2/(2*c3**2))+d
        resids = function-y
        weighted = sqrt(resids**2/err**2)
        return resids

    params = lmfit.Parameters()
    params.add('a', value = max(xbins[0]), vary = True)
    params.add('b', value = bg, vary = True)
    params.add('c', value = cg, vary = tflag)
    params.add('d', value = 0.00000001, vary = False)

    params.add('a2', value = max(xbins[0]), vary = True)
    params.add('b2', value =b2g, vary = True)
    params.add('c2', value = cg, vary = tflag)

    fit = lmfit.minimize(twogaussfit, params, args = (xcenter,xbins[0], sqrt(xbins[0])), method = 'leastsq')

    lmfit.report_errors(fit)

    a = fit.params['a'].value
    b = fit.params['b'].value
    berr = fit.params['b'].stderr
    c = fit.params['c'].value
    a2 = fit.params['a2'].value
    b2 = fit.params['b2'].value
    b2err = fit.params['b2'].stderr
    c2 = fit.params['c2'].value
    d = fit.params['d'].value

    xfit = arange(xmin,xmax,0.1)
    yfit = a*exp(-(xfit-b)**2/(2*c**2))+ a2*exp(-(xfit-b2)**2/(2*c2**2)) + d # + a3*exp(-(xfit-b3)**2/(2*c3**2))+d
    y1 = a*exp(-(xfit - b)**2/(2*c**2)) + d
    y2 = a2*exp(-(xfit-b2)**2/(2*c2**2)) + d    
    #plt.plot(xfit,yfit,'b-')
    #plt.plot(xfit,y1, 'r-')
    #plt.plot(xfit,y2, 'r-')
    
    return b, berr, b2, b2err

def threegauss_fit(data, xmin, xmax,numbins, bg,b2g,b3g, cg, *args):
    if len(args) == 1:
        tflag = args[0]
    if len(args) == 0:
        tflag = False
    clr = 'indianred'
    xbins = plt.hist(data, bins = numbins, range = (xmin,xmax), color = clr, histtype = 'stepfilled')
    xcenter = (xbins[1][:-1] + xbins[1][1:])/2.0
    def threegaussfit(params,x,y,err):
        a = params['a'].value
        b=params['b'].value
        c=params['c'].value
        d=params['d'].value

        a2=params['a2'].value
        b2=params['b2'].value
        c2=params['c2'].value

        a3=params['a3'].value
        b3=params['b3'].value
        c3=params['c3'].value
        
        function = a*exp(-(x-b)**2/(2*c**2)) + a2*exp(-(x-b2)**2/(2*c2**2)) + a3*exp(-(x-b3)**2/(2*c3**2)) +d
        resids = function-y
        weighted = sqrt(resids**2/err**2)
        return resids

    params = lmfit.Parameters()
    params.add('a', value = max(xbins[0]), vary = True)
    params.add('b', value = bg, vary = True)
    params.add('c', value = cg, vary = tflag)
    params.add('d', value = 0.00000001, vary = False)

    params.add('a2', value = max(xbins[0]), vary = True)
    params.add('b2', value =b2g, vary = True)
    params.add('c2', value = cg, vary = tflag)

    params.add('a3', value = max(xbins[0]), vary = True)
    params.add('b3', value = b3g, vary = True)
    params.add('c3', value = cg, vary = tflag)
    
    fit = lmfit.minimize(threegaussfit, params, args = (xcenter,xbins[0], sqrt(xbins[0])), method = 'leastsq')

    lmfit.report_errors(fit)

    a = fit.params['a'].value
    b = fit.params['b'].value
    berr = fit.params['b'].stderr
    c = fit.params['c'].value
    a2 = fit.params['a2'].value
    b2 = fit.params['b2'].value
    b2err = fit.params['b2'].stderr
    c2 = fit.params['c2'].value
    a3 = fit.params['a3'].value
    b3 = fit.params['b3'].value
    b3err = fit.params['b3'].stderr
    c3 = fit.params['c3'].value
    d = fit.params['d'].value

    xfit = arange(xmin,xmax,0.1)
    yfit = a*exp(-(xfit-b)**2/(2*c**2))+ a2*exp(-(xfit-b2)**2/(2*c2**2)) + a3*exp(-(xfit-b3)**2/(2*c3**2)) + d
    y1 = a*exp(-(xfit - b)**2/(2*c**2)) + d
    y2 = a2*exp(-(xfit-b2)**2/(2*c2**2)) + d    
    y3 = a3*exp(-(xfit-b3)**2/(2*c3**2)) + d    
    #plt.plot(xfit,yfit,'b-')
    #plt.plot(xfit,y1, 'r-')
    #plt.plot(xfit,y2, 'r-')
    #plt.plot(xfit, y3, 'r-')
    
    bs = array([b, b2, b3])
    berrs = array([berr, b2err, b3err])
    
    return bs, berrs 

def skewedgauss(xmin,xmax,data,numbin, clr):
    xbins = plt.hist(data, bins = numbin, range = (xmin,xmax), alpha = 0.6, color = clr, histtype = 'stepfilled')
    xcenter = (xbins[1][:-1] + xbins[1][1:])/2.0
    mod = SkewedGaussianModel()
    pars = mod.guess(xbins[0], x = xcenter)
    fit = mod.fit(xbins[0], x = xcenter, params = pars, method = 'leastsq')
    print (fit.fit_report())
    xfit = arange(xmin,xmax, 0.01)
    plt.plot(xfit, fit.eval(x=xfit), 'r-')
    return fit.params['center'].value, fit.params['center'].stderr

def twodgaussfit(xe,ye,M,xg,yg):
    xcenter = (xe[:-1] + xe[1:])/2.0
    ycenter = (ye[:-1] + ye[1:])/2.0
    xygrid = meshgrid(xcenter, ycenter)

    zd = M.flatten()
    xd = xygrid[0].flatten()
    yd = xygrid[1].flatten()

    nons = nonzero(zd>1)
    xnon = xd[nons]
    ynon = yd[nons]
    znon = zd[nons]
    def twodgauss(params, x,y,z,err):
        A = params['A'].value
        xo = params['xo'].value
        yo = params['yo'].value
        sx = params['sx'].value
        sy = params['sy'].value

        function = A*exp(-((x-xo)**2/(2*sx**2) + (y-yo)**2/(2*sy**2)))
        resids = function - z
        weighted = sqrt(resids**2/err**2)
        return weighted

    params = lmfit.Parameters()
    params.add('A', value = max(znon))
    params.add('xo', value = xg)
    params.add('yo', value = yg)
    params.add('sx', value = 1.0)
    params.add('sy', value = 1.0)

    fit = lmfit.minimize(twodgauss, params, args = (xnon,ynon,znon, sqrt(znon)), method = 'leastsq')
    lmfit.report_fit(fit)

    xo = fit.params['xo'].value
    xerr = fit.params['xo'].stderr
    yo = fit.params['yo'].value
    yerr = fit.params['yo'].stderr
    sx = fit.params['sx'].value
    sy = fit.params['sy'].value

    return xo, xerr, yo, yerr, sx, sy

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

##
##    ax = plt.subplot(111, aspect = 'equal')
##    plt.xlim(-13,7)
##    plt.ylim(-6,14)
##    colors = ['blue', 'salmon', 'darkorange', 'cadetblue', 'sage', 'yellow', 'green', 'black', 'cyan', 'indianred', 'chartreuse', 'seagreen', 'purple', 'aliceblue']
##    #for i in range(len(X)):
##    #    plt.plot(X[i][0], X[i][1], 'o', color = colors[labels[i]])
##    for k, col in zip(unique(labels), colors):
##        my = labels == k
##        plt.plot(X[my,0], X[my,1], 'o', color = colors[k])
##    for i in range(0,n_clusters_):
##        plt.text(-12,10 - i,'%s: %.1f%%'%(colors[i],100.0*ips[i]/sum(ips)))
##    plt.text(-12,12, 'total:%i'%sum(ips))
##    plt.plot(cluster_center[:,0], cluster_center[:,1], 'p', markersize=10, color = 'black')
##    plt.show()

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
##        plt.title('xbins = %i and ybins = %i'%(numbins(xcut), numbins(ycut)))
##    plt.show()

#    df = pd.DataFrame(columns = ['x'])
#    df['x'] = X[labels>-1][:,0]
#    df['y'] = X[labels >-1][:,1]
#    df['tof'] = tofraw['0'][labels>-1]
#    df['trig'] = trigger['0'][labels>-1]
#    df['id'] = labels[labels > -1]
    xkeep, ykeep = [],[]
    for i in range(len(labels)):
        if labels[i] > -1:
            xkeep.append(X[i][0])
            ykeep.append(X[i][1])
    return xs, xserr, ys, yserr, ips, xkeep, ykeep, X, n_clusters_, labels, cluster_center



def cluster_spots_new(xdata,ydata, radius, *args):
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

##    
    ax = plt.subplot(111, aspect = 'equal')
    plt.xlim(-13,7)
    plt.ylim(-6,14)
    colors = ['blue', 'salmon', 'darkorange', 'cadetblue', 'sage', 'yellow', 'green', 'black', 'cyan', 'indianred', 'chartreuse', 'seagreen', 'purple', 'aliceblue']
    #for i in range(len(X)):
    #    plt.plot(X[i][0], X[i][1], 'o', color = colors[labels[i]])
    for k, col in zip(unique(labels), colors):
        my = labels == k
        plt.plot(X[my,0], X[my,1], 'o', color = colors[k])
    for i in range(0,n_clusters_):
        plt.text(-12,10 - i,'%s: %.1f%%'%(colors[i],100.0*ips[i]/sum(ips)))
    plt.text(-12,12, 'total:%i'%sum(ips))
    plt.plot(cluster_center[:,0], cluster_center[:,1], 'p', markersize=10, color = 'black')
    plt.show()

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
        
    def newfit(data):
        def gauss_pdf(x, mu, sigma, A):
            return A / (sqrt(2*pi) * sigma) * exp(-(x - mu) **2 / (2. *sigma ** 2))
            
        
        chix = probfit.BinnedChi2(gauss_pdf, data,  bins = numbins(data), bound = (min(data),max(data)))
        
        dd = plt.hist(data, bins = numbins(data), color = 'seagreen', histtype = 'stepfilled')
        ddcent = (dd[1][:-1] + dd[1][1:])/2.0
        mod = GaussianModel()
        pars = mod.guess(dd[0], x = ddcent)
        
        
        parsx = {"mu":pars['center'].value,"sigma":pars['sigma'].value, "A": 1000}
        minuit = iminuit.Minuit(chix, pedantic=False, print_level=0, **parsx)
        #plt.hist(data, bins = numbins(data), histtype = 'stepfilled')        
        minuit.migrad()
        chix.draw(minuit)
        
        return minuit
    
    for i in range(0,len(clust_ind)):
        xcut = []
        ycut = []
        for j in range(len(labels)):
            if labels[j] == clust_ind[i]:
                xcut.append(xdata[j])
                ycut.append(ydata[j])
        widthx = max(xcut) - min(xcut)
        widthy = max(ycut) - min(ycut)
        #xfit = gaussmodel(min(xcut)-0.1*widthx, max(xcut)+0.1*widthx, xcut, numbins(xcut), 'cadetblue')
        plt.subplot(121)        
        xfit = newfit(xcut)
        plt.subplot(122)
        yfit = newfit(ycut)       
        #yfit = gaussmodel(min(ycut)-0.1*widthy, max(ycut)+0.1*widthy, ycut, numbins(ycut), 'darkorange')
        xs.append(xfit.values['mu'])
        xserr.append(xfit.errors['mu'])
        ys.append(yfit.values['mu'])
        yserr.append(yfit.errors['mu'])
        ips.append(len(xcut))
        plt.title('xbins = %i and ybins = %i'%(numbins(xcut), numbins(ycut)))
        #plt.show()
    plt.show()

#    df = pd.DataFrame(columns = ['x'])
#    df['x'] = X[labels>-1][:,0]
#    df['y'] = X[labels >-1][:,1]
#    df['tof'] = tofraw['0'][labels>-1]
#    df['trig'] = trigger['0'][labels>-1]
#    df['id'] = labels[labels > -1]
    xkeep, ykeep = [],[]
    for i in range(len(labels)):
        if labels[i] > -1:
            xkeep.append(X[i][0])
            ykeep.append(X[i][1])
    return xs, xserr, ys, yserr, ips, xkeep, ykeep

##def vector(xdata, ydata, center, center_err, radius = 0.7, density = 5.0):
##    cent = center
##    centerr = center_err
##    clust = cluster_spots_new(xdata, ydata, radius, density)
##    vector = array([clust[0][0] - cent[0], clust[2][0] - cent[1]])
##    vector_err = array([sqrt(clust[1][0]**2 + centerr[0]**2), sqrt(clust[3][0]**2 + centerr[1]**2)])
##
##    return vector, vector_err
