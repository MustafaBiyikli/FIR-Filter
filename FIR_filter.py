# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 21:16:29 2019

@author: Mustafa Biyikli & Katarzyna Lenard
"""
import numpy as np

class FIR_filter:   
    
    def __init__(self, coefficients):
        self.size = len(coefficients)
        self.coefficients = coefficients
        self.buffer = np.zeros(self.size)
        self.index = 0
    
    def dofilter(self, data):
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
        return self.output