# FIR-Filter
FIR filter written in Python 3

See the Report.pdf file for an in-depth explanation.

Generate your ideal frequency response and provide the FIR_filter with the coefficients and dofilter function with the data. See ecg_filter.py for an example usage of 50Hz mains interference removal (and its harmonics). Sample code uses a hanning window due to its narrow transition width. Use blackman window for improved noise attenuation.

Sample .dat files provided for both raw and filtered signals as an example.

Matched_filter.py has peak and threshold finder functions for rate detection. See hr_detect.py for an example. Custom templates may be used, this project uses wavelets. Samples for Morlet, Mexican Hat and Gaussian wavelets provided in Wavelets.py.
