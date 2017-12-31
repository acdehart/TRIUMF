"""
This file should contain a list of functions useful for organizing and plotting data.
"""
import fn
import glob
import math
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from scipy.optimize import leastsq # Levenberg-Marquadt Algorithm #
from iminuit import Minuit

"""
makelist()

INPUT: scan series, e.g. "scan2", optional description of 'odd' or 'even' files, and the path to the files
OUTPUT: list of strings of all files sharing the series name within the path used
EXAMPLES:
    fn.makelist('scan25','odd','./')
    fn.makelist('scan25')
"""

def makelist(series, numbers='', path='./'):
    os.chdir(path)
    file_list = glob.glob('*.txt')
    file_list = [item for item in file_list if series in item]
    file_list = [item for item in file_list if "_0" in item]
    nums = [os.path.splitext(item)[0] for item in file_list]
    nums = [item.split("_")[1] for item in nums]
    nums = [int(item) for item in nums]

    if numbers == 'even':
        even = []
        for i in range(len(file_list)):
            if nums[i]%2 is 0:
                even.append(file_list[i])
        file_list = even

    elif numbers == 'odd':
        odd = []
        for i in range(len(file_list)):
            if nums[i]%2 is not 0:
                odd.append(file_list[i])
        file_list = odd

    return file_list;



"""
sumlist()

INPUT: Array of file names, path to files
OUTPUT: data frame containing data from files and an additional column 'sum' with the row sum of all data
EXAMPLE: 
    fn.makedf(file_list)
"""

def makedf(file_list, path='./'):
    os.chdir(path)
    data = pd.DataFrame([])

    for file_path in file_list:
        data[file_path] = pd.read_csv(file_path, sep = '\n', skiprows=5, names =[file_path])
    
    data['sum'] = data.sum(axis=1)
#    data['bin'] = range(1,201)
    return data;




"""
bindf()

INPUT: DataFrame including a "sum" column, and the number of bins to be absorbed into one bin
OUTPUT: DataFrame with a value and position of the binned result relative to the original mapping
EXAMPLE: fn.bindf()

"""
def bindf(dataframe, bin_size):
    array = dataframe['sum'].values
    data_binned = []
    for i in range(0,len(array)/bin_size):
        a=sum((array[i*bin_size:(i+1)*bin_size]))
        data_binned=np.append(data_binned,a)
    x_vals = [x*bin_size for x in range(0,len(data_binned))]    
    data_binned = [y/bin_size for y in data_binned]

    df = pd.DataFrame({'x' : x_vals, 'binned' : data_binned})
    return df;



"""
rolldf()

INPUT: DataFrame including a "sum" column, and the number of bins to be absorbed into one bin
OUTPUT: DataFrame with a value and position of the binned result relative to the original mapping
EXAMPLE: fn.bindf()

"""
def rolldf(dataframe, bin_size = 6):
    array = dataframe['sum'].values
    data_binned = []
    for i in range(len(array)):
        if i in range(int(bin_size/2)):
            A = array[0:(i+int(bin_size/2))]
        elif i in range(len(array)-int(bin_size/2),len(array)):
            A = array[(i-int(bin_size/2)):len(array)-int(bin_size/2)]
        else:
            A = array[(i-int(bin_size/2)):(i+int(bin_size/2))]
        a = sum(A)
        elements = len(A)
        data_binned=np.append(data_binned,float(a/elements))
#    x_vals = [x*bin_size for x in range(0,len(data_binned))]    
#    data_binned = [y/bin_size for y in data_binned]

#    df = pd.DataFrame({'rolled' : data_binned})
    dataframe['rolled'] = pd.DataFrame(data_binned)
#    print(dataframe)
#    print(dataframe.shape)
    return dataframe;



"""
plotbinseries()

INPUT: String of series name, string describing low potential (even), string describing high potential (odd)
OPTIONAL INPUT: Int bin size, boolian as to whether or not to show plot
OUTPUT: Returns nothing, but shows the separated even and odd plots for a series of scans
EXAMPLE = fn.plotseries('scan28','1.2 kV', '13 kV') 
"""
def plotbinseries(series,low,high,binsize,path='./',raw=True):

    file_list = fn.makelist(series,'even',path)
    scanE = fn.makedf(file_list,path) #dataframe with even data
    scanEB = fn.bindf(scanE,binsize) #dataframe with binned even data 

    file_list = fn.makelist(series,'odd',path)
    scanO = fn.makedf(file_list,path) #dataframe with odd data 
    scanOB = fn.bindf(scanO,binsize) #dataframe with binned odd data


    if raw:
        ax = scanO.plot(legend = False)
        scanOB.plot(ax=ax, x = 'x', y = 'binned')
        fn.pretty(series,high,binsize)
        plt.show(block=False);
        ax = scanE.plot(legend = False)
        scanEB.plot(ax=ax, x = 'x', y = 'binned')
        fn.pretty(series,low,binsize)
        plt.show(block=False);
    else:# This is buggy. When raw == False, plots will print one at a time, not together.
        ax = scanO['sum'].plot(legend = False)
        scanOB.plot(ax=ax, x = 'x', y = 'binned')
        fn.pretty(series,high,binsize)  
        plt.show(block=True)
        ax = scanE['sum'].plot(legend = False)
        scanEB.plot(ax=ax, x = 'x', y = 'binned')
        fn.pretty(series,low,binsize)  
        plt.show(block=False);

    return;




