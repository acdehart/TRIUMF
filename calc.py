""" calc.py """
"""
Author: A.C. DeHart
Inspired by Avinash
Environnment: Python 3
Comment: This python3 script runs a GUI to help users at the lab calculate the number of atoms we are trapping in our MOT. Our trapped atoms are scattering light in every direction. We have cameras with known exposure times and steradians relative to the trap. The user enters in values such as the wavelength of the trapping light, the power of the trapping beams, the beam diameters, lifetime of the excited state of our atom, the red detuning of the trapping light, region of interest counts and background counts. Depending on the certainty of the input values, we can approximate the number of atoms in our trap based on calculations made by M. Kalita.
"""
 
import tkinter as tk
from functools import partial
 
"""Make calculation with input"""
def call_result(label_result, lam, p1, p2, p3, diam, t, det, ROI, BKG):
    """Get variables"""
    lambd = float(lam.get())    # 750
    P1 = float(p1.get())        # 17
    P2 = float(p2.get())        # 63
    P3 = float(p3.get())        # 102
    Diam = float(diam.get())    # 1
    Tau = float(t.get())        # 26.24
    Detun = float(det.get())    # 30
    ROICount = float(ROI.get()) # 4.6E5
    BKGCount = float(BKG.get()) # 5E2

    """Constants and calculations"""
    h=6.63*10**(-34)
    c=299792458
    lambd=lambd*10**(-9)
    Tau=Tau*10**-9
    Gamma=1/Tau
    d=Diam*2.54
    Area=3.141*(d/2)**2
    Intensity=2*(P1+P2+P3)/Area
    Detun=Detun*10**6
    SatInten=2.75*1000*3.141*h*c/(3*(lambd**3)*Tau*100**2)
    Snumber=Intensity/SatInten
    Scattering_rate=(Gamma/2)*Snumber/(1+Snumber+(2*2*3.141*Detun/Gamma)**2)
    Photon_perADC=12.5
    LnsDiam = 2*2.54;
    LnsArea = 3.141*(LnsDiam/2)**2;
    FLength = 10;
    SAngle = LnsArea/(FLength**2);
    FracCamera = 0.3;
    FracOfTotalSangle=SAngle/(4*3.141)

    ADCCount=ROICount-BKGCount
    ExposureTime = 0.10;
    NumberOfAtoms = (ADCCount*Photon_perADC)/(FracOfTotalSangle*ExposureTime*Scattering_rate*FracCamera)

    #result = float(P1)+float(P2)+float(P3)
    label_result.config(text="Percent Photons Collected %0.1f%%\nNumber of Atoms is %d" % (FracOfTotalSangle*100,NumberOfAtoms))
    return

"""Setup Window"""
root = tk.Tk()
root.bind("<Return>", lambda event: call_result())
root.geometry('355x250+100+200')
root.resizable(0,0)
root.title('Atom Number')

"""Initiate variables"""
lambd = tk.StringVar()
P1 = tk.StringVar()
P2 = tk.StringVar()
P3 = tk.StringVar()
Diam = tk.StringVar()
Tau = tk.StringVar()
Detun = tk.StringVar()
ROICount = tk.StringVar()
BKGCount = tk.StringVar()

"""Create labels for variables"""
#labelTitle = tk.Label(root, text="Atom Number").grid(row=0, column=2)
labelNum0 = tk.Label(root, text=" Wavelength ").grid(row=0, column=0);labelNum1 = tk.Label(root, text="(nm)").grid(row=0, column=4)
labelNum1 = tk.Label(root, text=" Power in Beam 1 ").grid(row=1, column=0);labelNum1 = tk.Label(root, text="(mW)").grid(row=1, column=4)
labelNum2 = tk.Label(root, text=" Power in Beam 2 ").grid(row=2, column=0);labelNum1 = tk.Label(root, text="(mW)").grid(row=2, column=4)
labelNum3 = tk.Label(root, text=" Power in Beam 3 ").grid(row=3, column=0);labelNum1 = tk.Label(root, text="(mW)").grid(row=3, column=4)
labelNum4 = tk.Label(root, text=" Beam Diameter ").grid(row=4, column=0);labelNum1 = tk.Label(root, text="(in.)").grid(row=4, column=4)
labelNum5 = tk.Label(root, text=" Lifetime of State ").grid(row=5, column=0);labelNum1 = tk.Label(root, text="(ns)").grid(row=5, column=4)
labelNum6 = tk.Label(root, text=" Detuning ").grid(row=6, column=0);labelNum1 = tk.Label(root, text="(MHz)").grid(row=6, column=4)
labelNum7 = tk.Label(root, text=" Enter ROI Count ").grid(row=7, column=0)
labelNum8 = tk.Label(root, text=" Enter BKG Count ").grid(row=8, column=0)

labelResult = tk.Label(root)
labelResult.grid(row=10, column=2)
 
"""Make space for user input"""
entryNum0 = tk.Entry(root, textvariable=lambd, width=24).grid(row=0, column=2)
entryNum1 = tk.Entry(root, textvariable=P1, width=24).grid(row=1, column=2)
entryNum2 = tk.Entry(root, textvariable=P2, width=24).grid(row=2, column=2)
entryNum3 = tk.Entry(root, textvariable=P3, width=24).grid(row=3, column=2)
entryNum4 = tk.Entry(root, textvariable=Diam, width=24).grid(row=4, column=2)
entryNum5 = tk.Entry(root, textvariable=Tau, width=24).grid(row=5, column=2)
entryNum6 = tk.Entry(root, textvariable=Detun, width=24).grid(row=6, column=2)
entryNum7 = tk.Entry(root, textvariable=ROICount, width=24).grid(row=7, column=2)
entryNum8 = tk.Entry(root, textvariable=BKGCount, width=24).grid(row=8, column=2)

"""Get resuslts and loop"""
call_result = partial(call_result, labelResult, lambd, P1, P2, P3, Diam, Tau, Detun, ROICount, BKGCount)
buttonCal = tk.Button(root, text="Calculate", command=call_result).grid(row=9, column=0)
#buttonCal.pack()
root.mainloop()
