import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate

path_folder_data = "/eos/user/j/jcapotor/FBGdata/Data/InterrogatorTests/20221220/"

data_o11_1 = pd.read_csv(path_folder_data + "Test1_Optics.txt", sep="\t", header=None)
data_o11_2 = pd.read_csv(path_folder_data + "Test2_Optics .txt", sep="\t", header=None)
data_o11_3 = pd.read_csv(path_folder_data + "Test3_Optics.txt", sep="\t", header=None)
data_o11_4 = pd.read_csv(path_folder_data + "Test4_Optics.txt", sep="\t", header=None)
data_o11_5 = pd.read_csv(path_folder_data + "Test5_Optics.txt", sep="\t", header=None)
data_o11_6 = pd.read_csv(path_folder_data + "Test6_Optics.txt", sep="\t", header=None)
data_rtd_1 = pd.read_csv(path_folder_data + "Test1_RTD.txt", sep="\t", header=None)
data_rtd_2 = pd.read_csv(path_folder_data + "Test2_RTD.txt", sep="\t", header=None)
data_rtd_3 = pd.read_csv(path_folder_data + "Test3_RTD.txt", sep="\t", header=None)
data_rtd_4 = pd.read_csv(path_folder_data + "Test4_RTD.txt", sep="\t", header=None)
data_rtd_5 = pd.read_csv(path_folder_data + "Test4_RTD.txt", sep="\t", header=None)
data_rtd_6 = pd.read_csv(path_folder_data + "Test6_RTD.txt", sep="\t", header=None)
data_fbgs_1 = pd.read_csv(path_folder_data + "20221220 145052-Test1_LLumiSense-Wav-CH1.txt", sep="\t", skiprows=20, header=None, encoding= 'unicode_escape', decimal=",")
data_fbgs_2 = pd.read_csv(path_folder_data + "20221220 150330-Test2_LLumiSense-Wav-CH1.txt", sep="\t", skiprows=20, header=None, encoding= 'unicode_escape', decimal=",")
data_fbgs_3 = pd.read_csv(path_folder_data + "20221220 151505-Test3_LLumiSense-Wav-CH1.txt", sep="\t", skiprows=20, header=None, encoding= 'unicode_escape', decimal=",")
data_fbgs_4 = pd.read_csv(path_folder_data + "20221220 153003-Test4_LLumiSense-Wav-CH1.txt", sep="\t", skiprows=20, header=None, encoding= 'unicode_escape', decimal=",")
data_fbgs_5 = pd.read_csv(path_folder_data + "20221220 154444-Test5_LLumiSense-Wav-CH1.txt", sep="\t", skiprows=20, header=None, encoding= 'unicode_escape', decimal=",")
data_fbgs_6 = pd.read_csv(path_folder_data + "20221220 160945-Test6_LLumiSense-Wav-CH1.txt", sep="\t", skiprows=20, header=None, encoding= 'unicode_escape', decimal=",")

def time_to_sec_rtd(column):
    time_sec = []
    for ev in column:
        time = ev.split(":")
        h, m, s = time[0], time[1], time[2]
        totalseconds = float(h)*3600 + float(m)*60 + float(s)
        time_sec.append(totalseconds)
    return time_sec

def time_to_sec_o11(column):
    time_sec = []
    for ev in column:
        time = ev.split(" ")[1]
        time = time.split(":")
        h, m, s = time[0], time[1], time[2]
        totalseconds = float(h)*3600 + float(m)*60 + float(s)
        time_sec.append(np.round(totalseconds, 0))
    return time_sec

def average_data(df, ref, col1, col2, col3, col4):
    rows = []
    for time in df[ref].unique():
        df2 = df[df[ref]==time]
        mean_s1 = np.average(df2[col1].astype("float"))
        mean_s2 = np.average(df2[col2].astype("float"))
        mean_s3 = np.average(df2[col3].astype("float"))
        mean_s4 = np.average(df2[col4].astype("float"))
        rows.append([time, mean_s1, mean_s2, mean_s3, mean_s4])
    df3 = pd.DataFrame(rows)
    return df3

def cut_time(df1, df2):
    min_t1 = np.min(df1[0].astype("float"))
    min_t2 = np.min(df2[0].astype("float"))
    max_t1 = np.max(df1[0].astype("float"))
    max_t2 = np.max(df2[0].astype("float"))

    min_time = max(min_t1, min_t2)
    max_time = min(max_t1, max_t2)

    df1 = df1[(df1[0]>=min_time) & (df1[0]<max_time)]
    df2 = df2[(df2[0]>=min_time) & (df2[0]<max_time)]

    return df1, df2

