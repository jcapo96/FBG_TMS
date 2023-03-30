import read_files, manage_data
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

path_to_folder = "/eos/user/j/jcapotor/FBGdata/Data/PatchCableTests/20230210/"
files = ["1", "2", "3", "4", "5", "6", "7", "9", "10"]

amp_results = {}
wav_results = {}
fwhm_results = {}
for file in files:
    print("Filling Run" + file)
    peaks = read_files.read_peaks(path_to_folder + "Run"+file+"_peaks.txt")
    peaks_p, peaks_s, peaks_p_full, peaks_s_full = manage_data.process_data(peaks)
    spectrums = read_files.read_spectrums(path_to_folder + "Run"+file+"_specs.txt", [0])
    spectrums_p, spectrums_s, spectrums_p_full, spectrums_s_full = manage_data.process_data(spectrums)
    spectrums_p, peaks_p = manage_data.match_dataframes(spectrums_p, peaks_p)

    amp_results["Run"+file] = {}
    wav_results["Run"+file] = {}
    fwhm_results["Run"+file] = {}
    for variable in ["Wav1-1", "Wav1-2", "Wav1-3", "Wav1-4"]:
        amp_results["Run"+file]["specs_P_"+variable+"_amp (AU)"] = str(np.round(np.mean(spectrums_p[variable+"_amp"]), 0)) + " +- " + str(np.round(np.std(spectrums_p[variable+"_amp"]),0))
        wav_results["Run"+file]["peaks_P_"+variable] = str(np.round(np.mean(peaks_p[variable]*1e9), 6)) + " +- " + str(np.round(np.std(peaks_p[variable]*1e12), 3)) + " pm"
        wav_results["Run"+file]["specs_P_"+variable] = str(np.round(np.mean(spectrums_p[variable]), 6)) + " +- " + str(np.round(np.std(spectrums_p[variable]*1e3), 3)) + " pm"
        fwhm_results["Run"+file]["specs_P_"+variable+"_sgima"] = str(np.round(np.mean(spectrums_p[variable+"_sigma"]*1e3), 3)) + " +- " + str(np.round(np.std(spectrums_p[variable+"_sigma"]*1e3), 3)) + " pm"