import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import getters
from tabulate import tabulate

path_to_split = "/eos/user/j/jcapotor/FBGana/camara_climatica/FebruaryRuns/"

def line(x, A, B):
    return A + B*x

def get_residuals(data, col, t0):
    popt, pcov = curve_fit(line, xdata=data["Timestamp"]-t0, ydata=data[col])
    res = data[col] - line(data["Timestamp"]-t0, popt[0], popt[1])
    mean_res = np.mean(res)
    rms_res = np.std(res)
    return mean_res, rms_res, popt

plateaus = {
    "20230221":{"273_down":[10000,12300], "253_down":[22000,24300], "233_down":[34000,36300], "213_down":[45000,52000], "233_up":[61000,64000], "253_up":[73000,76000], "273_up":[85000,88000]},
    "20230222":{"273_down":[14000,19800], "253_down":[34000,39000], "233_down":[53000,58200], "213_down":[68000,77300]},
    "20230223":{"253_down":[12500,24000], "213_down":[34000,48000]},
    "20230224":{"293_down":[11900,15900], "283_down":[27750,31750], "273_down":[43650,47650], "263_down":[59550,63550], "253_down":[75450,79450], "243_down":[91350,95350],
    "233_down":[106450,110450], "223_down":[122350,126350], "213_down":[138250,142250], "223_up":[154150,158150], "233_up":[170050,174050], "243_up":[186000,190000],
    "253_up":[201900,205900], "263_up":[217800,221800], "273_up":[233700,237700]}
}

date = "20230223"
temp = pd.read_csv(path_to_split+date+"/temperature.txt", header=0)
peaks_p = getters.get_data(path_to_split+date+"/", pol="P")
peaks_s = getters.get_data(path_to_split+date+"/", pol="S")
t0 = temp["Timestamp"][0]

for plateau in plateaus[date].keys():
    print(plateau)
    temp_table = [
        ["T0 (K)"],
        ["Tf (K)"],
        ["dT (K)"],
        ["t0 (s)"],
        ["tf (s)"],
        ["dt (s)"],
        ["Slope (mK/s)"],
        ["Res. (mK)"]
    ]
    temp_header = ["Names"]
    sens = "Wav1-1"
    temp_plateau = temp.loc[(temp["Timestamp"]-t0 > plateaus[date][plateau][0]) & (temp["Timestamp"]-t0 < plateaus[date][plateau][1])].reset_index(drop=True)
    for rtd in temp_plateau.columns:
        if rtd[0] != "T" or rtd == "Timestamp" or rtd[-1]=="r":
            continue
        T0 = temp_plateau[rtd].iloc[0]
        Tf = temp_plateau[rtd].iloc[-1]
        tini = temp_plateau["Timestamp"].iloc[0] - t0
        tfin = temp_plateau["Timestamp"].iloc[-1] - t0

        deltaT = (Tf-T0)
        deltat = (tfin-tini)
        temp_table[0].append(T0)
        temp_table[1].append(Tf)
        temp_table[2].append(np.round(deltaT, 3))
        temp_table[3].append(tini)
        temp_table[4].append(tfin)
        temp_table[5].append(np.round(deltat, 0))

        mean_resT, rms_resT, poptT = get_residuals(temp_plateau, rtd, t0)
        temp_table[6].append(np.round(poptT[1]*1e3, 3))
        temp_table[7].append(np.round(rms_resT*1e3, 1))
        temp_header.append(rtd)
    print(tabulate(temp_table, temp_header, "grid"))
    wl_table = [
        ["WL0 - P (pm)"],
        ["WL0 - S (pm)"],
        ["WLf - P (pm)"],
        ["WLf - S (pm)"],
        ["dWL - P (pm)"],
        ["dWL - S (pm)"],
        ["Slope - P (fm/s)"],
        ["Slope - S (fm/s)"],
        ["Res. - P (fm)"],
        ["Res. - S (fm)"],
        ["Sensitivity. - S (pm/K)"],
        ["Sensitivity. - S (pm/K)"]
    ]
    wl_header = ["Names"]
    pp_plateau = peaks_p.loc[(peaks_p["Timestamp"]-t0 > plateaus[date][plateau][0]) & (peaks_p["Timestamp"]-t0 < plateaus[date][plateau][1])]
    ps_plateau = peaks_p.loc[(peaks_s["Timestamp"]-t0 > plateaus[date][plateau][0]) & (peaks_s["Timestamp"]-t0 < plateaus[date][plateau][1])]
    for sens in pp_plateau.columns:
        if sens[0] != "W" or sens[-1]=="r":
            continue
        pp0 = pp_plateau[sens].iloc[0]
        ppf = pp_plateau[sens].iloc[-1]
        ps0 = ps_plateau[sens].iloc[0]
        psf = ps_plateau[sens].iloc[-1]
        deltapp = (pp0-ppf)
        deltaps = (ps0-psf)
        wl_table[0].append(pp0*1e12)
        wl_table[1].append(ps0*1e12)
        wl_table[2].append(ppf*1e12)
        wl_table[3].append(psf*1e12)
        wl_table[4].append(deltapp*1e12)
        wl_table[5].append(deltaps*1e12)
        mean_respp, rms_respp, poptpp = get_residuals(pp_plateau, sens, t0)
        mean_resps, rms_resps, poptps = get_residuals(ps_plateau, sens, t0)
        wl_table[6].append(poptpp[1]*1e15)
        wl_table[7].append(poptps[1]*1e15)
        wl_table[8].append(rms_respp*1e15)
        wl_table[9].append(rms_resps*1e15)
        sensitivitypp = []
        sensitivityps = []
        for value in temp_table[6]:
            if value == "Slope (mK/s)":
                continue
            value = float(value)
            sensitivitypp.append(poptpp[1]*1e12/value*1e3)
            sensitivityps.append(poptps[1]*1e12/value*1e3)
        wl_table[10].append(np.mean(sensitivitypp))
        wl_table[11].append(np.mean(sensitivityps))
        wl_header.append(sens)
    print(tabulate(wl_table, wl_header, "grid"))
