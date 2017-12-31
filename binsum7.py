""""
Author: A.C. DeHart & Mukut
Date: 25/05/2016
File: binsum2.py
Version: Python 3.5.1
"""
print(":::Running Binsum7:::\n")
import os, time, sys, re
from glob import glob as glob2
import glob
import numpy as np
import matplotlib.pyplot as plt
from operator import add
from scipy.optimize import leastsq # Levenberg-Marquadt Algorithm #
import warnings
print("Imported Libraries...")

"""
Call 6774, elog for files

This script should (live):
    -identify newest directory and navigate there
    -identify the last primary scan with data via the info tag (eg. scan1_info.txt, data_000000.txt)
    -sum all sub-scans within a frequency range (eg. scan1_000 to scan1_009)
    -plot live results of sum
    -save plot before repeating

BUGS:
    -Uncomment line 51 (directs to Data Z Drive) & line 267 (plt.cla())
    -enable while 1 & continue statement
    -Throws self depricating warning on first plot, can be ignored
    -Requires python.exe (version 3.5.1| Anaconda 4.0.0) to be on the Desktop (?)
    -Constantly alerts user to what scan is being examined
"""


bin = int(input("Bin size?: "))
#raw_bin = int(input("How many bins in raw data?: "))

def main():
    print("Running Main...")
    def fxn():
        warnings.warn("deprecated", DeprecationWarning)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        fxn()


    
    """INITIALIZATION OF VARIABLES AND FUNCTIONS"""
    """
    print("Notes to user:")
    print("Use the naming convention of 'scanX' and save all scans into the same directory.")
    print("This software should only be launched after the directory has been created.") 
    print("It will not look for new directories while running.")    
    """    

    def cls():
        os.system('cls' if os.name=='nt' else 'clear')
    #Need screen size ( scrsz = get(groot,'ScreenSize') )
    works = False
    wait = 0
    cls = cls()
    stitle = ''
    latest_subdir = ''
    previous = ''


    
    """FIND NEWEST FOLDER"""
    os.chdir("Z:\\Data")
    all_subdirs = [d for d in os.listdir('.') if os.path.isdir(d)]
    latest_subdir = max(all_subdirs, key=os.path.getmtime)
    os.chdir(latest_subdir)
    workpath = os.getcwd()
    #workpath = "/home/dehart/Desktop/Work/live fit"
    print("Work Path: '{}'".format(workpath))



    """INFINITE LOOP"""
    print("Initiating Loop...")
    while True:  


        """FIND NEWEST FOLDER"""
        os.chdir("Z:\\Data")
        all_subdirs = [d for d in os.listdir('.') if os.path.isdir(d)]
        latest_subdir = max(all_subdirs, key=os.path.getmtime)
        os.chdir(latest_subdir)
        workpath = os.getcwd()
        #workpath = "/home/dehart/Desktop/Work/live fit"
        print("Work Path: '{}'".format(workpath))

        

        """NAVIGATE TO ROOT DATA DIRECTORY"""
        os.chdir(workpath)
        print('Navigating to work path')



        """FIND NEWEST INFO FILE"""
        #print("Finding newest file:")
        files = []        
        #For 3.5
        #print(os.path.join(workpath+'/**/*info.txt'))
        #print(glob.iglob(os.path.join(workpath+'/**/*info.txt'), recursive=True))
        for filename in glob.iglob(os.path.join(workpath+'/**/*info.txt'), recursive=True):
            #print(filename)
            files.append(filename)
        #For 3.4
        #files = [y for x in os.walk(os.getcwd()) for y in glob2(os.path.join(x[0], '*info.txt'))]
        #print("E1")        
        
        
        """CONTINUE IF NO DATA PRESENT"""
        if files == []:
            if not wait:
                cls
                print("Waiting for data.", end="")            
            else:
                print(".", end="")
                if wait>1:
                    wait = -1
                    print("")
            sys.stdout.flush()
            wait = wait + 1
            time.sleep(1)
            continue


        """NAVIGATE TO NEWEST INFO FILE"""
        path_name = max(files, key = os.path.getctime)
        #print("E2")        
        print("Newest info file: {}".format(path_name))        
        [new_dir,new_file] = os.path.split(path_name)
        #print("E3")        
        stitle = new_file.split('_')[0]
        #print("Working on files labeled '{}'".format(stitle))
        if previous != path_name:
            print("Found '{}'".format(path_name))
            previous = path_name
        os.chdir(new_dir)
        #print("Operating in '{}'".format(new_dir))



        """IDENTIFY LAST INFO FILE
        mat = []
        headers = []
        names = glob.glob('./*info.txt')
        names = [n[2:] for n in names]

        #print(names)

        for name in names:
            if len(re.split('(\d+)',names[0])) is 2:
                name = np.insert(name,1,'0')
            mat.append(int(re.split('(\d+)', name)[1]))
            headers.append(re.split('(\d+)', name)[0])
        
        
        
        #print(mat)
        #print(headers)                
        H = headers[mat.index(max(mat))]
        N = max(mat)
        #print(H,N)
        


        IDENTIFY LAST SCAN
        mat = []
        names = glob.glob('./*.txt')
        names = [n[2:] for n in names]
        for name in names:
            if name[0:4]=='scan' and '_0' in name:
                num = int(name.split('scan')[1].split('_')[0])
                mat.append(num)
        """


        """CHECK IF ANY DATA PRESENT"""
        names = glob.glob(stitle+'*')
        """
        if names == []:
            if not wait:
                cls
                print("Waiting for data.", end="")
                works = False            
            else:
                print(".", end="")
                if wait>1:
                    wait = -1
                    print("")
            sys.stdout.flush()
            wait = wait + 1
            time.sleep(1)
    #        continue
        else:
            cls
            if not works:
                print("Data found.")
                works = True
        """        


        """Trouble Shoot stitle values
        print(stitle)
        print(H+str(N)+'_0')
        print(stitle != H+str(N)+'_0')
        """            

        
        
        """GET LIST OF DATA FILES"""
        names = glob.glob('./'+ stitle+'_0'+'*.txt')
        names = [n[2:] for n in names]



        """GET NUMBER OF RAW BINS"""
        with open(names[0]) as inputfile:
            lines = inputfile.read().split('\n')
            lines = lines[5:-1]
            lines = list(map(int, lines))
            raw_bin = len(lines)
        print("raw_bin: ", raw_bin)
        M = np.zeros(raw_bin)
        


        """SUM DATA FROM ALL FILES"""
        for name in names:
            lines = []
            with open(name) as inputfile:
                lines = inputfile.read().split('\n')
                lines = lines[5:-1]
                lines = list(map(int, lines))
            M = list(map(add,M,lines))
        #print(M[0:10]);print(M[-10:])



        """SAVE SCAN BEFORE MOVING ON"""
        #plt.clf()
        if not os.path.isdir('./results'):
            os.makedirs('./results')
        #M=M/np.linalg.norm(M) #Normalized Data



        """MUKUT'S BIN & PLOT SCRIPT (PMT_2photon.py modified)"""
        data_binned=[]
        a=[]

        #bin = 50
        range_max = int(raw_bin/bin)

        for i in range(0,range_max):
           a=sum((M[i*bin:(i+1)*bin]))
           data_binned=np.append(data_binned,a)

        #plot the data
        import matplotlib.pyplot as plt
        x=np.arange(0,len(data_binned))
        """    
        fig1=plt.figure()
        plt.plot(x,data_binned,'r.')
        plt.title(stitle[0:-2] + ' (' + str(mat.count(max(mat))) + ' files)')
        plt.xlabel("Frequency range is 80 Mhz, 40 up and 40 down")
        plt.ylabel("Normalized PMT counts")
        plt.grid()
        plt.show()
        """

        A=np.column_stack((x.flatten(),data_binned.flatten()))
        np.savetxt(stitle + '_plot.txt',A)
        # This part saves data from the plot to text files.
        """ Unnecessary plots?
        #first part of the plot
        fig2=plt.figure()
        plt.plot(x[0:118],data_binned[0:118],'g.')
        plt.grid()
        plt.show()
        A=np.column_stack((x[0:118].flatten(),data_binned[0:118].flatten()))
        np.savetxt(stitle[0:-2] + '_test1.txt',A)
        #second part of the plot
        fig3=plt.figure()
        plt.plot(x[119:237],data_binned[119:237],'k.')
        plt.grid()
        plt.show()
        A=np.column_stack((x[119:237].flatten(),data_binned[119:237].flatten()))
        np.savetxt(stitle[0:-2]+'_test2.txt',A)
        """


        """MUKUT'S FUNCTION FITTING SCRIPT (Fit_Lorentzian_data_offset.py modified)"""
        A= np.loadtxt(stitle + "_plot.txt")
        x=A[0:,0]
        y=A[0:,1]


        def lorentzian(x,p):
            numerator =  (p[2]/2 )
            denominator1 = 3.142*(( x - (p[3]) )**2 + (p[2]/2)**2)
            denominator2 = 3.142*(( x - (p[4]) )**2 + (p[2]/2)**2)
            y = p[0]+p[1]*(numerator/denominator1)+p[1]*(numerator/denominator2)
            return y


        def residuals(p,y,x):
            err = y - lorentzian(x,p)
            return err
        # defining the 'background' part of the spectrum #
        ind_bg_low = (x > min(x)) & (x < 20.0)
        ind_bg_high = (x > 80.0) & (x < max(x))

        x_bg = np.concatenate((x[ind_bg_low],x[ind_bg_high]))
        y_bg = np.concatenate((y[ind_bg_low],y[ind_bg_high]))
        #pylab.plot(x_bg,y_bg)
        # fitting the background to a line # 
        m, c = np.polyfit(x_bg, y_bg, 1)

        # removing fitted background # not using it now 
        background = m*x + c
        y_bg_corr = y
        #pylab.plot(x,y_bg_corr)
        # FITTING DATA 

        """
        I DISAGREE WITH THIS HARDCODED IMPLIMENTATION
        # initial values #
        p = [5000,40000,5,55,167]  # [offset, Peak height, FWHM,center1, center2] #

        # optimization # 
            
        pbest = leastsq(residuals,p,args=(y_bg_corr,x),full_output=1)
        best_parameters = pbest[0]
        print(best_parameters)
        print("First peak: ", best_parameters[3])
        print("Second peak: ", best_parameters[4])
        midP=best_parameters[3]+(best_parameters[4]-best_parameters[3])/2
        print("Mid point: ", midP)
        print("FWHM: ", best_parameters[2])
        # fit to data #
        x1=np.arange(0,239,0.1)
        fit = lorentzian(x1,best_parameters)
        """

#        plt.clf()
        plt.cla()
#        plt.close("all")
        """PLOTTING"""
        #print("Plotting {}".format(stitle))

        sys.stdout.flush()
        #print(stitle[0:-2])
        plt.plot(x[1:],y_bg_corr[1:],'g.')
        #plt.plot(x1,fit,'k-',lw=1) # I disagree with this plotting method
        #plt.plot((midP,midP),(min(y_bg_corr),max(y_bg_corr)),'b--')
        if len(names)== 1:
            plt.title(os.path.join(os.getcwd(),stitle) + ' (' + str(len(names)) + ' file)')
        else:
            plt.title(os.path.join(os.getcwd(),stitle) + ' (' + str(len(names)) + ' files)')
        plt.xlabel("Integrated bin# (bin size: {})".format(bin))
        plt.ylabel("PMT counts")
        plt.grid()
#        plt.show()#block=False)
        plt.savefig('./results/' + stitle + '.png', bbox_inches='tight')
        #plt.waitforbuttonpress(False)
        plt.draw()
        time.sleep(0.001)
        plt.pause(0.0001)





if __name__ == '__main__':
    main()
