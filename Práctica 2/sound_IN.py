# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 16:37:36 2019
@author: Publico
"""

import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
import time

from generador import GeneradorFunciones



%## """Entrada de Placa de audio, genera la señal un Generador de Funciones"""



gen = GeneradorFunciones()


def record(tau, fs):  #input: tiempo total que lee la placa de audio (s), con una frecuencia de sampleo fs
    
    myrecording = sd.rec(int(tau*fs), samplerate=fs, channels=1, blocking=True)  #lee cantidad de puntos int(tau*fs), no sigue hasta que termina de leer (blocking= True)
  
    time_total = np.linspace(0, tau, int(tau*fs)) 

    return myrecording, time_total  #sirve para plotear la señal


tau = 2 #s

fsamp = 44100 #Hz

frequency = np.linspace(400, 1000, 100)


#generador de funciones manda una sinusoideal de frecuencia tal, el microfono lee un captura pantalla

def barrido_frecuency_generador(): 

    vpp = []   

    reco = [] 
     
    tiempos = []

    for f in frequency: 

        gen.SetFrequency(f)   #el generador de frecuencia manda una señal de frecuencia f

        my_recording, timetotal = record(tau, fsamp) #el microfono lee la señal, devuelve un "captura pantalla" (voltaje vs tiempo)

        reco.append(my_recording) #guardamos los valores que lee

        vpp.append(2*max(my_recording)) #guardamos lo que sería aprox. el voltaje pico a pico

        tiempos.append(timetotal) #guardamos el array de tiempo

    total = {'reco': reco, 'tiempos': tiempos, 'vpp': vpp}

return total
