import pandas as pd
import numpy as np
from scipy.signal import find_peaks
from iminuit import Minuit
from iminuit.cost import LeastSquares
import datetime
import xlrd
import sys
sys.path.insert(1, '/afs/cern.ch/user/j/jcapotor/FBG_TMS/ana_tools')
import getters, setters, utils

def gaussian(x, H, A, x0, sigma):
    return H + A * np.exp(-(x - x0) ** 2 / (2 * sigma ** 2))

def sine(x, H, A, x0, sigma):
    return H + A*np.sin((x-x0)*sigma)

def process_spectrums(
    path_to_data = "",
    filename = "", path_to_save_folder="",
    channels=[0,1], n_sensors=[5,4], wl_positions=[[1535,1540,1545,1550,1555],[1540,1545,1550,1555]],
    n_points=60, threshold=500, i4g_resolution=30E-6,
    func=gaussian, save_all=False
    ):
    #This function takes the filename with the full path to the data and the channels in list format that must be stored in the dataframe
    #it returns the data contained in the binary spectrum files
    FileId=open(path_to_data + filename,'rb')#open file to be read
    data = {}
    data["Timestamp"] = []
    data["Baseline"] = []
    if save_all == True:
        sweeps = []
        sweeps = pd.DataFrame(sweeps)
    persistentRead = True
    cnt = 0
    cnt_fin = 0
    while persistentRead == True:
        try:
            sweep = {}
            sweep['PacketSize'] = (np.fromfile(FileId, dtype='<i4', count=1))
            sweep['Timestamp'] = float((np.fromfile(FileId, dtype='<u8', count=1)))
            sweep['Validity flag'] = (np.fromfile(FileId, dtype='<i4', count=1))
            sweep['Channel No.'] = (np.fromfile(FileId, dtype='<i4', count=1))
            sweep['Fibre No.'] = (np.fromfile(FileId, dtype='<i4', count=1))
            sweep['Start wavelength'] = (np.fromfile(FileId, dtype='<d', count=1))
            sweep['Stop wavelength'] = (np.fromfile(FileId, dtype='<d', count=1))
            sweep['No. of wavelength points']=(np.fromfile(FileId, dtype='<i4', count=1))
            sweep['Data']=(np.fromfile(FileId, dtype='<i2', count=sweep['No. of wavelength points'][0]))
            sweep['WL']=np.linspace(sweep['Start wavelength'],sweep['Stop wavelength'],int(sweep['No. of wavelength points'])).T[0]
            if save_all == True:
                sweeps.append(sweep)
            try:
                current_channel = int(sweep["Channel No."][0])
                start_wl = float(sweep["Start wavelength"][0])*1e3
                if current_channel not in channels:
                    continue
                if current_channel == channels[0]:
                    data["Timestamp"].append(sweep["Timestamp"])
                    data["Baseline"].append(np.mean(sweep["Data"][0:4000]))
                if cnt % 1000 == 0:
                    print(sweep)
                peaks_index, _ = find_peaks(sweep["Data"], height=threshold)
                if len(peaks_index) != n_sensors[current_channel]:
                    peaks_index = []
                    for pos in wl_positions[current_channel]:
                        n_points = 2000
                        wl_peak = int(pos*1e3 - start_wl)
                        peak, peak_amp = find_peaks(sweep["Data"][wl_peak-n_points:wl_peak+n_points], height=threshold)
                        try:
                            peak = int(wl_peak + peak[0])
                            peaks_index.append(peak)
                        except:
                            peak = int(wl_peak + peak)
                            peaks_index.append(peak)
                current_sens = 1
                for peak in peaks_index:
                    xdata, ydata = sweep["WL"][int(peak-n_points/2):int(peak+n_points/2)+1], sweep["Data"][int(peak-n_points/2):int(peak+n_points/2)+1]
                    ydata_err = i4g_resolution
                    LSQ = LeastSquares(xdata, ydata, ydata_err, func)
                    m = Minuit(LSQ, H=1e2, A=3e3, x0=sweep["WL"][peak], sigma=4e-2)
                    m.migrad()
                    fwhm = utils.get_fwhm(sweep, peak, xdata, m, func)
                    As = utils.get_As(sweep, peak, xdata, m, func)
                    if cnt in range(len(channels)):
                        data["Wav"+str(current_channel+1)+"-"+str(current_sens)] = [m.values["x0"]]
                        data["Wav"+str(current_channel+1)+"-"+str(current_sens)+"_FLAG"] = [m.accurate]
                        data["Wav"+str(current_channel+1)+"-"+str(current_sens)+"_fwhm"] = [fwhm]
                        data["Wav"+str(current_channel+1)+"-"+str(current_sens)+"_sigma"] = [m.values["sigma"]]
                        data["Wav"+str(current_channel+1)+"-"+str(current_sens)+"_amp"] = [np.max(func(xdata, m.values["H"], m.values["A"], m.values["x0"], m.values["sigma"]))]
                        data["Wav"+str(current_channel+1)+"-"+str(current_sens)+"_As"] = [As]
                    else:
                        data["Wav"+str(current_channel+1)+"-"+str(current_sens)].append(m.values["x0"])
                        data["Wav"+str(current_channel+1)+"-"+str(current_sens)+"_FLAG"].append(m.accurate)
                        data["Wav"+str(current_channel+1)+"-"+str(current_sens)+"_sigma"].append(m.values["sigma"])
                        data["Wav"+str(current_channel+1)+"-"+str(current_sens)+"_fwhm"].append(fwhm)
                        data["Wav"+str(current_channel+1)+"-"+str(current_sens)+"_amp"].append(np.max(func(xdata, m.values["H"], m.values["A"], m.values["x0"], m.values["sigma"])))
                        data["Wav"+str(current_channel+1)+"-"+str(current_sens)+"_As"].append(As)
                    current_sens += 1
            except:
                print("Event: "+str(cnt)+" failed")
                cnt += 1
                continue
            cnt += 1
            if cnt % 100 == True:
                print(cnt)
                print(sweep)
        except:
            print("Finished at event: " + str(cnt))
            persistentRead = False
            data = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in data.items() ]))
            data["Timestamp"] = data["Timestamp"].apply(setters.time_to_seconds)
            data = setters.add_polarisation_mask(data)
            data_p = data.loc[(data["PolMask"] == "p")].reset_index(drop=True)
            data_s = data.loc[(data["PolMask"] == "s")].reset_index(drop=True)
            n_file = filename.split("_")[1].split(".")[0]
            data_p.to_hdf(path_to_save_folder + "spectrums.h5", key="P"+n_file)
            data_s.to_hdf(path_to_save_folder + "spectrums.h5", key="S"+n_file)
            del data_p["PolMask"]
            del data_s["PolMask"]
            data_av = (data_p + data_s)/2
            data_diff = (data_p - data_s)
            data_av.to_hdf(path_to_save_folder + "spectrums.h5", key="Av"+n_file)
            data_diff.to_hdf(path_to_save_folder + "spectrums.h5", key="Diff"+n_file)
            print("Spectrums Saved")