def process_data_o11(rtd, imon):
    rtd[1] = time_to_sec_rtd(rtd[1])
    imon[0] = time_to_sec_o11(imon[0])
    imon = average_data(imon, 0, 8, 14, 20, 26)
    rtd = average_data(rtd, 1, 2, 3, 2, 3)
    rtd, imon = cut_time(rtd, imon)
    return rtd, imon

def process_data_fbgs(rtd, imon):
    rtd[1] = time_to_sec_rtd(rtd[1])
    imon[1] = time_to_sec_rtd(imon[1])
    imon = average_data(imon,1,4,5,6,7)
    rtd = average_data(rtd, 1, 2, 3, 2, 3)
    rtd, imon = cut_time(rtd, imon)
    return rtd, imon

data_rtd_1_cut, data_o11_1 = process_data_o11(data_rtd_1.copy(), data_o11_1)
data_rtd_2_cut, data_o11_2 = process_data_o11(data_rtd_2.copy(), data_o11_2)
data_rtd_3_cut, data_o11_3 = process_data_o11(data_rtd_3.copy(), data_o11_3)
data_rtd_4_cut, data_o11_4 = process_data_o11(data_rtd_4.copy(), data_o11_4)
data_rtd_5_cut, data_o11_5 = process_data_o11(data_rtd_5.copy(), data_o11_5)
data_rtd_6_cut, data_o11_6 = process_data_o11(data_rtd_6.copy(), data_o11_6)

data2_rtd_1 = pd.read_csv(path_folder_data + "Test1_RTD.txt", sep="\t", header=None)
data2_rtd_2 = pd.read_csv(path_folder_data + "Test2_RTD.txt", sep="\t", header=None)
data2_rtd_3 = pd.read_csv(path_folder_data + "Test3_RTD.txt", sep="\t", header=None)
data2_rtd_4 = pd.read_csv(path_folder_data + "Test4_RTD.txt", sep="\t", header=None)
data2_rtd_5 = pd.read_csv(path_folder_data + "Test4_RTD.txt", sep="\t", header=None)
data2_rtd_6 = pd.read_csv(path_folder_data + "Test4_RTD.txt", sep="\t", header=None)

data_rtd_1_cut2, data_fbgs_1 = process_data_fbgs(data2_rtd_1, data_fbgs_1)
data_rtd_2_cut2, data_fbgs_2 = process_data_fbgs(data2_rtd_2, data_fbgs_2)
data_rtd_3_cut2, data_fbgs_3 = process_data_fbgs(data2_rtd_3, data_fbgs_3)
data_rtd_4_cut2, data_fbgs_4 = process_data_fbgs(data2_rtd_4, data_fbgs_4)

# data_rtd_6_cut2, data_fbgs_6 = process_data_fbgs(data2_rtd_6, data_fbgs_6)

plt.figure()
plt.subplot(1,3,1)
plt.title("OPTICS")
plt.hist(data_o11_1[1], color="red")
plt.hist(data_o11_2[1], color="green")
plt.hist(data_o11_3[1], color="orange")
plt.hist(data_o11_4[1], color="blue")
plt.subplot(1,3,3)
plt.title("Temperature")
plt.hist(data_rtd_1_cut[2], color="red")
plt.hist(data_rtd_1_cut2[2], edgecolor="red", linewidth=1, fill=False)
plt.hist(data_rtd_2_cut[2], color="green")
plt.hist(data_rtd_2_cut2[2], edgecolor="green", linewidth=1, fill=False)
plt.hist(data_rtd_3_cut[2], color="orange")
plt.hist(data_rtd_3_cut2[2], edgecolor="orange", linewidth=1, fill=False)
plt.hist(data_rtd_4_cut[2], color="blue")
plt.hist(data_rtd_4_cut2[2], edgecolor="blue", linewidth=1, fill=False)
plt.subplot(1,3,2)
plt.title("FBGS")
plt.hist(data_fbgs_1[4], edgecolor="red", linewidth=2, fill=False)
plt.hist(data_fbgs_2[4], edgecolor="green",linewidth=2,fill=False)
plt.hist(data_fbgs_3[4], edgecolor="orange", linewidth=2, fill=False)
plt.hist(data_fbgs_4[4], edgecolor="blue", linewidth=2, fill=False)

