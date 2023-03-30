import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#Change here the folder where the data is stored, you need to have all the files in the same folder (the script is not necessary)
path_folder_data = "/eos/user/j/jcapotor/FBGdata/Heater_Tests/09012023/"

def time_to_sec(imon, type, df):
    if type == "peaks":
        time_sec = []
        if imon == "O11":
            for ev in df["Time"]:
                time = ev.split(" ")[1].split(":")
                h, m, s = time[0], time[1], time[2]
                totalseconds = float(h)*3600 + float(m)*60 + float(s)
                time_sec.append(np.round(totalseconds, 0))
        if imon == "FBGS":
            for ev in df["Time"]:
                time = ev.split(":")
                h, m, s = time[0], time[1], time[2]
                totalseconds = float(h)*3600 + float(m)*60 + float(s)
                time_sec.append(totalseconds)
    if type == "temp":
        time_sec = []
        for ev in df["Time"]:
            time = ev.split(":")
            h, m, s = time[0], time[1], time[2]
            totalseconds = float(h)*3600 + float(m)*60 + float(s)
            time_sec.append(totalseconds)
    return time_sec

def get_header(imon, type, filename):
    if type=="peaks":
        if imon == "O11":
            names = ["Time", "It_N", "Dummy", "Sweep_N",
                    "ChS1", "FibreS1", "S1", "StatusS1", "Wav1-1", "T1-1",
                    "ChS2", "FibreS2", "S2", "StatusS2", "Wav1-2", "T1-2",
                    "ChS3", "FibreS3", "S3", "StatusS3", "Wav1-3", "T1-3",
                    "ChS4", "FibreS4", "S4", "StatusS4", "Wav1-4", "T1-4"]
        if imon == "FBGS":
            names = ["Date","Time","LineNumber","System status","Wav1-1","Wav1-2","Wav1-3","Wav1-4","Pow1-1","Pow1-2","Pow1-3","Pow1-4"]
    if type=="spectrum":
        print("Still not implemented")
    return names

def resample_data(imon, type, df):
    rows = []
    for time in df["Time"].unique():
        chunk = df[df["Time"]==time]
        cols = []
        for col in chunk.columns:
            if col == "Date" or col == "System status" or col == "It_N" or col == "Dummy" or col[0:3] == "ChS" or col[0:6] == "FibreS" or col[0] == "S":
                cols.append(chunk[col].unique().astype("str"))
            else:
                if col[0] == "W": #this selects the columns that have wl data
                    if imon == "FBGS":
                        cols.append(np.average(chunk[col].astype("float"))*1E3) #results are stored in pm
                        cols.append(np.std(chunk[col].astype("float"))*1E3) #errors are stored in pm
                    if imon == "O11":
                        cols.append(np.average(chunk[col].astype("float"))*1E12) #results are stored in pm
                        plt.hist(chunk[col].astype("float")*1E12)
                        cols.append(np.std(chunk[col].astype("float"))*1E12) #errors are stored in pm
                elif col[0:4] == "Temp":
                    cols.append(np.average(chunk[col].astype("float"))*1E3) #results are stored in mK
                    cols.append(np.std(chunk[col].astype("float"))*1E3) #errors are stored in mK
                else:
                    cols.append(np.average(chunk[col].astype("float")))
                    cols.append(np.std(chunk[col].astype("float")))
        rows.append(cols)
    if type == "peaks":
        if imon == "FBGS":
            names = ["Date","Time","Time_err","LineNumber","LineNumber_err","System status","Wav1-1","Wav1-1_err",
                    "Wav1-2","Wav1-2_err","Wav1-3","Wav1-3_err","Wav1-4","Wav1-4_err","Pow1-1","Pow1-1_err","Pow1-2",
                    "Pow1-2_err","Pow1-3","Pow1-3_err","Pow1-4","Pow1-4_err"]
            resampled_df = pd.DataFrame(rows)
            resampled_df.columns = names
        if imon == "O11":
            names = ["Time", "Time_err", "It_N", "Dummy", "Sweep_N",
                    "ChS1", "FibreS1", "S1", "StatusS1", "Wav1-1", "Wav1-1_err", "T1-1", "T1-1_err",
                    "ChS2", "FibreS2", "S2", "StatusS2", "Wav1-2", "Wav1-2_err", "T1-2", "T1-2_err",
                    "ChS3", "FibreS3", "S3", "StatusS3", "Wav1-3", "Wav1-3_err", "T1-3", "T1-3_err",
                    "ChS4", "FibreS4", "S4", "StatusS4", "Wav1-4", "Wav1-4_err", "T1-4", "T1-4_err"]
            resampled_df = pd.DataFrame(rows)
            resampled_df.columns = names
    if type == "temp":
        names = ["Date", "Time", "Time_err", "Temp1", "Temp1_err", "Temp2", "Temp2_err"]
        resampled_df = pd.DataFrame(rows)
        resampled_df.columns = names
    return resampled_df

