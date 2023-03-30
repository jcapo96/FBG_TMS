import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

path_folder_data = "/eos/user/j/jcapotor/FBGdata/Data/HeatTests/"

data_o11 = pd.read_csv(path_folder_data + "07122022_air_fbg_wl_3.txt", sep="\t", header=None)
data_rtd = pd.read_csv(path_folder_data + "07122022_air_rtd_3.txt", sep="\t", header=None)
data_fbgs = pd.read_csv(path_folder_data + "20221202_air_fbg-ILLumiSense-Wav-CH1.txt", sep="\t", skiprows=20, header=None)
print(data_fbgs)

def time_to_sec_o11(column):
    time_sec = []
    for ev in column:
        time = ev.split(" ")[1]
        time = time.split(":")
        h, m, s = time[0], time[1], time[2]
        totalseconds = float(h)*3600 + float(m)*60 + float(s)
        time_sec.append(np.round(totalseconds, 0))
    return time_sec

def time_to_sec_rtd(column):
    time_sec = []
    for ev in column:
        time = ev.split(":")
        h, m, s = time[0], time[1], time[2]
        totalseconds = float(h)*3600 + float(m)*60 + float(s)
        time_sec.append(totalseconds)
    return time_sec

data_rtd[1] = time_to_sec_rtd(data_rtd[1])
data_o11[0] = time_to_sec_o11(data_o11[0])
data_fbgs[1] = time_to_sec_rtd(data_fbgs[1])

def average_data(df, ref, col1, col2, col3, col4):
    rows = []
    for time in df[ref].unique():
        df2 = df[df[ref]==time]
        mean_s1 = np.average(df2[col1])
        mean_s2 = np.average(df2[col2])
        mean_s3 = np.average(df2[col3])
        mean_s4 = np.average(df2[col4])
        error_s1 = np.std(df2[col1])
        rows.append([time, mean_s1, mean_s2, mean_s3, mean_s4, error_s1])
    df3 = pd.DataFrame(rows)
    return df3

data_o11 = average_data(data_o11, 0, 8, 14, 20, 26)
data_rtd = average_data(data_rtd, 1, 2, 3, 2, 3)

def cut_time(df1, df2):
    min_t1 = np.min(df1[0])
    min_t2 = np.min(df2[0])
    max_t1 = np.max(df1[0])
    max_t2 = np.max(df2[0])

    min_time = max(min_t1, min_t2)
    max_time = min(max_t1, max_t2)

    df1 = df1[(df1[0]>=min_time) & (df1[0]<max_time)]
    df2 = df2[(df2[0]>=min_time) & (df2[0]<max_time)]

    return df1, df2

data_rtd, data_o11 = cut_time(data_rtd, data_o11)

def linear(xdata, a, b):
    return a + b*xdata