def process_peaks(
    path_to_data="",
    filename="",
    path_to_save_folder = "",
    channels = [], n_sensors=[],
    chunksize=1e6
    ):
    data = pd.read_csv(path_to_data+filename, sep="\t", header=None, chunksize=chunksize)
    names = ["Timestamp"]
    columns = [1]
    totalsensors = 0
    for chan in range(len(channels)):
        for sens in range(n_sensors[chan]):
            names.append("Wav"+str(chan+1)+"-"+str(sens+1))
            columns.append(6*totalsensors + 8)
            totalsensors += 1
    i = 1
    for chunk in data:
        chunk = chunk[columns]
        chunk.columns = names
        chunk = chunk.reset_index(drop=True)
        # chunk_p, chunk_s = manage_data.process_data(chunk)
        chunk["Timestamp"] = chunk["Timestamp"].apply(setters.time_to_seconds)
        chunk = setters.add_polarisation_mask(chunk)
        chunk_p = chunk.loc[(chunk["PolMask"]=="p")].reset_index(drop=True)
        chunk_s = chunk.loc[(chunk["PolMask"]=="s")].reset_index(drop=True)
        n_file = filename.split("_")[1].split(".")[0]
        chunk_p.to_hdf(path_to_save_folder + "peaks.h5", key=str(i)+"P"+n_file)
        chunk_s.to_hdf(path_to_save_folder + "peaks.h5", key=str(i)+"S"+n_file)
        del chunk_p["PolMask"]
        del chunk_s["PolMask"]
        chunk_av = (chunk_p+chunk_s)/2
        chunk_diff = (chunk_p-chunk_s)
        chunk_av.to_hdf(path_to_save_folder + "peaks.h5", key=str(i)+"Av"+n_file)
        chunk_diff.to_hdf(path_to_save_folder + "peaks.h5", key=str(i)+"Diff"+n_file)
        print("Processed chunk" + str(i))
        i += 1

def process_temperature(
    path_to_data="",
    filename="", path_to_save_folder=""):
    data = pd.read_csv(path_to_data + filename, sep="\t", header=None)
    for n_sensors in range(1,7):
        try:
            names = ["Date", "Time"]
            for i in range(n_sensors):
                names.append("T"+str(i+1))
            data.columns = names
        except:
            continue
    data["Timestamp"] = data["Date"]+ "-" +data["Time"]
    data["Timestamp"] = data["Timestamp"].apply(setters.time_to_seconds)
    n_file = filename.split("_")[1].split(".")[0]
    data.to_hdf(path_or_buf=path_to_save_folder+"temperature.h5", key="Temp"+str(n_file))

def process_humidity(
    path_to_data="",
    filename="", path_to_save_folder=""
    ):
    data = pd.read_csv(path_to_data+filename, sep=";", skiprows=1, header=None, decimal=",").astype(float)
    data.columns = ["Timestamp", "ObRH", "RH", "ObT", "T"]
    data["Timestamp"] = data["Timestamp"].apply(lambda x: str(xlrd.xldate.xldate_as_datetime(x, 0).date()) + " " + str(xlrd.xldate.xldate_as_datetime(x, 0).time()).split(".")[0])
    data["Timestamp"] = data["Timestamp"].apply(setters.time_to_seconds)
    n_file = str(filename.split("_")[1].split(".")[0])
    print(data)
    data.to_hdf(path_or_buf=path_to_save_folder+"humidity.h5", key="Hum"+n_file)
