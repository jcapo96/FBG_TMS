import numpy as np
import pandas as pd
import getters

def get_offsets(data):
    timestamp = data["Timestamp"]
    data = data.sort_values(by="Timestamp").reset_index(drop=True)
    data=data.apply(lambda x: x*1e9 - 5*np.round(x[0]*1e9/5,0))
    offsets = {}
    for ref in data.columns:
        if "Timestamp" in ref:
            continue
        doff = data.sub(data[ref], axis=0)
        doff["Timestamp"] = timestamp
        offsets[ref] = doff
    return offsets

def cut_plat(data,plateaus,date):  #function to cut data in the plateaus 
    dplat={}
    for plateau in plateaus[date]:
        ti=plateaus[date][plateau][0]
        tf=plateaus[date][plateau][1]
        dplat[plateau]=data.loc[(data["Timestamp"]-np.min(data["Timestamp"])>ti)&(data["Timestamp"]-np.min(data["Timestamp"])<tf)].reset_index(drop=True)
    return dplat

def offsets_plat(date,data):
    offset_p={}
    plateaus = getters.get_plateaus()
    peaks_cut = cut_plat(data,plateaus,date)
    for plateau in plateaus[date]:
        offset_p[plateau]=get_offsets(peaks_cut[plateau])
    return offset_p