plt.figure()
plt.suptitle("Sensitivity plot")
plt.subplot(2,2,1)
plt.title("Sensor 1 (2m)")
plt.scatter(data_rtd[1], data_o11[1]*1E12 - data_o11[1][0]*1E12)
popt, pcov = curve_fit(linear, data_rtd[1][500:], (data_o11[1]*1E12 - data_o11[1][0]*1E12)[500:])
plt.plot(data_rtd[1][500:], linear(data_rtd[1][500:], popt[0], popt[1]), color="red", label=str(np.round(popt[1], 2)) + " pm/K")
popt, pcov = curve_fit(linear, data_rtd[1][100:350], (data_o11[1]*1E12 - data_o11[1][0]*1E12)[100:350])
plt.plot(data_rtd[1][100:350], linear(data_rtd[1][100:350], popt[0], popt[1]), color="green", label=str(np.round(popt[1], 2)) + " pm/K")
plt.ylabel("Wavelength diff (pm)")
plt.grid("on")
plt.legend()
plt.subplot(2,2,2)
plt.title("Sensor 2 (2.5m)")
plt.scatter(data_rtd[1], data_o11[2]*1E12 - data_o11[2][0]*1E12)
popt, pcov = curve_fit(linear, data_rtd[1][500:], (data_o11[2]*1E12 - data_o11[2][0]*1E12)[500:])
plt.plot(data_rtd[1][500:], linear(data_rtd[1][500:], popt[0], popt[1]), color="red", label=str(np.round(popt[1], 2)) + " pm/K")
popt, pcov = curve_fit(linear, data_rtd[1][100:350], (data_o11[2]*1E12 - data_o11[2][0]*1E12)[100:350])
plt.plot(data_rtd[1][100:350], linear(data_rtd[1][100:350], popt[0], popt[1]), color="green", label=str(np.round(popt[1], 2)) + " pm/K")
plt.ylabel("Wavelength diff (pm)")
plt.grid("on")
plt.legend()
plt.subplot(2,2,3)
plt.title("Sensor 3 (3m)")
plt.scatter(data_rtd[1], data_o11[3]*1E12 - data_o11[3][0]*1E12)
popt, pcov = curve_fit(linear, data_rtd[1][500:], (data_o11[3]*1E12 - data_o11[3][0]*1E12)[500:])
plt.plot(data_rtd[1][500:], linear(data_rtd[1][500:], popt[0], popt[1]), color="red", label=str(np.round(popt[1], 2)) + " pm/K")
popt, pcov = curve_fit(linear, data_rtd[1][100:350], (data_o11[3]*1E12 - data_o11[3][0]*1E12)[100:350])
plt.plot(data_rtd[1][100:350], linear(data_rtd[1][100:350], popt[0], popt[1]), color="green", label=str(np.round(popt[1], 2)) + " pm/K")
plt.xlabel("Temperature (K)")
plt.ylabel("Wavelength diff (pm)")
plt.grid("on")
plt.legend()
plt.subplot(2,2,4)
plt.title("Sensor 4 (3.5m)")
plt.scatter(data_rtd[1], data_o11[4]*1E12 - data_o11[4][0]*1E12)
popt, pcov = curve_fit(linear, data_rtd[1][500:], (data_o11[4]*1E12 - data_o11[4][0]*1E12)[500:])
plt.plot(data_rtd[1][500:], linear(data_rtd[1][500:], popt[0], popt[1]), color="red", label=str(np.round(popt[1], 2)) + " pm/K")
popt, pcov = curve_fit(linear, data_rtd[1][100:350], (data_o11[4]*1E12 - data_o11[4][0]*1E12)[100:350])
plt.plot(data_rtd[1][100:350], linear(data_rtd[1][100:350], popt[0], popt[1]), color="green", label=str(np.round(popt[1], 2)) + " pm/K")
plt.xlabel("Temperature (K)")
plt.ylabel("Wavelength diff (pm)")
plt.grid("on")
plt.legend()

plt.figure()
plt.suptitle("Temperature Resolution (mK)")
plt.subplot(2,2,1)
plt.title("Wavelength diff")
plt.scatter((data_o11[1]*1E12 - data_o11[1][0]*1E12)[500:], (data_o11[2]*1E12 - data_o11[2][0]*1E12)[500:])
plt.scatter((data_o11[1]*1E12 - data_o11[1][0]*1E12)[500:], (data_o11[3]*1E12 - data_o11[3][0]*1E12)[500:])
plt.scatter((data_o11[1]*1E12 - data_o11[1][0]*1E12)[500:], (data_o11[4]*1E12 - data_o11[4][0]*1E12)[500:])
plt.xlabel("Wavelength diff (pm)")
plt.ylabel("Wavelength diff (pm)")
plt.subplot(2,2,2)
plt.title("S1-S2 vs Time")
minimum = min((data_o11[1]*1E12 - data_o11[1][0]*1E12)[500:] - (data_o11[2]*1E12 - data_o11[2][0]*1E12)[500:] - ((data_o11[1]*1E12 - data_o11[1][0]*1E12)[500:] - (data_o11[2]*1E12 - data_o11[2][0]*1E12))[500])
maximum = max((data_o11[1]*1E12 - data_o11[1][0]*1E12)[500:] - (data_o11[2]*1E12 - data_o11[2][0]*1E12)[500:] - ((data_o11[1]*1E12 - data_o11[1][0]*1E12)[500:] - (data_o11[2]*1E12 - data_o11[2][0]*1E12))[500])
deltaT = (maximum - minimum)/popt[1]*1000
plt.scatter(data_rtd[0][500:], (data_o11[1]*1E12 - data_o11[1][0]*1E12)[500:] - (data_o11[2]*1E12 - data_o11[2][0]*1E12)[500:] - ((data_o11[1]*1E12 - data_o11[1][0]*1E12)[500:] - (data_o11[2]*1E12 - data_o11[2][0]*1E12))[500],
            label = str(np.round(deltaT, 1)) + str(" mK"))
