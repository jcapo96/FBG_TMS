import numpy as np
import pandas as pd
import h5py
from tqdm import tqdm
import json

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

def get_plateaus():
    f = open("plateaus.json")
    plateaus = json.load(f)
    return plateaus

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