plt.figure(constrained_layout=True)
plt.subplot(5,1,2)
plt.scatter(data_rtd_1_cut[0], data_o11_1[1], color="black", label="OPTICS11")
plt.scatter(data_rtd_2_cut[0], data_o11_2[1][3:], color="black")
plt.scatter(data_rtd_3_cut[0], data_o11_3[1], color="black")
plt.scatter(data_rtd_4_cut[0], data_o11_4[1], color="black")
plt.scatter(data_rtd_1_cut2[0], data_fbgs_1[1]/1E9, color="red", label="FBGS")
plt.scatter(data_rtd_2_cut2[0], data_fbgs_2[1]/1E9, color="red")
plt.scatter(data_rtd_3_cut2[0], data_fbgs_3[1]/1E9, color="red")
plt.scatter(data_rtd_4_cut2[0], data_fbgs_4[1]/1E9, color="red")
plt.ylabel("WL (pm)")
plt.title("S1: 1540 nm")
plt.subplot(5,1,3)
plt.scatter(data_rtd_1_cut[0], data_o11_1[2], color="black", label="OPTICS11")
plt.scatter(data_rtd_2_cut[0], data_o11_2[2][3:], color="black")
plt.scatter(data_rtd_3_cut[0], data_o11_3[2], color="black")
plt.scatter(data_rtd_4_cut[0], data_o11_4[2], color="black")
plt.scatter(data_rtd_1_cut2[0], data_fbgs_1[2]/1E9, color="red", label="FBGS")
plt.scatter(data_rtd_2_cut2[0], data_fbgs_2[2]/1E9, color="red")
plt.scatter(data_rtd_3_cut2[0], data_fbgs_3[2]/1E9, color="red")
plt.scatter(data_rtd_4_cut2[0], data_fbgs_4[2]/1E9, color="red")
plt.ylabel("WL (pm)")
plt.title("S2: 1545 nm")
plt.subplot(5,1,1)
plt.scatter(data_rtd_1_cut[0], data_rtd_1_cut[2], color="black", label="OPTICS11")
plt.scatter(data_rtd_2_cut[0], data_rtd_2_cut[2], color="black")
plt.scatter(data_rtd_3_cut[0], data_rtd_3_cut[2], color="black")
plt.scatter(data_rtd_4_cut[0], data_rtd_4_cut[2], color="black")
plt.scatter(data_rtd_1_cut2[0], data_rtd_1_cut2[2], color="black", label="OPTICS11")
plt.scatter(data_rtd_2_cut2[0], data_rtd_2_cut2[2], color="black")
plt.scatter(data_rtd_3_cut2[0], data_rtd_3_cut2[2], color="black")
plt.scatter(data_rtd_4_cut2[0], data_rtd_4_cut2[2], color="black")
plt.ylabel("T (K)")
plt.title("RTD Temperature")
plt.subplot(5,1,4)
plt.scatter(data_rtd_1_cut[0], data_o11_1[3], color="black", label="OPTICS11")
plt.scatter(data_rtd_2_cut[0], data_o11_2[3][3:], color="black")
plt.scatter(data_rtd_3_cut[0], data_o11_3[3], color="black")
plt.scatter(data_rtd_4_cut[0], data_o11_4[3], color="black")
plt.scatter(data_rtd_1_cut2[0], data_fbgs_1[3]/1E9, color="red", label="FBGS")
plt.scatter(data_rtd_2_cut2[0], data_fbgs_2[3]/1E9, color="red")
plt.scatter(data_rtd_3_cut2[0], data_fbgs_3[3]/1E9, color="red")
plt.scatter(data_rtd_4_cut2[0], data_fbgs_4[3]/1E9, color="red")
plt.ylabel("WL (pm)")
plt.title("S3: 1550 nm")
plt.subplot(5,1,5)
plt.scatter(data_rtd_1_cut[0], data_o11_1[4], color="black", label="OPTICS11")
plt.scatter(data_rtd_2_cut[0], data_o11_2[4][3:], color="black")
plt.scatter(data_rtd_3_cut[0], data_o11_3[4], color="black")
plt.scatter(data_rtd_4_cut[0], data_o11_4[4], color="black")
plt.scatter(data_rtd_1_cut2[0], data_fbgs_1[4]/1E9, color="red", label="FBGS")
plt.scatter(data_rtd_2_cut2[0], data_fbgs_2[4]/1E9, color="red")
plt.scatter(data_rtd_3_cut2[0], data_fbgs_3[4]/1E9, color="red")
plt.scatter(data_rtd_4_cut2[0], data_fbgs_4[4]/1E9, color="red")
plt.xlabel("Time (s)")
plt.ylabel("WL (pm)")
plt.title("S4: 1555 nm")
plt.legend()

