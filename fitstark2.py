""" fitstark2.py """
"""
Author: A.C. DeHart
Environnment: Python 2.7
Dependence: requires an out.dat file processed from main.py
Comment: This is the main file requiring only the path to a structured dat file in teh same directory as our data
RUN fitstark.py and stability.py AFTER!!!
This should be used to process future data sets under a different naming regieme
""" 
import os 
import calc_alpha as ca
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from iminuit import Minuit

"""
Double check expected signal
Check rates for excited S in elog

Scan    V_low   V_hi    low     hi
21      1.2     2       even?   odd?
29      1.2     3       even    odd
24      1.2     5       even    odd
25      1.2     10      even    odd Discontinuity at 13, but that's fine
28      1.2     13      even    odd
"""


"""MAIN"""
#NOTE: plotlyseries and plotseries will call either bindf() or rolldf(). rolldf() produces nice rolling average data while bindf() takes a more traditional aproach of just adding sequential sets of 3 data points. bindf() has issues being that it's series has fewer data points than everything else and needs special treatment when plotted. rolldf() is pretty much fucking fantastic on it's own though.

def main(data_path):
    #Path of scans.dat should be same as the scans in that directory
    path = os.path.split(os.path.abspath(data_path))[0]  
    data = pd.read_csv(data_path, sep = "\t", engine='python')  #Parsing file
    V_hi = data['Voltage'].values
    V_hi = [float(a.split(" ")[0]) for a in V_hi]
    Odd_C1 = data['C1'].values/2 # in bins
    Odd_C1 = [abs(a-53)*350 for a in Odd_C1] # in kHz
    Odd_C1_err = data['C1_err'].values/2
    Odd_C1_err = [a*350 for a in Odd_C1_err] # in kHz


    def squarelaw(x,p):        
        y=(p[0]+p[1]*(x/2.8575)**2) #[kHz] the (cm/kV)^2 should cancel
        return y


    def f(offset,k):
        Sum=0;
        p = [offset,k]
        nu = len(V_hi)-len(p); # nu (degrees of freedom) = N - r = number of points in our set - variables?
        print("V_hi",len(V_hi),"p",len(p),"nu",nu)
        for i in range(len(V_hi)):
            s = squarelaw(V_hi[i],p)
            if Odd_C1[i]==0:
                Sum+=pow((Odd_C1[i]-s)/(1),2)
            else:
                Sum+=pow((Odd_C1[i]-s)/(Odd_C1_err[i]),2)
            print(Odd_C1_err[i],Sum/nu)
        return Sum/nu #Normalized chi^2


    p = [-1000,100]  # [offset, k]

    m=Minuit(f, offset = p[0],  limit_offset = (-1E6,1E6),    error_offset = 5E2,
                k = p[1],       limit_k = (-1E3,1E3),       error_k = 50)
    m.migrad()

    pbest = [[]]*len(p);
    pbest[0]=m.values['offset']
    pbest[1]=m.values['k']


    print("Params", m.parameters)
    print("Args", m.args)
    print("Vals", m.values)
    print("Error", m.errors["k"])
    x1=np.arange(0,16,.1)
    y_fit = [squarelaw(i,pbest) for i in x1]

    chi2 = f(pbest[0],pbest[1])
    print("Chi Squared = " + str(chi2))
    plt.grid()
    #fn.pretty(series, voltage, binsize=False, Chi = chi2)

    Odd_C1 =[a-pbest[0] for a in Odd_C1]
    y_fit = [a-pbest[0] for a in y_fit ]
    plt.plot(x1, y_fit)
    plt.plot(V_hi, Odd_C1,'or')
    plt.errorbar(V_hi,Odd_C1,Odd_C1_err,visible=False)
    plt.xlim((0,max(x1)))
    plt.xlabel("Potential across Rb [kV]")
    plt.ylabel(r"Frequency Shift of the 5s $\rightarrow$ 6s Transition [kHz]")
    plt.text(min(V_hi),max(Odd_C1),"$\chi^2$ = " + "{0:.2f}".format(chi2))
    #plt.title("Stark Shift Measurements, k = " + "{0:.1f}".format(pbest[1]) + ", $\chi^2$ = " + "{0:.1f}".format(chi2))
    plt.title("Stark Shift Measurements, k = " + "{0:.0f}".format(pbest[1]) + "$ \pm $ " + "{0:.0f}".format(m.errors["k"]) + " [kHz cm$^2$ kV$^{-2}$]")#, $\chi^2$ = " + "{:f}".format(chi2))

    plt.show(block=False)

    ca.alpha(pbest[1],m.errors["k"])
    raw_input("You know what to do...")


"""INPUTS"""
#All you need is data and a 'readme' with relevant information in the same directory and it's file path.
data_path = '../exp/out.dat' #This contains rows and columns describing the scan number V_low and V_hi

main(data_path)


