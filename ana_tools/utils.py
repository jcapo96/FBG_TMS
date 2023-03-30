import numpy as np

def get_fwhm(sweep, peak, xdata, m, func):
    try:
        i1 = 0
        y = sweep["Data"][peak]
        while y > np.max(func(xdata, m.values["H"], m.values["A"], m.values["x0"], m.values["sigma"]))/2:
            y = sweep["Data"][peak+i1]
            i1 += 1
        i2 = 0
        y = sweep["Data"][peak]
        while y > np.max(func(xdata, m.values["H"], m.values["A"], m.values["x0"], m.values["sigma"]))/2:
            y = sweep["Data"][peak-i2]
            i2 += 1
        fwhm = (i1+i2) #in pm
        return fwhm
    except:
        fwhm = 9999
        return fwhm

def get_As(sweep, peak, xdata, m, func):
    try:
        a = 0
        y = sweep["Data"][peak]
        while y > np.max(func(xdata, m.values["H"], m.values["A"], m.values["x0"], m.values["sigma"]))/2:
            y = sweep["Data"][peak+a]
            a += 1
        b = 0
        y = sweep["Data"][peak]
        while y > np.max(func(xdata, m.values["H"], m.values["A"], m.values["x0"], m.values["sigma"]))/2:
            y = sweep["Data"][peak-b]
            b += 1
        as_50 = a/b
        a = 0
        y = sweep["Data"][peak]
        while y > np.max(func(xdata, m.values["H"], m.values["A"], m.values["x0"], m.values["sigma"]))*0.1:
            y = sweep["Data"][peak+a]
            a += 1
        b = 0
        y = sweep["Data"][peak]
        while y > np.max(func(xdata, m.values["H"], m.values["A"], m.values["x0"], m.values["sigma"]))*0.1:
            y = sweep["Data"][peak-b]
            b += 1
        as_10 = a/b
        As = as_50/as_10
        return As
    except:
        As = 9999
        return As