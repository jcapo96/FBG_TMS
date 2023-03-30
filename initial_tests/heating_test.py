import polars as pl
import numpy as np
import matplotlib.pyplot as plt

path_folder_data = "/eos/user/j/jcapotor/FBGdata/Data/Heater_Tests/09012023/"

def convert_time_temp(x):
    x = x.split(":")
    if len(x) == 2:
        return int(x[0]) * 60 + int(x[1])
    return int(x[0]) * 3600 + int(x[1]) * 60 + int(x[2])

def convert_time_peaks(x):
    x = x.split(" ")[1].split(":")
    return int(np.round(int(x[0])*3600 + int(x[1])*60 + float(x[2]), 0))

def read_peaks(filename):
    data = pl.read_csv(
        path_folder_data + filename,
        sep="\t",
        columns = [0, 8, 14, 20, 26],
        new_columns = ["TimeStamp", "Wav1-1", "Wav1-2", "Wav1-3", "Wav1-4"]
    )
    data["TimeStamp"] = data["TimeStamp"].apply(convert_time_peaks)
    data = data.groupby("TimeStamp", maintain_order=True).mean()
    return data

def read_temp(filename):
    data = pl.read_csv(
        path_folder_data + filename,
        sep="\t",
        columns = [1,2,3],
        new_columns = ["Time", "T1", "T2"]
    )
    data["Time"] = data["Time"].apply(convert_time_temp)
    data = data.groupby("Time", maintain_order=True).mean()
    return data


data_peaks = read_peaks("09012023_peaks_1.txt")
data_temp = read_temp("09012023_RTD_temp.txt")

data_peaks = data_peaks.filter(
    (pl.col("TimeStamp") > data_temp["Time"].min()) & (pl.col("TimeStamp") < data_temp["Time"].max())
)

print(data_peaks)

plt.figure()
plt.plot(data_peaks["TimeStamp"], data_peaks["Wav1-1_mean"])
plt.show(block=True)
# data_merged = pl.concat([
#     data_peaks,
#     data_temp,
#     ],
#     how="horizontal")
# data_merged = data_merged.filter(
#     pl.col("TimeStamp") == data_merged["Time"]
# )

