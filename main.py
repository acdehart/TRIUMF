""" main.py """
"""
Author: A.C. DeHart
Environnment: Python 2.7
Dependence: requires fn.py as well as the raw data files and scans.dat which contains necessary header information for parsing.
Comment: This is the main file requiring only the path to a structured dat file in teh same directory as our data
RUN fitstark.py and stability.py AFTER!!!
This should be used to process future data sets under a different naming regieme
""" 

import os 
import fn
import pandas as pd
import numpy as np
import glob

"""
Fake data log so far:

	Scan	Voltage	C1	C1_err
0	scan7	2 kV	67.2054474619	29.6082962222
1	scan19	2 kV	59.5471778939	29.6650778858
2	scan12	5 kV	59.3579755971	15.2875269837
3	scan14	5 kV	72.2341396919	23.1515131326
4	scan18	5 kV	59.5479826303	4.85580644103
5	scan20	8 kV	55.503137393	3.29525945204
6	scan6	10 kV	50.6591848735	2.40956959767
7	scan9	12 kV	47.5724499543	5.00762475977
8	scan10	12 kV	47.164596016	3.15378700303
9	scan15	15 kV	37.1837378905	3.23732279316
"""


"""MAIN"""
#NOTE: plotlyseries and plotseries will call either bindf() or rolldf(). rolldf() produces nice rolling average data while bindf() takes a more traditional aproach of just adding sequential sets of 3 data points. bindf() has issues being that it's series has fewer data points than everything else and needs special treatment when plotted. rolldf() is pretty much fucking fantastic on it's own though.

def main(data_path, single = "",key= 'sum', raw = True, plot=True):
    #Path of scans.dat should be same as the scans in that directory
    path = os.path.split(os.path.abspath(data_path))[0]
    data = pd.read_csv(data_path, sep = ", ", engine='python')  #Parsing file

    os.chdir(path)
    file_list = glob.glob('*.txt')

    data_list = []
    position1 = np.zeros(len(data))
    error1    = np.zeros(len(data))
    #for dat in data['Scan'].values:
    for i in range(len(data)):
        #i=4
        dat = data.iloc[i]['Scan']
        volt = data.iloc[i]['Voltage']
        for txt in file_list:
            if dat in txt and '_0' in txt:
                data_list.append(txt)
        m = fn.mfit(dat,data_list,volt,path,raw,plot)  
        position1[i] = np.mean([m.values['C1'], 200-m.values['C2']])
        error1[i] = (m.errors['C1']**2 + m.errors['C2']**2)**.5/2
        data_list = []
        print(position1[i],error1[i])        
        #raw_input("Yep")
        #break
    data['C1'] = position1
    data['C1_err'] = error1

    #with open(os.path.join(path,file_out),'w') as outfile:
    data.to_csv("out.dat", sep = "\t"); print("Saved results to 'out.dat'")
    raw_input("Yep")

    #refsdf = fn.makedf(meas_list,path)

    #print(refsdf.head())
    

    """
    for index in range(len(data)):    
        if single != "":
            index = single
        A = data.iloc[index]['Scan'],data.iloc[index]['Voltage'],data.iloc[index]['Time'],data.iloc[index]['Type']
        print(A)
        
        for item in range(len(data)):
            if data.iloc[item]['Type'] == 'R':
                print("yea!")
            
        file_list = fn.makelist(series,'odd',path) #High
        resultsodd = mfit(series,file_list,high,path,raw,plot)
        file_list = fn.makelist(series,'even',path) #Low
        resultseven = mfit(series,file_list,low,path,raw,plot)
    

        elif key == 'min':
            m = fn.plotminseries(A[0],A[1],A[2],path,raw,plot);odd =m[0];even=m[1]
            even_C1[index] = even.values['C1']
            odd_C1[index]  = odd.values['C1']
            even_C1_err[index] = even.errors['C1']
            odd_C1_err[index]  = odd.errors['C1']
            even_C2[index] = even.values['C2']
            odd_C2[index]  = odd.values['C2']
            even_C2_err[index] = even.errors['C2']
            odd_C2_err[index]  = odd.errors['C2']
        data['Even_C1']     = even_C1
        data['Even_C1_err'] = even_C1_err
        data['Odd_C1']      = odd_C1
        data['Odd_C1_err']  = odd_C1_err
        data['Even_C2']     = even_C2
        data['Even_C2_err'] = even_C2_err
        data['Odd_C2']      = odd_C2
        data['Odd_C2_err']  = odd_C2_err
        
        if single !=  "":
            return;
    #with open(os.path.join(path,file_out),'w') as outfile:
    data.to_csv("out.dat", sep = "\t"); print("Saved results to 'out.dat'")
    
    """
    #raw_input("Hit return to close all\n")
    return;





"""INPUTS"""
#All you need is data and a 'readme' with relevant information in the same directory and it's file path.
data_path = '../exp/scans.dat' #This contains rows and columns describing the scan number V_low and V_hi
index = "" #this requests a plot of a specific line in the the .dat file. leave as "" if you want to display all. 
raw = True
key = 'min'# 'sum', 'roll', 'bin', 'fit', 'min'

main(data_path, index, key='mfit', raw = False, plot=True)


