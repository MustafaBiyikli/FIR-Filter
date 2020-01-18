# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 13:47:39 2019

@author: Mustafa Biyikli & Katarzyna Lenard
"""

import numpy as np; import matplotlib.pyplot as plt; import time
# Import our modules
import FIR_filter

time_total = time.time()    # This will be used to print the total execution time
# Load the data, select time & data arrays & set some variables
data = np.loadtxt('ecg.dat')
ecg = data[:, 2] * ((1.325*2)/2**24)    # Potential difference [mV]
T = data[:, 0] / 1000                   # in seconds [s]
# Plot the raw data
plt.subplots(); plt.plot(T, ecg, linewidth=0.8, color='k')
plt.title('Raw ECG Signal [Einthoven II]'); plt.ylabel('Amplitude [mV]'); plt.xlabel('Time [s]')

M = 2000        # Number of Taps (double Fs)
Fs = 1000       # Sampling rate [Hz]

# Ideal Frequency Response
X = np.ones(M)
for k in np.arange(45, int(Fs/2), 100):
    k1 = int(k/Fs*M); k2 = int((k+10)/Fs*M) # A moving frequency range of 10Hz
    X[k1:k2+1] = 0                          # Set the ranges in real part to 0
    X[M-k2:M-k1+1] = 0                      # Set the complex conjgate ranges to 0

x = np.fft.ifft(X)
x = np.real(x)

# Slice & Swap & Shift into positive time
h = np.zeros(M)
h[0:int(M/2)] = x[int(M/2):M]
h[int(M/2):M] = x[0:int(M/2)]

# Window function
h = h * np.hanning(M)   # Choice justified in the report 

# DC Removal (sharp DC removal response)
X = np.fft.fft(h)
X[0:int(0.5/Fs*M)] = 0
h = np.real(np.fft.ifft(X))

time1 = time.time()     # Seconds passed since epoch (1/1/1970 00:00:00)                      

# FIR Filter usage
f = FIR_filter.FIR_filter(h)
y = np.empty(len(ecg))
for i in range(len(ecg)):
    y[i] = f.dofilter(ecg[i])

y = y[M:]
plt.subplots(); plt.plot(T[M:], y, linewidth=0.8, color='k')
plt.title('FIR Filter Output'); plt.ylabel('Amplitude [mV]'); plt.xlabel('Time [s]')
# Time the FIR Filter
print('{} {} {}'.format('FIR Filter; took', time.time()-time1, 'seconds'))
np.savetxt('ecg_clean.dat', y)

print('{} {} {}'.format('Total Execution; took', time.time()-time_total, 'seconds'))
plt.show()



