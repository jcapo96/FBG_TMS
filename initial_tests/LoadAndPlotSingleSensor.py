import numpy as np
import matplotlib.pyplot as plt
import os

#Location of sensor file on disk
currfolder='/Users/jcapo/Documents/FBGS/Data/InterrogatorTests/20221222/'
sname='17_spectrum_OPTICS.txt'

#open sensor data file
current_file=str(currfolder+sname)
File_to_read=open(current_file,'rb')#open file to be read

plt.figure()
#load first 1000 values from file
peakOfInterest=(np.fromfile(File_to_read, dtype=np.int32))#load data from file
peakOfInterest=(np.memmap(File_to_read, dtype=np.int32, mode="r"))#load data from file
print(peakOfInterest[::2])

#Plot sensor data
plt.plot(peakOfInterest)
File_to_read.close()
plt.show(block=True)

