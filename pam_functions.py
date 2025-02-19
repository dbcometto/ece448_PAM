# This implements functions which create discrete pulse shapes for PAM
# Modified by Ben Cometto

import numpy as np

def pampt(sps, ptype, pparms=[]):
    if ptype == 'rect':
        nn = np.arange(sps)
        pt = np.ones(len(nn))
    elif ptype == 'rcf':
        nk = round(pparms[0]*sps)
        nn = np.arange(-nk,nk)
        pt = np.sinc(nn/float(sps))

        if len(pparms) > 1:
            p2t = 0.25*np.pi*np.ones(len(nn))
            atFB = pparms[1]/float(sps)*nn
            atFB2 = np.power(2*atFB,2.0)
            ix = np.where(atFB2 != 1)[0]
            p2t[ix] = np.cos(np.pi*atFB[ix])
            p2t[ix] = p2t[ix]/(1-atFB2[ix])
            pt = pt*p2t

    elif ptype == 'sinc':
        nk = round(pparms[0]*sps)
        nn = np.arange(-nk,nk)
        pt = np.sinc(nn/float(sps))

    elif ptype == 'ramp':
        nn = np.arange(-round(sps/2),round(sps/2))
        pt = nn


    else:
        pt = np.ones(1) # default value

    return pt

def pamhRt(sps, ptype, pparms=[]):
    pt = pampt(sps, ptype, pparms)
    hRt = pt[::-1] # h_R(t) = p(-t)
    hRt = 1.0/sum(np.power(pt,2.0))*hRt
    return hRt