def get_temp(imon, type, filename):
    if type == "peaks":
        try:
            if imon == "FBGS":
                temp_filename = "Test" + filename.split("Test")[1][0] + "_RTD.txt"
            if imon == "O11":
                temp_filename = "Test" + filename.split("Test")[1][0] + "_RTD.txt"
        except:
            temp_filename = "09012023_RTD_temp.txt"
    df = pd.read_csv(path_folder_data + temp_filename, sep="\t", names = ["Date", "Time", "Temp1", "Temp2"])
    df["Time"] = time_to_sec(None, "temp", df)
    df = resample_data(None, "temp", df)
    return df

def match_df(df1,df2):
    min_t1 = np.min(df1["Time"].astype("float"))
    min_t2 = np.min(df2["Time"].astype("float"))
    max_t1 = np.max(df1["Time"].astype("float"))
    max_t2 = np.max(df2["Time"].astype("float"))

    min_time = max(min_t1, min_t2)
    max_time = min(max_t1, max_t2)

    df1 = df1[(df1["Time"]>=min_time) & (df1["Time"]<max_time)]
    df2 = df2[(df2["Time"]>=min_time) & (df2["Time"]<max_time)]
    return df1, df2

def process_data(imon, type, filename):
    if type == "peaks":
        if imon == "FBGS":
            df = pd.read_csv(path_folder_data + filename, sep="\t", header=None, skiprows=20, encoding="unicode_escape", decimal=",")
        if imon == "O11":
            df = pd.read_csv(path_folder_data + filename, sep="\t", header=None, encoding="unicode_escape")
            print("Read data DONE")
    df.columns = get_header(imon, type, filename)
    print("Header DONE")
    df["Time"] = time_to_sec(imon, type, df)
    print("Time transformed to seconds")
    df_resampled = resample_data(imon, type, df)
    print("Data Resampled")
    df_temp = get_temp(imon, type, filename)
    print("Temperature uploaded")
    df_resampled, df_temp = match_df(df_resampled, df_temp)
    print("Data Matched")
    return df_resampled, df_temp

def read_data(imon, type, filename):
    if type == "peaks":
        if imon == "O11":
            df_resampled, df_temp = process_data(imon, type, filename)
        if imon == "FBGS":
            df_resampled, df_temp = process_data(imon, type, filename)
        return df_resampled, df_temp
    if type == "spectrum":
        print("Still not implemented")

#To run the software you just have to change in the following line the name of the IMON (FBGS, O11), the type of the file (peaks, spectrum) and the filename
#here there is an example that is comparing the peaks vs time for both interrogators during the same run
data1, data_temp1 = read_data("O11", "peaks", "09012023_peaks_1.txt")
print(data1.head())
plt.figure()
plt.errorbar(data1["Time"], data1["Wav1-2"], yerr=data1["Wav1-2_err"])
plt.show(block=True)