plt.figure(constrained_layout=True)
plt.subplot(3,1,1)
plt.scatter(data_rtd_1_cut[0], data_o11_1[1] - data_o11_1[2], color="black", label="OPTICS11")
plt.scatter(data_rtd_2_cut[0], data_o11_2[1][3:] - data_o11_2[2][3:], color="black")
plt.scatter(data_rtd_3_cut[0], data_o11_3[1] - data_o11_3[2], color="black")
plt.scatter(data_rtd_4_cut[0], data_o11_4[1] - data_o11_4[2], color="black")
plt.scatter(data_rtd_1_cut2[0], data_fbgs_1[1]/1E9 - data_fbgs_1[2]/1E9, color="red", label="FBGS")
plt.scatter(data_rtd_2_cut2[0], data_fbgs_2[1]/1E9 - data_fbgs_2[2]/1E9, color="red")
plt.scatter(data_rtd_3_cut2[0], data_fbgs_3[1]/1E9 - data_fbgs_3[2]/1E9, color="red")
plt.scatter(data_rtd_4_cut2[0], data_fbgs_4[1]/1E9 - data_fbgs_4[2]/1E9, color="red")
plt.ylabel("WL Off. (pm)")
plt.title("S1 - S2")
plt.subplot(3,1,2)
plt.scatter(data_rtd_1_cut[0], data_o11_1[1] - data_o11_1[3], color="black", label="OPTICS11")
plt.scatter(data_rtd_2_cut[0], data_o11_2[1][3:] - data_o11_2[3][3:], color="black")
plt.scatter(data_rtd_3_cut[0], data_o11_3[1] - data_o11_3[3], color="black")
plt.scatter(data_rtd_4_cut[0], data_o11_4[1] - data_o11_4[3], color="black")
plt.scatter(data_rtd_1_cut2[0], data_fbgs_1[1]/1E9 - data_fbgs_1[3]/1E9, color="red", label="FBGS")
plt.scatter(data_rtd_2_cut2[0], data_fbgs_2[1]/1E9 - data_fbgs_2[3]/1E9, color="red")
plt.scatter(data_rtd_3_cut2[0], data_fbgs_3[1]/1E9 - data_fbgs_3[3]/1E9, color="red")
plt.scatter(data_rtd_4_cut2[0], data_fbgs_4[1]/1E9 - data_fbgs_4[3]/1E9, color="red")
plt.ylabel("WL Off. (pm)")
plt.title("S1 - S3")
plt.subplot(3,1,3)
plt.scatter(data_rtd_1_cut[0], data_o11_1[1] - data_o11_1[4], color="black", label="OPTICS11")
plt.scatter(data_rtd_2_cut[0], data_o11_2[1][3:] - data_o11_2[4][3:], color="black")
plt.scatter(data_rtd_3_cut[0], data_o11_3[1] - data_o11_3[4], color="black")
plt.scatter(data_rtd_4_cut[0], data_o11_4[1] - data_o11_4[4], color="black")
plt.scatter(data_rtd_1_cut2[0], data_fbgs_1[1]/1E9 - data_fbgs_1[4]/1E9, color="red", label="FBGS")
plt.scatter(data_rtd_2_cut2[0], data_fbgs_2[1]/1E9 - data_fbgs_2[4]/1E9, color="red")
plt.scatter(data_rtd_3_cut2[0], data_fbgs_3[1]/1E9 - data_fbgs_3[4]/1E9, color="red")
plt.scatter(data_rtd_4_cut2[0], data_fbgs_4[1]/1E9 - data_fbgs_4[4]/1E9, color="red")
plt.ylabel("WL Off. (pm)")
plt.title("S1 - S4")