plt.ylabel("Wavelength diff: s1 - s2 (pm)")
plt.xlabel("Abs. Time (s)")
plt.legend()
plt.subplot(2,2,3)
minimum = min((data_o11[1]*1E12 - data_o11[1][0]*1E12)[500:] - (data_o11[3]*1E12 - data_o11[3][0]*1E12)[500:] - ((data_o11[1]*1E12 - data_o11[1][0]*1E12)[500:] - (data_o11[3]*1E12 - data_o11[3][0]*1E12))[500])
maximum = max((data_o11[1]*1E12 - data_o11[1][0]*1E12)[500:] - (data_o11[3]*1E12 - data_o11[3][0]*1E12)[500:] - ((data_o11[1]*1E12 - data_o11[1][0]*1E12)[500:] - (data_o11[3]*1E12 - data_o11[3][0]*1E12))[500])
deltaT = (maximum - minimum)/popt[1]*1000
plt.scatter(data_rtd[0][500:], (data_o11[1]*1E12 - data_o11[1][0]*1E12)[500:] - (data_o11[3]*1E12 - data_o11[3][0]*1E12)[500:] - ((data_o11[1]*1E12 - data_o11[1][0]*1E12)[500:] - (data_o11[3]*1E12 - data_o11[3][0]*1E12))[500],
            label = str(np.round(deltaT, 1)) + str(" mK"))
plt.ylabel("Wavelength diff: s1 - s3 (pm)")
plt.xlabel("Abs. Time (s)")
plt.legend()
plt.subplot(2,2,4)
minimum = min((data_o11[1]*1E12 - data_o11[1][0]*1E12)[500:] - (data_o11[4]*1E12 - data_o11[4][0]*1E12)[500:] - ((data_o11[1]*1E12 - data_o11[1][0]*1E12)[500:] - (data_o11[4]*1E12 - data_o11[4][0]*1E12))[500])
maximum = max((data_o11[1]*1E12 - data_o11[1][0]*1E12)[500:] - (data_o11[4]*1E12 - data_o11[4][0]*1E12)[500:] - ((data_o11[1]*1E12 - data_o11[1][0]*1E12)[500:] - (data_o11[4]*1E12 - data_o11[4][0]*1E12))[500])
deltaT = (maximum - minimum)/popt[1]*1000
plt.scatter(data_rtd[0][500:], (data_o11[1]*1E12 - data_o11[1][0]*1E12)[500:] - (data_o11[4]*1E12 - data_o11[4][0]*1E12)[500:] - ((data_o11[1]*1E12 - data_o11[1][0]*1E12)[500:] - (data_o11[4]*1E12 - data_o11[4][0]*1E12))[500],
            label = str(np.round(deltaT, 1)) + str(" mK"))
plt.ylabel("Wavelength diff: s1 - s4 (pm)")
plt.xlabel("Abs. Time (s)")
plt.legend()
plt.show(block=True)