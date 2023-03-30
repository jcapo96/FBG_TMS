# -*- coding: utf-8 -*-
"""
Created on Wed May 03 15:28:58 2017

@author: john.odowd
"""

'''
FemtoSense packages each sweep of the laser into one packet.
The packet is saved in binary format (little endian)

The packet format is:
1) PacketSize (I32, 4 Bytes)
   This is the number of Bytes of spectral data in a single sweep
2) Timestamp (U64, 8 Bytes)
   seconds since the epoch 01/01/1900 00:00:00.00 UTC (using the Gregorian calendar and ignoring leap seconds),
3) Validity flag (I32, 4 Bytes) : 0=data valid 		
4) Channel No. (I32, 4 Bytes)
5) Start wavelength, nm (dBl, 8 Bytes) 
6) Stop wavelength, nm (dBl, 8 Bytes)
7) No. of wavelength points (I32, 4 Bytes)
8) Spectral data, (I16, 2 Bytes)
   The amount of spectral data points is PacketSize/2
   Each Spectral data point is seperated by 1 pm
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

'''Open File'''
#SpecFile='C:/temp/test_sensor1'

def plot_spectrums(filename, color):
   FileId=open(filename,'rb')#open file to be read
   #start_counter=(np.fromfile(CounterFile, dtype='>u4', count=1))[0]


   '''Read single sweep of data'''
   sweeps = []
   persistentRead = True
   cnt = 0
   while persistentRead == True:
      try:
         sweep = {}
         sweep['PacketSize'] = (np.fromfile(FileId, dtype='<i4', count=1))
         sweep['Timestamp'] = (np.fromfile(FileId, dtype='<u8', count=1))
         sweep['Validity flag'] = (np.fromfile(FileId, dtype='<i4', count=1))
         sweep['Channel No.'] = (np.fromfile(FileId, dtype='<i4', count=1))
         sweep['Fibre No.'] = (np.fromfile(FileId, dtype='<i4', count=1))
         sweep['Start wavelength'] = (np.fromfile(FileId, dtype='<d', count=1))
         sweep['Stop wavelength'] = (np.fromfile(FileId, dtype='<d', count=1))
         sweep['No. of wavelength points']=(np.fromfile(FileId, dtype='<i4', count=1))
         sweep['Spectral data']=(np.fromfile(FileId, dtype='<i2', count=sweep['No. of wavelength points'][0]))
         sweep['Wavelength Axis (nm)']=np.linspace(sweep['Start wavelength'],sweep['Stop wavelength'],int(sweep['No. of wavelength points']))
         sweeps.append(sweep)
         cnt += 1
         print(cnt)
      except:
         persistentRead = False


   persistentDraw = True
   '''Plot Data'''
   plt.figure('Spectra Data')
   for cnt in range(len(sweeps)):
      if cnt == 35:
         break
      if sweeps[cnt]["Channel No."][0] != 0:
         continue
      print(sweeps[cnt])
      plt.plot(sweeps[cnt]['Wavelength Axis (nm)'],sweeps[cnt]['Spectral data']/np.max(sweeps[cnt]['Spectral data']), ".", color=color)
      plt.xlabel('Wavelength (nm)')
      plt.ylabel('Amplitude (Arb. units)')
      cnt += 1

SpecFile1='/eos/user/j/jcapotor/LabData/Heater_Tests/09012023/'
plot_spectrums(SpecFile1, "blue")
plt.show()