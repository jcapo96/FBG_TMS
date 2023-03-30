import read_files, manage_data
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

path_to_folder = "/eos/user/j/jcapotor/FBGdata/Data/PatchCableTests/20230209/"
files = ["1", "2", "3", "4", "5", "6", "7"]

amp_results = {}
wav_results = {}
fwhm_results = {}
for file in files:
    print("Filling Run" + file)
    temp = read_files.read_temperature(path_to_folder + "RTD.txt")
    temp = manage_data.process_data(temp)
    peaks = read_files.read_peaks(path_to_folder + "Run"+file+"_peaks")
    peaks_p, peaks_s, peaks_p_full, peaks_s_full = manage_data.process_data(peaks)
    spectrums = read_files.read_spectrums(path_to_folder + "Run"+file+"_specs", [0])
    spectrums_p, spectrums_s, spectrums_p_full, spectrums_s_full = manage_data.process_data(spectrums)
    spectrums_p, peaks_p = manage_data.match_dataframes(spectrums_p, peaks_p)
    spectrums_p, temp = manage_data.match_dataframes(spectrums_p, temp)
    peaks_p, temp = manage_data.match_dataframes(peaks_p, temp)

    amp_results["Run"+file] = {}
    wav_results["Run"+file] = {}
    fwhm_results["Run"+file] = {}
    for variable in ["Wav1-1", "Wav1-2", "Wav1-3", "Wav1-4"]:
        amp_results["Run"+file]["specs_P_"+variable+"_amp (AU)"] = str(np.round(np.mean(spectrums_p[variable+"_amp"]), 0)) + " +- " + str(np.round(np.std(spectrums_p[variable+"_amp"]),0))
        wav_results["Run"+file]["peaks_P_"+variable] = str(np.round(np.mean(peaks_p[variable]*1e9), 6)) + " +- " + str(np.round(np.std(peaks_p[variable]*1e12), 3)) + " pm"
        wav_results["Run"+file]["specs_P_"+variable] = str(np.round(np.mean(spectrums_p[variable]), 6)) + " +- " + str(np.round(np.std(spectrums_p[variable]*1e3), 3)) + " pm"
        fwhm_results["Run"+file]["specs_P_"+variable+"_sgima"] = str(np.round(np.mean(spectrums_p[variable+"_sigma"]*1e3), 3)) + " +- " + str(np.round(np.std(spectrums_p[variable+"_sigma"]*1e3), 3)) + " pm"
    amp_results["Run"+file]["Temp1 (K)"] = str(np.round(np.mean(temp["T1"]), 3)) + " +- " + str(np.round(np.std(temp["T1"])*1e3, 0)) + " mK"
    amp_results["Run"+file]["Temp2 (K)"] = str(np.round(np.mean(temp["T2"]), 3)) + " +- " + str(np.round(np.std(temp["T2"])*1e3, 0)) + " mK"
    wav_results["Run"+file]["Temp1 (K)"] = str(np.round(np.mean(temp["T1"]), 3)) + " +- " + str(np.round(np.std(temp["T1"])*1e3, 0)) + " mK"
    wav_results["Run"+file]["Temp2 (K)"] = str(np.round(np.mean(temp["T2"]) , 3)) + " +- " + str(np.round(np.std(temp["T2"])*1e3, 0)) + " mK"
    fwhm_results["Run"+file]["Temp1 (K)"] = str(np.round(np.mean(temp["T1"]), 3)) + " +- " + str(np.round(np.std(temp["T1"])*1e3, 0)) + " mK"
    fwhm_results["Run"+file]["Temp2 (K)"] = str(np.round(np.mean(temp["T2"]), 3)) + " +- " + str(np.round(np.std(temp["T2"])*1e3, 0)) + " mK"