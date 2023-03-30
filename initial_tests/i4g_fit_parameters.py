import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from tabulate import tabulate
import seaborn as sns

def time_to_seconds(x):
    time = x.split(" ")[1]
    time = time.split(":")
    h, m, s = time[0], time[1], time[2]
    totalseconds = float(h)*3600 + float(m)*60 + float(s)
    return totalseconds

def gaussian(x, amp, cen, wid):
    return amp * np.exp(-(x-cen)**2 / wid)

def get_fit_parameters(df):
    wl_data = []
    amplitude_data = []
    for point in df["Wavelength Axis (nm)"][0][11000:11100]:
        wl_data.append(float(point[0]))
    for point in df["Spectral data"][0][11000:11100]:
        amplitude_data.append(point)
    init_vals = [4000., 1540., 0.1]  # for [amp, cen, wid]
    parameters, covariance = curve_fit(gaussian, wl_data, amplitude_data, p0=init_vals)
    return parameters

def read_logile():
    logfile = pd.read_csv("/eos/user/j/jcapotor/FBGdata/Data/12012023_datosRepetitividadLatiguillo/Log.txt", skiprows=78, header=None, sep="\t")
    del logfile[2], logfile[4], logfile[6], logfile[7]
    names = ["Run", "FitPoints", "WidthThres", "RoundTrip", "DownSampling"]
    logfile.columns = names
    return logfile

def read_peaks(filename):
    data = pd.read_csv(filename, sep="\t", header=None)
    data[0] = data[0].apply(time_to_seconds)
    s_pol = data[8].iloc[::2]
    p_pol = data[8].iloc[1::2]
    return s_pol, p_pol

def read_spectrums(filename, run):
    FileId=open(filename,'rb')#open file to be read
    sweeps = []
    persistentRead = True
    cnt = 0
    while persistentRead == True:
        try:
            sweep = {}
            sweep['PacketSize'] = (np.fromfile(FileId, dtype='<i4', count=1))
            sweep['Timestamp'] = (np.fromfile(FileId, dtype='<u8', count=1))
            sweep['Validity flag'] = (np.fromfile(FileId, dtype='<i4', count=1))
            sweep['Channel No.'] = (np.fromfile(FileId, dtype='<i4', count=1))
            sweep['Fibre No.'] = (np.fromfile(FileId, dtype='<i4', count=1))
            sweep['Start wavelength'] = (np.fromfile(FileId, dtype='<d', count=1))
            sweep['Stop wavelength'] = (np.fromfile(FileId, dtype='<d', count=1))
            sweep['No. of wavelength points']=(np.fromfile(FileId, dtype='<i4', count=1))
            sweep['Spectral data']=(np.fromfile(FileId, dtype='<i2', count=sweep['No. of wavelength points'][0]))
            sweep['Wavelength Axis (nm)']=np.linspace(sweep['Start wavelength'],sweep['Stop wavelength'],int(sweep['No. of wavelength points']))
            if sweep["Channel No."] != 0:
                continue
            else:
                if run == 3 or run == 4 or run==7 or run==11 or run==13 or run==14 or run==15 or run==16:
                    if cnt % 2 == 1:
                        cnt += 1
                        continue
                    else:
                        sweeps.append(sweep)
                        cnt += 1
                else:
                    if cnt % 2 == 0:
                        cnt += 1
                        continue
                    else:
                        sweeps.append(sweep)
                        cnt += 1
        except:
            persistentRead = False
    sweeps = pd.DataFrame(sweeps)
    return sweeps

