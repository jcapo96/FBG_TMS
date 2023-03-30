import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from tabulate import tabulate
import seaborn as sns

def read_logile():
    logfile = pd.read_csv("/eos/user/j/jcapotor/FBGdata/Data/12012023_datosRepetitividadLatiguillo/Log.txt", skiprows=78, header=None, sep="\t")
    del logfile[2], logfile[4], logfile[6], logfile[7]
    names = ["Run", "FitPoints", "WidthThres", "RoundTrip", "DownSampling"]
    logfile.columns = names
    return logfile

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
                if run == 3 or run == 4 or run==7 or run==11 or run==13 or run==14 or run==15 or run==16 or run == 18:
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

spectrums = read_spectrums("/eos/user/j/jcapotor/FBGdata/Data/12012023_datosRepetitividadLatiguillo/Run1_spectrum.bin", 1)
print("The first spectrum has: " + str(len(spectrums)))

results = {}
int_range = 500
max_value = np.max(spectrums["Spectral data"][0])
cnt = 0
for amplitude in spectrums["Spectral data"][0]:
    if amplitude == max_value:
        max_index = cnt
        break
    else:
        cnt += 1

max_value_s2 = np.max(spectrums["Spectral data"][0][max_index+10000+int_range:max_index+int_range+15000])
cnt = 0
for amplitude in spectrums["Spectral data"][0][max_index+10000+int_range:max_index+int_range+15000]:
    if amplitude == max_value_s2:
        max_index_s2 = cnt
        break
    else:
        cnt += 1
print("**************************************************************")
max_index_s2 = max_index_s2 + max_index
print("The maximum index is " + str(max_index))
print("The maximum index s2 is " + str(max_index_s2))

integral0 = np.sum(spectrums["Spectral data"][0][(max_index-int_range):max_index+int_range]/np.max(spectrums["Spectral data"][0][(max_index-int_range):max_index+int_range]))
integral0_s2 = np.sum(spectrums["Spectral data"][0][(max_index_s2-int_range):max_index_s2+int_range]/np.max(spectrums["Spectral data"][0][(max_index_s2-int_range):max_index_s2+int_range]))

logfile = read_logile()
integrals = []
integrals_s2 = []
for index, row in logfile.iterrows(): 
    if str(row["Run"]) =="10":
        break
    spectrums = read_spectrums("/eos/user/j/jcapotor/FBGdata/Data/12012023_datosRepetitividadLatiguillo/Run"+str(row["Run"])+"_spectrum.bin", row["Run"])
    for i in range(len(spectrums["Spectral data"])):
        #plt.plot(spectrums["Spectral data"][i][(max_index-int_range):max_index+int_range]/(np.max(spectrums["Spectral data"][i][(max_index-int_range):max_index+int_range])))
        plt.plot(spectrums["Spectral data"][i][(max_index_s2-int_range):max_index_s2+int_range]/(np.max(spectrums["Spectral data"][i][(max_index_s2-int_range):max_index_s2+int_range])))
    print("The spectrum number " + str(row["Run"]) + " has " + str(len(spectrums)))

    for cnt in range(len(spectrums)):
        integral = np.sum(spectrums["Spectral data"][cnt][(max_index-int_range):(max_index+int_range)]/(np.max(spectrums["Spectral data"][cnt][(max_index-int_range):max_index+int_range])))
        integral_s2 = np.sum(spectrums["Spectral data"][cnt][(max_index_s2-int_range):(max_index_s2+int_range)]/(np.max(spectrums["Spectral data"][cnt][(max_index_s2-int_range):max_index_s2+int_range])))
        integrals.append(integral/integral0)
        integrals_s2.append(integral_s2/integral0_s2)
    print(integral)
    print(integral_s2)

print(len(integrals))
print(len(integrals_s2))

plt.figure()
plt.plot(integrals)
plt.plot(integrals_s2)
plt.show(block=True)
