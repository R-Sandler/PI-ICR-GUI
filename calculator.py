import numpy as np
import math
import sys
import fnmatch

def Calculator(xs, xserr, ys, yserr, cluster_of_interest):

    xs[0]=xs[cluster_of_interest]
    xserr[0]=xserr[cluster_of_interest]
    ys[0]=ys[cluster_of_interest]
    yserr[0]=yserr[cluster_of_interest]

    radius = np.sqrt(np.square(xs[0]+1.94)+np.square(ys[0]-3.77))
    radius = round(radius, 3)
    radius_uncertainty = np.sqrt(np.square(xserr[0])+np.square(yserr[0]))
    radius_uncertainty = round(radius_uncertainty, 3)

    angle = math.atan2(3.77-ys[0],-1.94-xs[0])
    angle_uncertainty = 1/(np.square(3.77-ys[0])+np.square(-1.94-xs[0]))*np.sqrt(np.square(-1.94-xs[0])*np.square(0.05)+np.square(xs[0]+1.94)*np.square(yserr[0])+np.square(ys[0]-3.77)*np.square(0.05)+np.square(3.77-ys[0])*np.square(xserr[0]))
    angle = round(angle, 3)
    angle_uncertainty = round(angle_uncertainty, 3)

    return radius, radius_uncertainty, angle, angle_uncertainty
