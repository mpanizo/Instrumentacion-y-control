# -*- coding: utf-8 -*-
"""
Created on Tue May 14 16:30:34 2019

@author: Publico
"""

import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
import time


fsamp = 44100 #Hz frecuencia de sampleo máxima de la placa de sonido

#frequency = np.linspace(1000, 16000, 200) #Hz


def signal(frequency, tau =2, fs = fsamp):   

    myarray = 0.3*np.sin(np.linspace(0,tau,int(tau*fs))*frequency*(2*np.pi)) 

    tiempo = np.linspace(0, tau, int(tau*fs))
    
    return tiempo, myarray  


def GeneradorArray(tau, frequency, Amplitude = 1, fs = 44100): #por default tiene 44100 y no hay que aclararsela
    if type(frequency) == int: #si el input de frecuencia es un dado valor, hace lo de siempre
        myarray = Amplitude*np.sin(np.linspace(0,tau,int(tau*fs))*frequency*(2*np.pi))
        Tiempo = np.linspace(0, tau, len(myarray))
        return myarray, frequency, Tiempo
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

    Tiempos = np.linspace(0, tau, len(myarray))
    
    return myarray, Frecuencias, Tiempos

def play_record(frequency, tau = 90, fs = fsamp):  #s, Hz, Hz
    myarray, Frec, tiempo = GeneradorArray(tau, [0, 1000, 0, 2000, 0, 3000, 0, 4000,0, 5000, 0, 6000, 0, 7000, 0, 8000, 0, 9000, 0, 10000, 0, 11000, 0, 12000, 0, 13000, 0, 14000, 0, 15000, 0, 16000, 0, 17000, 0, 18000, 0, 19000, 0, 20000, 0, 21000, 0, 22000, 0, 23000, 0, 24000, 0, 25000, 0])
    t1 = time.time()
    myrecording = sd.playrec(myarray, samplerate=fs, channels=2)
    sd.wait()
    t2 = time.time()
    myrecording = np.transpose(myrecording)
    return tiempo, myrecording, t2-t1, myarray



tiempo, myrecording, t, pulsoenviado = play_record(1000)
tiempo = np.linspace(0, 90, len(myrecording[0]))
np.savetxt("BARRIDO_tiempo_myrecording_pulsoenviado_t" +str(t) + ".txt", np.transpose([tiempo, myrecording[0], pulsoenviado]))
print('duro ', t, 'segundos')
time_real = np.linspace(0, t, len(myrecording[0]))
plt.plot(tiempo, myrecording[0], tiempo, 0.5*pulsoenviado)
plt.plot(tiempo, 0.5*pulsoenviado)
plt.show()




frequency = np.linspace(1000, 30000, 100)
def barrido_play_record():
    
    vpp = []   
    
    reco = [] 
    
    tiempos = []
    
    for f in frequency:
        
        timetotal, myrecording = play_record(f)
        
        reco.append(myrecording) #guardamos los valores que lee

        vpp.append(2*max(myrecording)) #guardamos lo que sería aprox. el voltaje pico a pico

        tiempos.append(timetotal)
        
    total  = {'reco': reco, 'tiempos': tiempos, 'vpp': vpp}

    return total