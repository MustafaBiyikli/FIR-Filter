# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 13:56:45 2019

@author: Mustafa Biyikli & Katarzyna Lenard
"""
import numpy as np

class Wavelet:
    def __init__(self, number_of_taps):
        self.M = number_of_taps
    def Morlet(self):
        mor1 = np.empty(self.M)
        mor1_inversed = np.empty(self.M)
        for t in range(-int(self.M/2), int(self.M/2), 1):
            mor1[t] = np.exp(-(t**2)/2)*np.cos(5*t)
        mor1_inversed[0:int(int(self.M/2))] = mor1[int(int(self.M/2)):self.M]
        mor1_inversed[int(int(self.M/2)):self.M] = mor1[0:int(int(self.M/2))]        
        return mor1_inversed

    def Mexican_Hat(self):
        mex_hat = np.empty(self.M)
        mex_hat_inversed = np.empty(self.M)
        for t in range(-int(self.M/2), int(self.M/2), 1):
            mex_hat[t] = (2/(3**(1/2)*(np.pi**(1/4))))*np.exp(-(t**2)/2)*(1-t**2)
        mex_hat_inversed[0:int(int(self.M/2))] = mex_hat[int(int(self.M/2)):self.M]
        mex_hat_inversed[int(int(self.M/2)):self.M] = mex_hat[0:int(int(self.M/2))]
        return mex_hat_inversed
    
    def Gaussian(self, C=1):
        gaus = np.empty(self.M)
        gaus_inversed = np.empty(self.M)
        for t in range(-int(self.M/2), int(self.M/2), 1):
            gaus[t] = C*np.exp(-(t**2))
        gaus_inversed[0:int(int(self.M/2))] = gaus[int(int(self.M/2)):self.M]
        gaus_inversed[int(int(self.M/2)):self.M] = gaus[0:int(int(self.M/2))]
        return gaus_inversed
