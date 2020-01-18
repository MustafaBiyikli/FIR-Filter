# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 10:52:31 2019

@author: Mustafa Biyikli & Katarzyna Lenard
"""
import numpy as np; import matplotlib.pyplot as plt; import time
# Import our modules
import Matched_filter; import Wavelets

time_total = time.time()    # This will be used to print the total execution time

####                            ####
####    Testing the wavelets    ####
####                            ####

Fs = 1000;              # Sampling rate [Hz]
M = 2000;               # This was used for the FIR Filter and is needed here
M_template = int(Fs/4); # Number of taps for the template
y = np.loadtxt('ecg_clean.dat')
T = np.linspace(0,  len(y)/Fs, num=len(y))  # Time [s]

wavelet = Wavelets.Wavelet(M_template) # Our module, see Wavelets.py for derivations

""" MORLET WAVELET """
morlet = wavelet.Morlet()
plt.subplots(); plt.subplot(231); plt.plot(morlet, linewidth=0.8, color='k'); plt.title("Morlet Wavelet")
plt.suptitle('Wavelet Performance Comparison')
plt.ylabel('Amplitude'); plt.xlabel('Number of taps')

d = Matched_filter.Matched_filter(morlet)
detector = np.empty(len(y))
for i in range(len(y)):
    detector[i] = d.hr_detector(y[i])
plt.subplot(234); plt.plot(T, detector, linewidth=0.8, color='k')
plt.ylabel('Amplitude'); plt.xlabel('Time [s]')

""" MEXICAN HAT WAVELET """
mexican_hat = wavelet.Mexican_Hat()
plt.subplot(232); plt.plot(mexican_hat, linewidth=0.8, color='k'); plt.title("Mexican Hat Wavelet")
plt.ylabel('Amplitude'); plt.xlabel('Number of taps')

d = Matched_filter.Matched_filter(mexican_hat)
detector = np.empty(len(y))
for i in range(len(y)):
    detector[i] = d.hr_detector(y[i])
plt.subplot(235); plt.plot(T, detector, linewidth=0.8, color='k')
plt.ylabel('Amplitude'); plt.xlabel('Time [s]')

""" GAUSSIAN DERIVATIVE """
gaussian = wavelet.Gaussian()
plt.subplot(233); plt.plot(gaussian, linewidth=0.8, color='k'); plt.title("Gaussian Derivative")
plt.ylabel('Amplitude'); plt.xlabel('Number of taps')

time1 = time.time()
d = Matched_filter.Matched_filter(gaussian)
detector = np.empty(len(y))
for i in range(len(y)):
    detector[i] = d.hr_detector(y[i])
plt.subplot(236); plt.plot(T, detector, linewidth=0.8, color='k')
plt.ylabel('Amplitude'); plt.xlabel('Time [s]')
plt.subplots_adjust(left=0.05, right=0.95, top=0.9, bottom=0.1, wspace=0.3, hspace=0.3)
# Time the Matched Filter
print('{} {} {}'.format('Matched Filter; took', time.time()-time1, 'seconds'))

""" HEARTRATE DETECTION w/GAUSSIAN """

# Matched filter heartrate detection
thresholds, momentary_hr = d.threshold_finder(detector, Fs, threshold=1.25)
thresholds_time_domain = np.empty(len(thresholds))

# Get peak indexes in time domain
for i in range(len(thresholds)):
    thresholds_time_domain[i] = thresholds[i]/Fs

# Calculate the momentary heart rate in bpm
for i in range(len(momentary_hr)):
    momentary_hr[i] = 60/(momentary_hr[i]/Fs)

# Plot the mathced filter output w/detections
plt.subplots(); plt.plot(T, detector, linewidth=0.8, color='k'); plt.plot(thresholds_time_domain, detector[thresholds], 'ro', markersize=3)
plt.title('Matched Filter Output'); plt.ylabel('Amplitude'); plt.xlabel('Time [s]')

# Plot the momentary heartrate over the entire signal
plt.subplots();plt.step(np.linspace(1, len(momentary_hr), num=len(momentary_hr)),momentary_hr, linewidth=0.8, color='k')
plt.ylabel('momentary heart rate [beats/min]');plt.xlabel('Beat Index');plt.xlim(1, len(momentary_hr))

print('{} {} {}'.format('Total Execution; took', time.time()-time_total, 'seconds'))
plt.show()