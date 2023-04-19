import sys
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, '../ana_tools')
import getters
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import ROOT

dates = ["20230321", "20230322", "20230323", "20230327", "20230328", "20230329", "20230330"]
for date in dates:
    path_to_ana = "/eos/user/j/jcapotor/FBGana/camara_climatica/MarchRuns/" + date + "/"
    list_of_files = pd.read_csv(path_to_ana+"list_of_files.txt", header=None, names=["Filename"])
    data_list = {}
    for index, file in list_of_files.iterrows():
        filetype = file["Filename"].split(".")[0]
        if filetype == "list_of_files" or filetype=="humidity":
            continue
        print(filetype)
        if filetype == "temperature":
            pols = ["Temp"]
        if filetype == "humidity":
            pols = ["Hum"]
        if filetype == "peaks" or filetype=="spectrums":
            pols = ["Av", "P", "S"]
        for pol in pols:
            data = getters.downsample_data(getters.get_raw_data(path_to_ana, filetype=filetype, pol=pol))
            print(data.columns)
            if filetype == "temperature": 
                data_list["temp"] = data
            if filetype == "humidity":
                data_list["humi"] = data
            if filetype == "peaks":
                data_list["p"+pol.lower()] = data
            if filetype == "spectrums":
                data_list["s"+pol.lower()] = data

    def make_names(df, key):
        names = df.columns
        new_names = []
        for col in names:
            if col == "Timestamp":
                new_names.append(col)
            else:
                new_names.append(key+col)
        print(new_names)
        return new_names

    for key in data_list:
        print(data_list[key].columns)
        data_list[key].columns = make_names(data_list[key], key)
        data_list[key].sort_values("Timestamp")

    data_list_keys = list(data_list.keys())
    merged_df = pd.merge(data_list[data_list_keys[0]], data_list[data_list_keys[1]], on='Timestamp')
    print(merged_df.columns)
    for i in range(2, len(data_list_keys)):
        merged_df = pd.merge(merged_df, data_list[data_list_keys[i]], on='Timestamp')
        print(merged_df.columns)

    merged_df.to_hdf(path_to_ana+"matched.h5", key="data")

    file = ROOT.TFile(path_to_ana+"matched.root", "RECREATE")
    tree = ROOT.TTree("data", "data")

    branch_dict = {}
    cnt = 0
    for col in merged_df.columns:
        branch_dict[col] = ROOT.std.vector('float')()
        for val in merged_df[col]:
            branch_dict[col].push_back(val)
        tree.Branch(col, branch_dict[col])

    tree.Fill()

    file.Write()
    file.Close()