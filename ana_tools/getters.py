import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import h5py
from tqdm import tqdm

def get_raw_data(
    path_to_split="",
    filetype = "peaks",
    pol="Av"
    ):
    cnt = 0
    f = h5py.File(path_to_split+filetype+".h5", "r")
    keys = list(f.keys())
    list_of_keys = []
    joint_data = pd.DataFrame()
    for key in keys:
        if pol in key:
            list_of_keys.append(key)
    print("Keys to read: " + str(list_of_keys))
    progress_bar = tqdm(total=len((list_of_keys)), desc="Reading " + filetype + " key: " + pol)
    for key in list_of_keys:
        data = pd.read_hdf(path_to_split+filetype+".h5", key=key)
        joint_data = pd.concat([joint_data, data], ignore_index=True, axis=0, keys=data)
        progress_bar.update(1)
    progress_bar.close()
    return joint_data

def get_processed_data(
    path_to_split=""
):
    data = pd.read_hdf(path_to_split+"matched.h5", key="data")
    return data

def spectra(s, nu, L):
    k = s*nu/2
    num = (np.sinh(L*np.sqrt(s**2 - k**2)))**2
    den = (np.cosh(L*np.sqrt(s**2 - k**2)))**2 - (s**2)/(k**2)
    return num/den

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