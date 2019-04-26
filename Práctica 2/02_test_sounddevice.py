# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 16:37:36 2019
@author: Publico
"""

import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
import time


fsamp = 44100

def GeneradorArray(tau, frequency, Amplitude = 1, fs = 44100): #por default tiene 44100 y no hay que aclararsela
    if type(frequency) == int: #si el input de frecuencia es un dado valor, hace lo de siempre
        myarray = Amplitude*np.sin(np.linspace(0,tau,int(tau*fs))*frequency*(2*np.pi))
        return myarray
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
    

#sd.play(funcion(3, fsamp, 440),fsamp)

#sd.stop()

#time.sleep(3)
#array = funcion(3, fsamp, 450)
#plt.plot(array)

def barrido():
    frecuencia = np.linspace(200, 600, 10)
    for f in frecuencia:
        myarray = GeneradorArray(1, fsamp, f)
        sd.play(myarray, fsamp)
        time.sleep(1)
        #print(f)
        
#barrido()
def pasaralista(a):
    b = list(a)
    c = []
    i = 0
    while i < len(b):
        c.append(float(b[i]))
        i = i + 1
    return c


def record(tau, fs):
    myrecording = sd.rec(int(tau*fs), samplerate=fs, channels=1, blocking=True)
    time_total = np.linspace(0, tau, int(tau*fs))
    return myrecording, time_total

myrecording, time_total = record(3, fsamp)

#print('my recording ', myrecording)
#print('time total', time_total)

#time.sleep(3)
#sd.wait()

plt.plot(pasaralista(myrecording))
#plt.plot(list(time_total), pasaralista(myrecording))

#plt.plot(myrecording)
#print(len(list(time_total)))
#print(len(list(pasaralista(myrecording))))
plt.show()



#%%
import matplotlib.pyplot as plt
array1, Frec, Tiempo = GeneradorArray(1, [5, 10, 15, 20, 25, 30, 35, 40, 45, 50])

plt.plot(Tiempo, array1)
