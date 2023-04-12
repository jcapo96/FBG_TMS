import sys
sys.path.insert(1, '../../ana_tools')
import getters, tools
import matplotlib.pyplot as plt
import numpy as np

plateaus = getters.get_plateaus()

path_to_data = "/eos/user/j/jcapotor/FBGana/camara_climatica/FebruaryRuns/"
dates= ["20230221","20230222","20230223","20230224"]

data = getters.get_raw_data(path_to_data+"20230221"+"/", filetype="peaks", pol="Av").sort_values(by="Timestamp").reset_index(drop=True)
t0 = data["Timestamp"][0]

data = data.loc[(data["Wav1-1"]>1.45e-6) & (data["Wav1-3"]>1.45e-6) & (data["Wav1-4"]>1.45e-6) & (data["Wav1-5"]>1.45e-6)]
plt.figure(figsize=(8,8))
plt.subplot(2,2,1)
plt.plot(data["Timestamp"]-t0, data["Wav1-1"] - data["Wav1-1"][0], label="Wav1-1")
plt.plot(data["Timestamp"]-t0, data["Wav1-2"] - data["Wav1-2"][0], label="Wav1-2")
plt.plot(data["Timestamp"]-t0, data["Wav1-3"] - data["Wav1-3"][0], label="Wav1-3")
plt.plot(data["Timestamp"]-t0, data["Wav1-4"] - data["Wav1-4"][0], label="Wav1-4")
plt.plot(data["Timestamp"]-t0, data["Wav1-5"] - data["Wav1-5"][0], label="Wav1-5")
plt.legend()

data = getters.get_raw_data(path_to_data+"20230222"+"/", filetype="peaks", pol="Av").sort_values(by="Timestamp").reset_index(drop=True)
t0 = data["Timestamp"][0]
plt.subplot(2,2,2)
data = data.loc[(data["Wav1-1"]>1.45e-6) & (data["Wav1-3"]>1.45e-6) & (data["Wav1-4"]>1.45e-6) & (data["Wav1-5"]>1.45e-6)]
plt.plot(data["Timestamp"]-t0, data["Wav1-1"] - data["Wav1-1"][0], label="Wav1-1")
plt.plot(data["Timestamp"]-t0, data["Wav1-2"] - data["Wav1-2"][0], label="Wav1-2")
plt.plot(data["Timestamp"]-t0, data["Wav1-3"] - data["Wav1-3"][0], label="Wav1-3")
plt.plot(data["Timestamp"]-t0, data["Wav1-4"] - data["Wav1-4"][0], label="Wav1-4")
plt.plot(data["Timestamp"]-t0, data["Wav1-5"] - data["Wav1-5"][0], label="Wav1-5")
plt.legend()

data = getters.get_raw_data(path_to_data+"20230223"+"/", filetype="peaks", pol="Av").sort_values(by="Timestamp").reset_index(drop=True)
t0 = data["Timestamp"][0]
plt.subplot(2,2,3)
data = data.loc[(data["Wav1-1"]>1.45e-6) & (data["Wav1-3"]>1.45e-6) & (data["Wav1-4"]>1.45e-6) & (data["Wav1-5"]>1.45e-6)]
plt.plot(data["Timestamp"]-t0, data["Wav1-1"] - data["Wav1-1"][0], label="Wav1-1")
plt.plot(data["Timestamp"]-t0, data["Wav1-2"] - data["Wav1-2"][0], label="Wav1-2")
plt.plot(data["Timestamp"]-t0, data["Wav1-3"] - data["Wav1-3"][0], label="Wav1-3")
plt.plot(data["Timestamp"]-t0, data["Wav1-4"] - data["Wav1-4"][0], label="Wav1-4")
plt.plot(data["Timestamp"]-t0, data["Wav1-5"] - data["Wav1-5"][0], label="Wav1-5")
plt.legend()

# data = getters.get_raw_data(path_to_data+"20230224"+"/", filetype="peaks", pol="Av").sort_values(by="Timestamp").reset_index(drop=True)
# t0 = data["Timestamp"][0]
# plt.subplot(2,2,4)
# data = data.loc[(data["Wav1-1"]>1.45e-6) & (data["Wav1-3"]>1.45e-6) & (data["Wav1-4"]>1.45e-6) & (data["Wav1-5"]>1.45e-6)]
# plt.plot(data["Timestamp"]-t0, data["Wav1-1"] - data["Wav1-1"][0], label="Wav1-1")
# plt.plot(data["Timestamp"]-t0, data["Wav1-2"] - data["Wav1-2"][0], label="Wav1-2")
# plt.plot(data["Timestamp"]-t0, data["Wav1-3"] - data["Wav1-3"][0], label="Wav1-3")
# plt.plot(data["Timestamp"]-t0, data["Wav1-4"] - data["Wav1-4"][0], label="Wav1-4")
# plt.plot(data["Timestamp"]-t0, data["Wav1-5"] - data["Wav1-5"][0], label="Wav1-5")
# plt.legend()

plt.show(block=True)