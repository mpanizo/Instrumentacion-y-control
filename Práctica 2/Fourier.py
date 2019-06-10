# -*- coding: utf-8 -*-
"""
Created on Tue May 28 14:16:55 2019

@author: nicon
"""
import numpy as np
import random
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from scipy import fftpack
from scipy.signal import find_peaks    

def NoisySin(f):
    x = np.linspace(0, 4*np.pi/f, 1000)
    y = [np.sin(2*np.pi*f*i) + random.random()*0.1 for i in x] 
    return x, y

def CommonSin(x, A, w, phi):
    return A*np.sin(w*x + phi)

def GetFrequency(V, t, Aguess = 1, wguess = 0.5, phiguess = 0):
    params, params_cov = curve_fit(CommonSin, t, V, p0=[Aguess, wguess, phiguess])
    print(params)
    return params[1]

def Frecuencias_FFT(x, y, debug = False):
    yfft = fftpack.fft(y)
    N = len(x)
    T = x[-1]/N
    xf = np.linspace(0, 1/(2*T), N/2)
    yf = 2.0/N * np.abs(yfft[:N//2])
    PosicionPicos, IntensidadPicos = find_peaks(yf, height=yf[0])
    VectorFrecuenciaPicos = [xf[i] for i in PosicionPicos]
    if len(list(IntensidadPicos['peak_heights'])) > 0:
        PosicionImax = np.argmax(list(IntensidadPicos['peak_heights']))
        FrecuenciaDelMaximo = VectorFrecuenciaPicos[PosicionImax]
    else:
        FrecuenciaDelMaximo = 0
        
    if debug:
        print('El vector de las frecuencias de los picos es', VectorFrecuenciaPicos)
        print('Las intensidades de los picos son ', IntensidadPicos)
        print('La frecuencia del maximo es ', FrecuenciaDelMaximo)
#    print('La frecuencia es', VectorFrecuenciaPicos)
#    return VectorFrecuenciaPicos
    return xf, yf, FrecuenciaDelMaximo



if __name__ == '__main__':

    x, y = NoisySin(100)
#    params, params_cov = curve_fit(CommonSin, x, y, p0=[1, 0.5, 0])
#    plt.plot(x, CommonSin(x, *params))
#    plt.plot(x, y)  

#    xf, yf, N, pp = Frecuencias_FFT(x, y)
#    plt.plot(xf, yf)
    f = Frecuencias_FFT(x, y)    
    print(f)
#    print(Fpicos)
    #plt.plot(x, y)