"""
plotrollseries() -> Same as plotseries() but uses the plotly library

INPUT: String of series name, string describing low potential (even), string describing high potential (odd)
OPTIONAL INPUT: Int bin size, boolian as to whether or not to show plot
OUTPUT: Returns nothing, but shows the separated even and odd plots for a series of scans
EXAMPLE = fn.plotseries('scan28','1.2 kV', '13 kV') 
"""
def plotrollseries(series,low,high,binsize,path='./',raw=True):

    file_list = fn.makelist(series,'even',path) #Low 
    scanE = fn.makedf(file_list,path) #dataframe with even data
    scanE = fn.rolldf(scanE,binsize) #dataframe with rolled even data 
    
    file_list = fn.makelist(series,'odd',path) #High
    scanO = fn.makedf(file_list,path) #dataframe with odd data 
    scanO = fn.rolldf(scanO,binsize) #dataframe with rolled odd data

    if not raw:
        scanO = scanO[['sum','rolled']].copy()    
        scanE = scanE[['sum','rolled']].copy()    

    ax = scanO.plot(legend = False)
    fn.pretty(series,high,binsize)      
    plt.show(block = False);
    ax2 = scanE.plot(legend = False)
    fn.pretty(series,low,binsize)      
    plt.show(block = False);
    return scanO;



"""
plotsumseries() -> Same as plotseries() but uses the plotly library

INPUT: String of series name, string describing low potential (even), string describing high potential (odd)
OPTIONAL INPUT: Int bin size, boolian as to whether or not to show plot
OUTPUT: Returns nothing, but shows the separated even and odd plots for a series of scans
EXAMPLE = fn.plotseries('scan28','1.2 kV', '13 kV') 
"""
def plotsumseries(series,low,high,path='./',raw=True):

    file_list = fn.makelist(series,'even',path) #Low 
    scanE = fn.makedf(file_list,path) #dataframe with even data
    
    file_list = fn.makelist(series,'odd',path) #High
    print(series,len(file_list))
    scanO = fn.makedf(file_list,path) #dataframe with odd data 
    scanO['bin'] = range(len(scanO))

    if not raw:
        scanO = scanO[['sum']].copy()    
        scanE = scanE[['sum']].copy()

    #print(scanO.head(),scanO.shape)
    
    ax = scanO.plot(legend = False)
    fn.pretty(series,high)    
    #plt.show(block = False);
    ax2 = scanE.plot(legend = False)
    fn.pretty(series,low)
    #plt.show(block = False);

    scanO.to_csv(series+"_summed.dat", sep = "\t"); print("Saved results")
    return;

"""
lorentzian() with domain and parameters returns a range 
"""
def lorentzian(x,p):
    #p = [5000,40000,30,75,125]  # [offset, Peak height, FWHM,center1, center2] #
    numerator =  (p[2]/2 )
    denominator1 = math.pi*(( x - (p[3]) )**2 + (p[2]/2)**2)
    denominator2 = math.pi*(( x - (p[4]) )**2 + (p[2]/2)**2)
    y = p[0]+p[1]*(numerator/denominator1)+p[1]*(numerator/denominator2)
    return y

"""
residuals() will be suqared, summed, then minimized
"""
def residuals(p,Y,X):
    L = fn.lorentzian(X,p)
    err = [(y-l)/l**.5 for l,y in zip(L,Y)]    
    return err


"""
plotfitseries() uses 
"""
def plotfitseries(series,low,high,path='./',raw=True,plot=True):
    file_list = fn.makelist(series,'odd',path) #High
    resultsodd = fn.chi2fit(series,file_list,high,path,raw,plot)
    file_list = fn.makelist(series,'even',path) #Low    
    resultseven = fn.chi2fit(series,file_list,low,path,raw,plot)
    return [resultsodd, resultseven];



"""
plotminseries() uses minuit fitting functions and reports errors in fitted params
"""
def plotminseries(series,low,high,path,raw,plot=True):
    file_list = fn.makelist(series,'odd',path) #High
    resultsodd = mfit(series,file_list,high,path,raw,plot)
    file_list = fn.makelist(series,'even',path) #Low
    resultseven = mfit(series,file_list,low,path,raw,plot)
    
    """
    print("Params", m.parameters)
    print("Args", m.args)
    print("Vals", m.values)
    print("Error", m.errors)
    """

    return [resultsodd, resultseven];



    
