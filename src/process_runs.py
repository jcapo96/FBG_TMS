import read_files
import pandas as pd
import json
import warnings
from tables import NaturalNameWarning
warnings.filterwarnings('ignore', category=NaturalNameWarning)
import sys

path_to_data = sys.argv[1]
subfolder = path_to_data.split("/")[8]
subsubfolder = path_to_data.split("/")[9]
path_to_save_folder = "/eos/user/j/jcapotor/FBGana/camara_climatica/" + subfolder + "/" + subsubfolder + "/"
print(path_to_save_folder)

print("Processing " + path_to_data)

def get_topology(path_to_data):
    topology = "topology.json"
    f = open(path_to_data+topology)
    data = json.load(f)
    n_channels = len(data["Channels"])
    wl_positions = []
    chan_sensors = []
    channels = []
    for chan in range(n_channels):
        n_sensors = len(data["Channels"][chan]["fibers"][0]["sensors"])
        if n_sensors <= 0:
            continue
        channels.append(data["Channels"][chan]["channelId"])
        chan_positions = []
        chan_sensors.append(n_sensors)
        for sens in range(n_sensors):
            wl0=(data["Channels"][chan]["fibers"][0]["sensors"][sens]["start"])
            wlf=(data["Channels"][chan]["fibers"][0]["sensors"][sens]["end"])
            wl = int((wl0+wlf)/2)
            chan_positions.append(wl)
        wl_positions.append(chan_positions)
    return channels, chan_sensors, wl_positions

#this comes out from the topology file
channels, n_sensors, wl_positions = get_topology(path_to_data=path_to_data)

list_of_files = pd.read_csv(path_to_data+"list_of_files.txt", header=None, names=["Filename"])
print(list_of_files)
for index, file in list_of_files.iterrows():
    filename = file["Filename"].lower()
    print(filename)
    try:
        if filename.split("_")[0] == "spectrums":
            print("Processing Spectrums")
            specs = read_files.process_spectrums(
                path_to_data=path_to_data,
                filename=filename,
                path_to_save_folder=path_to_save_folder,
                channels=channels,
                n_sensors=n_sensors,
                wl_positions=wl_positions
            )
        elif filename.split("_")[0] == "peaks":
            print("Processing Peaks")
            peaks = read_files.process_peaks(
                path_to_data=path_to_data,
                filename=filename,
                path_to_save_folder=path_to_save_folder,
                channels=channels,
                n_sensors=n_sensors
            )
        elif filename.split("_")[0] == "temperature":
            print("Processing Temperature")
            temperature = read_files.process_temperature(
                path_to_data=path_to_data,
                path_to_save_folder=path_to_save_folder,
                filename=filename
            )
        elif filename.split("_")[0] == "humidity":
            print("Processing Humidity")
            humidity = read_files.process_humidity(
                path_to_data=path_to_data,
                filename=filename,
                path_to_save_data=path_to_save_folder
            )
    except:
        print("Failed for file: " + filename)
        continue
