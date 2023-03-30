import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

path_to_data = "/eos/user/j/jcapotor/FBGdata/Data/camara_climatica/TEST_minus70_prog31.CSV"

data = pd.read_csv(path_to_data, sep=";", header=None, skiprows=1, decimal=",")
data[0] = data[0].apply(lambda x: np.round(x*24*3600, 0))

plt.figure()
plt.title("Climatic chamber: Temperature Profile")
plt.scatter(data[0] - data[0][0], data[4])
plt.xlabel("Time (s)")
plt.ylabel("Temperature (ºC)")
plt.grid("on")
plt.show(block=True)