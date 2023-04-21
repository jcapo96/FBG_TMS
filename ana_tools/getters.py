import numpy as np
import pandas as pd
import h5py
from tqdm import tqdm
import json
import glob, os, pathlib
#function to get the raw data processed into .hdf5 files 
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

#function to get the matched data from .hdf5 files
def get_processed_data(
    path_to_split=""
):
    data = pd.read_hdf(path_to_split+"matched.h5", key="data")
    return data

#function that reads the .json file containing the plateaus
def get_plateaus():
    current_dir = os.path.dirname(os.path.dirname(os.getcwd()))
    print(current_dir)
    path = glob.glob(current_dir + "/**/plateaus.json", recursive=False)[0]
    print(path)
    f = open(path)
    plateaus = json.load(f)
    return plateaus

#function that reads the .json file containing the plateaus
def get_rtdcal():
    current_dir = os.path.dirname(os.path.dirname(os.getcwd()))
    print(current_dir)
    path = glob.glob(current_dir + "/**/rtd_calib.json", recursive=False)[0]
    print(path)
    f = open(path)
    rtdcal = json.load(f)
    return rtdcal

def get_fbgscal():
    current_dir = os.path.dirname(os.path.dirname(os.getcwd()))
    print(current_dir)
    path = glob.glob(current_dir + "/**/fbgs_calib.json", recursive=False)[0]
    print(path)
    f = open(path)
    fbgcal = json.load(f)
    return fbgcal

#function to downsample data based on timestamp values
def downsample_data(df, bin=1):
    df["Timestamp"] = df["Timestamp"].apply(lambda x: np.round(x/bin, 0))
    downsampled = []
    unique_times = df["Timestamp"].unique()
    progress_bar = tqdm(total=len(unique_times), desc="Downsampling data")
    for time in unique_times:
        chunk = df.loc[df["Timestamp"] == time]
        row = {}
        for col in chunk:
            if col == "Date" or col=="Time" or col=="Datetime" or col == "PolMask":
                continue
            if col == "Timestamp":
                row[col] = time
            if col != "Timestamp":
                row[col] = np.mean(chunk[col])
                row[col+"_err"] = np.std(chunk[col])
        downsampled.append(row)
        progress_bar.update(1)
    progress_bar.close()
    downsampled = pd.DataFrame(downsampled)
    return downsampled