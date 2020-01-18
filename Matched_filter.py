# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 21:18:19 2019

@author: Mustafa Biyikli & Katarzyna Lenard
"""
import numpy as np

class Matched_filter:   
    
    def __init__(self, coefficients):
        self.size = len(coefficients)
        self.coefficients = coefficients
        self.buffer = np.zeros(self.size)
        self.index = 0
        self.peaks = []; self.momentary_hr = []; self.thresholds = []
        self.first = 0; self.last = 0
    
    def hr_detector(self, data):
        self.buffer[self.index] = data
        self.output = 0
        # Slice the ring buffer into two parts and invert them
        self.temporary = [*self.buffer[0:self.index][::-1], *self.buffer[self.index:self.size][::-1]]
        # Multiply the full buffer with coefficients and add all = output
        self.output = np.sum(self.temporary * self.coefficients)
        
        if self.index == self.size - 1:
            self.index = 0
        else:
            self.index += 1    
        return self.output**2

    def threshold_finder(self, signal, Fs, threshold):
        self.count = 0
        for i in range(len(signal)):
            if (signal[i] > threshold-(0.10*threshold)) and (signal[i] < threshold+(0.10*threshold)) and (self.count > Fs/4):
                self.thresholds.append(i)
                self.count = 0
            elif (signal[i] == threshold) and len(self.thresholds) == 0:
                self.thresholds.append(i)
                self.count = 0
            self.count += 1
        for i in range(1, len(self.thresholds)):
            self.momentary_hr.append(self.thresholds[i] - self.thresholds[i-1])
        return self.thresholds, self.momentary_hr
        
    def peak_finder(self, signal, threshold):
        for i in range(len(signal)):
            if signal[i] > threshold:        
                self.last = i
            else:
                if (self.last == i-1) and (self.last > self.first):
                    for r in range(self.first, self.last):
                        if signal[r] == max(signal[self.first:self.last]):
                            self.max_index = r
                    self.peaks.append(self.max_index)
                self.first = i
        for i in range(1, len(self.peaks)):
            self.momentary_hr.append(self.peaks[i] - self.peaks[i-1])
        return self.peaks, self.momentary_hr