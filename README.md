This repository should contain code I've developed through out my research at TRIUMF.

All data files were stored in a different directory than these scripts, so attempts to reproduce the results of calling the scripts bellow will require the raw data to be placed in the directory ../exp/ relative to the scripts themselves.

fn.py
This script contains several useful functions for processing data from this project and is called by main.py

main.py
This is the primary script to fit a double lorentzian curve on our raw data. The raw data is a mess, so the file scans.dat lists the useful data and acts as the header information for those scans. After displaying the resulting fit of each scan, the resulting fitting parameters are appended to out.dat for later use

fitstark2.py
This script fits an exponential curve to Stark-shift data. It first identifies and pulls data points from the out.dat file produced by main.py. After the fit, the plot is displayed along with the resulting reduced chi squared of the fit.

binsum7.py
On the local machines in the lab, this script will find the newest directory with data in it and actively displays the cumulative sum of the latest scan as well as binning the scan per initial user input.