plt.figure()
plt.subplot(2,2,1)
plt.scatter(data_o11_1[2], data_o11_1[2], color="black", label="OPTICS11")
plt.scatter(data_o11_2[2][3:], data_o11_2[2][3:], color="green")
plt.scatter(data_o11_3[2], data_o11_3[2], color="blue")
plt.scatter(data_o11_4[2], data_o11_4[2], color="orange")
plt.subplot(2,2,2)
plt.scatter(data_o11_1[2], data_o11_1[3], color="black", label="OPTICS11")
plt.scatter(data_o11_2[2][3:], data_o11_2[3][3:], color="green")
plt.scatter(data_o11_3[2], data_o11_3[3], color="blue")
plt.scatter(data_o11_4[2], data_o11_4[3], color="orange")
plt.subplot(2,2,3)
plt.scatter(data_o11_1[2], data_o11_1[4], color="black", label="OPTICS11")
plt.scatter(data_o11_2[2][3:], data_o11_2[4][3:], color="green")
plt.scatter(data_o11_3[2], data_o11_3[4], color="blue")
plt.scatter(data_o11_4[2], data_o11_4[4], color="orange")
plt.subplot(2,2,4)
plt.scatter(data_o11_1[2], data_o11_1[1], color="black", label="OPTICS11")
plt.scatter(data_o11_2[2][3:], data_o11_2[1][3:], color="green")
plt.scatter(data_o11_3[2], data_o11_3[1], color="blue")
plt.scatter(data_o11_4[2], data_o11_4[1], color="orange")
# plt.scatter(data_rtd_1_cut2[2], data_fbgs_1[4]/1E9, color="red", label="FBGS")
# plt.scatter(data_rtd_2_cut2[2], data_fbgs_2[4]/1E9, color="red")
# plt.scatter(data_rtd_3_cut2[2], data_fbgs_3[4]/1E9, color="red")
# plt.scatter(data_rtd_4_cut2[2], data_fbgs_4[4]/1E9, color="red")

results = [[], [], [], []]
data_rtd_optics = [np.mean(data_rtd_1_cut[2]), np.mean(data_rtd_2_cut[2]), np.mean(data_rtd_3_cut[2]), np.mean(data_rtd_4_cut[2])]
data_s1_optics = [np.mean(data_o11_1[1]), np.mean(data_o11_2[1]), np.mean(data_o11_3[1]), np.mean(data_o11_4[1])]
data_s2_optics = [np.mean(data_o11_1[2]), np.mean(data_o11_2[2]), np.mean(data_o11_3[2]), np.mean(data_o11_4[2])]
data_s3_optics = [np.mean(data_o11_1[3]), np.mean(data_o11_2[3]), np.mean(data_o11_3[3]), np.mean(data_o11_4[3])]
data_s4_optics = [np.mean(data_o11_1[4]), np.mean(data_o11_2[4]), np.mean(data_o11_3[4]), np.mean(data_o11_4[4])]
data_optics = [data_s1_optics, data_s2_optics, data_s3_optics, data_s4_optics]

error_rtd_optics = [np.std(data_rtd_1_cut[2]), np.std(data_rtd_2_cut[2]), np.std(data_rtd_3_cut[2]), np.std(data_rtd_4_cut[2])]
error_s1_optics = [np.std(data_o11_1[1]), np.std(data_o11_2[1]), np.std(data_o11_3[1]), np.std(data_o11_4[1])]
error_s2_optics = [np.std(data_o11_1[2]), np.std(data_o11_2[2]), np.std(data_o11_3[2]), np.std(data_o11_4[2])]
error_s3_optics = [np.std(data_o11_1[3]), np.std(data_o11_2[3]), np.std(data_o11_3[3]), np.std(data_o11_4[3])]
error_s4_optics = [np.std(data_o11_1[4]), np.std(data_o11_2[4]), np.std(data_o11_3[4]), np.std(data_o11_4[4])]
error_optics = [error_s1_optics, error_s2_optics, error_s3_optics, error_s4_optics]
for i in range(0,4):
    results[i].append("Run" + str(i+1))
    results[i].append(str(np.round((data_rtd_optics[i] - data_rtd_optics[0])*1000, 3)) +  " +- " + str(np.round(error_rtd_optics[i]*1000, 3)))
    for j in range(0,4):
        results[i].append(str(np.round((data_optics[j][i] - data_optics[j][0])*1E12, 3)) + " +- " + str(np.round(error_optics[j][i]*1E12, 3)))

