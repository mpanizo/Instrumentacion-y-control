# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 16:37:36 2019
@author: Publico
"""

import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
import time



%## """Otras opciones de generar señales:"""


def GeneradorArray(tau, frequency, Amplitude = 1, fs = 44100): #por default tiene 44100 y no hay que aclararsela
    if type(frequency) == int: #si el input de frecuencia es un dado valor, hace lo de siempre
        myarray = Amplitude*np.sin(np.linspace(0,tau,int(tau*fs))*frequency*(2*np.pi))
        Tiempo = np.linspace(0, tau, len(myarray))
        return myarray, frequency, Tiempo
    Tiempos = np.linspace(0, tau, fs)
    taufraccionado = tau/len(frequency) #fracciona en partes temporales iguales cada frecuencia
    
    i = 0
    myarray = np.linspace(0, 0, 0)
    Frecuencias = np.linspace(0, 0, 0)
    LastPoint = 0 #está para que el concatenado de todas las frecuencias sea correcto
    
    while i < len(frequency):
        PartialLinspace = np.linspace(0, taufraccionado, int(taufraccionado*fs))*frequency[i]*(2*np.pi) + LastPoint
        PartialArray = Amplitude*np.sin(PartialLinspace)
        PartialFrecuencias = np.linspace(frequency[i], frequency[i], len(PartialArray))
        myarray = np.concatenate((myarray, PartialArray))
        Frecuencias = np.concatenate((Frecuencias, PartialFrecuencias))
        i = i + 1
        LastPoint = PartialLinspace[-1]
    
    return myarray, Frecuencias, Tiempos
    

def GeneradorArraySweepContinuo(tau, freqini, freqf, Amplitude = 1, fs = 44100): #por default tiene 44100 y no hay que aclararsela
    frequency = np.linspace(freqini, freqf, fs*tau)
    Tiempos = np.linspace(0, tau, fs*tau)
    myarraylist = []
    i = 0
    while i < len(frequency):
        myarraylist.append(Amplitude*np.sin(Tiempos[i]*frequency[i]*2*np.pi))
        i = i + 1
    myarraylist = np.array(myarraylist)
    return myarraylist, frequency, Tiempos



def pasaralista(a):
    b = list(a)
    c = []
    i = 0
    while i < len(b):
        c.append(float(b[i]))
        i = i + 1
    return c


señal = [0]
mylist = [0]

def barridoamplitud():
    amplitud = np.linspace(1,3,3)
    for k in amplitud:
        mylist.append(k) 
    for j in amplitud:
         j = int(j)
         mylist [j-1] = GeneradorArray(0.1,20,j)
#        myrecording  = sd.playrec(myarray, fsamp, channels=2)
         time.sleep(1)  
         señal.extend(mylist[j-1])
    return señal