def get_table():
    logfile = read_logile()
    print(tabulate(logfile, headers = 'keys', tablefmt = 'psql'))
    ppol_ref, spol_ref = np.mean(read_peaks("/eos/user/j/jcapotor/FBGdata/Data/12012023_datosRepetitividadLatiguillo/Run1_peaks.txt"), axis=1)
    ppol_ref_err, spol_ref_err = np.std(read_peaks("/eos/user/j/jcapotor/FBGdata/Data/12012023_datosRepetitividadLatiguillo/Run1_peaks.txt"), axis=1)
    results = []
    for index, row in logfile.iterrows():
        peaks = read_peaks("/eos/user/j/jcapotor/FBGdata/Data/12012023_datosRepetitividadLatiguillo/Run"+str(row["Run"])+"_peaks.txt")
        file_results = {}
        file_results["Run"] = row["Run"]
        file_results["ppol"]=np.mean(peaks[0] - ppol_ref)
        file_results["ppol_err"]=np.std(peaks[0] - ppol_ref)
        file_results["spol"]=np.mean(peaks[1] - spol_ref)
        file_results["spol_err"]=np.std(peaks[1] - spol_ref)
        file_results["FitPoints"] = row["FitPoints"]
        file_results["WidthThres"] = row["WidthThres"]
        file_results["RoundTrip"] = row["RoundTrip"]
        if row["Run"] == 9:
            file_results["DownSampling"] = 1
        else:
            file_results["DownSampling"] = row["DownSampling"]
        results.append(file_results)

    results = pd.DataFrame(results)
    print(tabulate(results, headers = 'keys', tablefmt = 'psql'))
    return results, ppol_ref, spol_ref

spectrums = read_spectrums("/eos/user/j/jcapotor/FBGdata/Data/12012023_datosRepetitividadLatiguillo/Run1_spectrum.bin", 1)
print("The first spectrum has: " + str(len(spectrums)))

results = {}
for ev in range(len(spectrums)):
    x = np.array(np.round(spectrums["Wavelength Axis (nm)"][ev],3))
    index = []
    for i in x:
        index.append(i[0])
    y = (spectrums["Timestamp"][ev])/1E9
    z = np.array(spectrums["Spectral data"][ev])
    results[str(ev)] = z

df = pd.DataFrame(results, index=index)

logfile = read_logile()
xs = []
xs_err = []
xs.append(np.mean(df.columns.astype(int)))
xs_err.append(len(df.columns)/2)
for index, row in logfile.iterrows(): 
    if str(row["Run"]) == "1":
        continue
    if str(row["Run"]) =="17":
        break
    spectrums = read_spectrums("/eos/user/j/jcapotor/FBGdata/Data/12012023_datosRepetitividadLatiguillo/Run"+str(row["Run"])+"_spectrum.bin", row["Run"])
    print("The spectrum numnber " + str(row["Run"]) + " has " + str(len(spectrums)))

    results = {}
    for cnt in range(len(spectrums)):
        x = np.array(np.round(spectrums["Wavelength Axis (nm)"][cnt],3))
        index = []
        for i in x:
            index.append(i[0])
        y = np.array(np.round((spectrums["Timestamp"][cnt])/1E9,3))
        z = np.array(spectrums["Spectral data"][cnt])
        ev += 1
        results[str(ev)] = z

    df2 = pd.DataFrame(results, index=index)
    xs.append(np.mean(df2.columns.astype(int)))
    xs_err.append(len(df2.columns)/2)
    df = pd.merge(df, df2, left_index=True, right_index=True)

print("The final dataframe has: " + str(len(df.columns)))

results, ppol_ref, spol_ref = get_table()
y = (results["spol"][0:len(xs)]+spol_ref)*1E9
y2 = (results["ppol"][0:len(xs)]+ppol_ref)*1E9
for i in y:
    print(i)
yerr = (results["spol_err"][0:len(xs)])*1E9

df = df[df.index > np.min(y) - 0.1]
df = df[df.index < np.max(y) + 0.1]
print(df.head())

plt.figure(constrained_layout=True)
plt.imshow(df, cmap="inferno", extent=[0, np.max(df.columns.astype(int)), np.max(df.index.astype(float)), np.min(df.index.astype(float))], aspect="auto")
plt.axis("tight")
yticks = np.linspace(np.min(df.index.astype(float)), np.max(df.index.astype(float)), 20)
plt.yticks(yticks, np.round(yticks,3))
plt.errorbar(xs,y,yerr=yerr,xerr=xs_err, fmt="o")
plt.plot(xs, y2, "o")
plt.gca().invert_yaxis()
plt.show(block=True)

# fit_results = get_fit_parameters(spectrums)
# print(fit_results)
# plt.figure()
# plt.scatter(spectrums["Wavelength Axis (nm)"][0][10000:12000],spectrums["Spectral data"][0][10000:12000])
# plt.plot(spectrums["Wavelength Axis (nm)"][0][11000:11150], gaussian(spectrums["Wavelength Axis (nm)"][0][11000:11150], fit_results[0], fit_results[1], fit_results[2]), color="orange")
# plt.show(block=True)