results_fbgs = [[], [], [], []]
data_rtd_fbgs = [np.mean(data_rtd_1_cut2[2]), np.mean(data_rtd_2_cut2[2]), np.mean(data_rtd_3_cut2[2]), np.mean(data_rtd_4_cut2[2])]
data_s1_fbgs = [np.mean(data_fbgs_1[1]), np.mean(data_fbgs_2[1]), np.mean(data_fbgs_3[1]), np.mean(data_fbgs_4[1])]
data_s2_fbgs = [np.mean(data_fbgs_1[2]), np.mean(data_fbgs_2[2]), np.mean(data_fbgs_3[2]), np.mean(data_fbgs_4[2])]
data_s3_fbgs = [np.mean(data_fbgs_1[3]), np.mean(data_fbgs_2[3]), np.mean(data_fbgs_3[3]), np.mean(data_fbgs_4[3])]
data_s4_fbgs = [np.mean(data_fbgs_1[4]), np.mean(data_fbgs_2[4]), np.mean(data_fbgs_3[4]), np.mean(data_fbgs_4[4])]
data_fbgs = [data_s1_fbgs, data_s2_fbgs, data_s3_fbgs, data_s4_fbgs]

error_rtd_fbgs = [np.std(data_rtd_1_cut2[2]), np.std(data_rtd_2_cut2[2]), np.std(data_rtd_3_cut2[2]), np.std(data_rtd_4_cut2[2])]
error_s1_fbgs = [np.std(data_fbgs_1[1]), np.std(data_fbgs_2[1]), np.std(data_fbgs_3[1]), np.std(data_fbgs_4[1])]
error_s2_fbgs = [np.std(data_fbgs_1[2]), np.std(data_fbgs_2[2]), np.std(data_fbgs_3[2]), np.std(data_fbgs_4[2])]
error_s3_fbgs = [np.std(data_fbgs_1[3]), np.std(data_fbgs_2[3]), np.std(data_fbgs_3[3]), np.std(data_fbgs_4[3])]
error_s4_fbgs = [np.std(data_fbgs_1[4]), np.std(data_fbgs_2[4]), np.std(data_fbgs_3[4]), np.std(data_fbgs_4[4])]
error_fbgs = [error_s1_fbgs, error_s2_fbgs, error_s3_fbgs, error_s4_fbgs]
for i in range(0,4):
    results_fbgs[i].append("Run" + str(i+1))
    results_fbgs[i].append(str(np.round((data_rtd_fbgs[i] - data_rtd_fbgs[0])*1000, 3)) +  " +- " + str(np.round(error_rtd_fbgs[i]*1000, 3)))
    for j in range(0,4):
        results_fbgs[i].append(str(np.round((data_fbgs[j][i] - data_fbgs[j][0])*1E3, 3)) + " +- " + str(np.round(error_fbgs[j][i]*1E3, 3)))

col_names_o11 = ["Run", "Temp(mK): " + str(np.round(np.mean(data_rtd_1_cut[2]),3)),
                "S1 (pm): " + str(np.round(np.mean(data_o11_1[1])*1E9, 3)) + "nm",
                "S2 (pm): " + str(np.round(np.mean(data_o11_1[2])*1E9, 3)) + "nm",
                "S3 (pm): " + str(np.round(np.mean(data_o11_1[3])*1E9, 3)) + "nm",
                "S4 (pm): " + str(np.round(np.mean(data_o11_1[4])*1E9, 3)) + "nm"]
col_names_fbgs = ["Run", "Temp(mK): " + str(np.round(np.mean(data_rtd_1_cut2[2]),3)),
                "S1 (pm):" + str(np.round(np.mean(data_fbgs_1[1]), 4)) + "nm",
                "S2 (pm):" + str(np.round(np.mean(data_fbgs_1[2]), 3)) + "nm",
                "S3 (pm):" + str(np.round(np.mean(data_fbgs_1[3]), 3)) + "nm",
                "S4 (pm):" + str(np.round(np.mean(data_fbgs_1[4]), 3)) + "nm"]

comparison = [[],[],[],[]]
for i in range(0,4):
    comparison[i].append("Run" + str(i+1))
    comparison[i].append(str(np.round((data_rtd_fbgs[i] - data_rtd_optics[i])*1000, 3)) +  " +- " + str(np.round(error_rtd_fbgs[i]*1000, 3)))
    for j in range(0,4):
        comparison[i].append(str(np.round((data_fbgs[j][i] - data_optics[j][i]*1E9)*1E3, 3)))

print("OPTICS")
print(tabulate(results, headers=col_names_o11))
print("\nFBGS")
print(tabulate(results_fbgs, headers=col_names_fbgs))
print("\nComparison")
print(tabulate(comparison, headers=col_names_fbgs))