"""
Fit using iminuit, takes in information to fit one curve and returns values & errors
"""
def mfit(series,file_list,voltage,path="./",raw=True,plot=True):

    scan = fn.makedf(file_list,path)
    if not raw:
        scan = scan[['sum']].copy()
    y = scan['sum'].values
    x = range(len(y))

    

    def f(offset,peak,FWHM,C1,C2, elements):
        Sum=0;
        p = [offset,peak,FWHM,C1,C2]
        nu = len(x)-len(p); # nu (degrees of freedom) = N - r = number of points in our set - variables?
        for i in range(len(x)):
            l = fn.lorentzian(x[i],p)
            if y[i]==0:
                Sum+=(pow((y[i]-l),2))/(1)
            else:
                Sum+=(pow((y[i]-l),2))/(y[i])
            #print(Sum/nu)
        return Sum/nu #Normalized chi^2

    #p = [4,500,10,50,150]  # [offset, Peak height, FWHM,center1, center2] #
    p = [4,900,10,50,150]  # [offset, Peak height, FWHM,center1, center2] #
    #p = [4,1000,10,30,170]  # [offset, Peak height, FWHM,center1, center2] #

    m=Minuit(f, offset = p[0],  limit_offset = (0.,20.),    error_offset = 2.,
                peak = p[1],    limit_peak = (100.,1E5),    error_peak = 1E3,
                FWHM = p[2],    limit_FWHM = (5.,20.),      error_FWHM = 1.,
                C1 = p[3],      limit_C1 = (10.,90.),       error_C1 = 5.,
                C2 = p[4],      limit_C2 = (110.,190.),     error_C2 = 5.,
                elements = len(y),     fix_elements=True)
    m.migrad()
    #m.minos()

    pbest = [[]]*len(p);
    pbest[0]=m.values['offset']
    pbest[1]=m.values['peak']
    pbest[2]=m.values['FWHM']
    pbest[3]=m.values['C1']
    pbest[4]=m.values['C2']

    #print("Errors!")
    #print(m.get_merrors('C1'))
    #print("Params", m.parameters)
    #print("Args", m.args)
    print("Vals", m.values)
    print("Error C1", m.errors["C1"])
    print("Error C2", m.errors["C2"])

    y_fit = [fn.lorentzian(i,pbest) for i in range(len(x))]
    y_original = [fn.lorentzian(i,p) for i in range(len(x))]
    if raw:
        scan.plot(legend = True)
    else:
        plt.plot(x,y,'r^')
        plt.plot(x,y_fit)
    chi2 = f(pbest[0],pbest[1],pbest[2],pbest[3],pbest[4],len(y))
    print("Chi Squared = " + str(chi2))
    plt.grid()
    fn.pretty(series, voltage, binsize=False, Chi = chi2)

    c1str = str(int(round(pbest[3])))+" $\pm$ " + "{0:.1f}".format(m.errors["C1"])
    c2str = str(int(round(pbest[4])))+" $\pm$ " + "{0:.1f}".format(m.errors["C2"])
    plt.text(pbest[3]+max(x)*.02, max(y)*.95, c1str)
    plt.text(pbest[4]+max(x)*.02, max(y)*.95, c2str)
    if plot:
        plt.show(block = True)
    print(m.values['C1'])
    return m;


"""
chi2fit() takes in enough information to fit one curve and returns best fir parameters and chi^2
"""
def chi2fit(series,file_list,voltage,path='./',raw=True,plot=True):
    scan = fn.makedf(file_list,path)

    x = range(len(scan['sum'].values))
    y = scan['sum'].values
    #p = [4,500,10,50,150]  # This is tailored for smaller peaks, and works well enough for large ones
    

    p = np.asarray(p)
    pbest = leastsq(fn.residuals,p,args=(y,x),full_output=1)
    fit = lorentzian(x,pbest[0])
#    fit = lorentzian(x,p)
    scan['fit'] = pd.DataFrame(fit)
    chi2 = sum(r**2 for r in residuals(pbest[0],y,x))
    print(series+"\t"+voltage+",\tFWHM = " + str(pbest[0][2]))
    
    if plot:
        if not raw:
            scan = scan[['sum','fit']].copy()    

        #plt.text(max(y), max(x)*.25, str(p[3]))
        #plt.text(max(y), max(x)*.75, str(p[4]))
        if raw:
            ax = scan.plot(legend = False)
        else:
            ax = scan.plot(legend = True)
            ax.legend( ('Summed Scans', 'Best Fit Curve'), loc='upper center')
            
        fn.pretty(series,voltage,False,int(chi2))    
    #    plt.text(max(x)*.45, max(y)*.92, "$\chi^2$ = " + str(int(chi2)))
        plt.text(pbest[0][3]+max(x)*.02, max(y)*.95, str(int(round(pbest[0][3]))))
        plt.text(pbest[0][4]+max(x)*.02, max(y)*.95, str(int(round(pbest[0][4]))))
        if plot:
            plt.show(block = not plot);

    return [pbest[0][3], len(x)-pbest[0][4]-1, chi2];

"""
pretty()

A universal way for me to control all labels of figures
"""
def pretty(series, voltage, binsize=False, Chi=False):
    titlestr = series.title() + " at " + voltage
    if binsize:
        titlestr = titlestr + ", " + str(binsize) + "pt bin size"
    if Chi:
        titlestr = titlestr + ", $\chi^2$ = " + "{0:.2}".format(Chi)
    plt.title(titlestr)
    plt.xlabel("Bins having 0.35 MHz F-EOM width")
    plt.ylabel("PMT counts")
    plt.grid(True)
    return;
