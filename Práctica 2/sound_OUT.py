# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 16:37:36 2019
@author: Publico
"""

import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
import time

from osciloscopio import Osciloscopio


%## """Salida de Placa de audio, lee la señal un Osciloscopio"""


osc = Osciloscopio()


def signal(tau, fs, frequency):   #input: tiempo total de la señal (s), frecuencia de sampleo (Hz), frecuencia de la señal (Hz) 

    myarray = np.sin(np.linspace(0,tau,int(tau*fs))*frequency*(2*np.pi)) #crea una señal sinosuideal con int(tau*fs)) cantidad de puntos

    return myarray  


tau = 1 #s

fsamp = 44100 #Hz frecuencia de sampleo máxima de la placa de sonido

frequency = np.linspace(1000, 16000, 200) #Hz



#la placa manda una sinusoideal de frecuencia tal, el osciloscopio setea el time base y lee la frecuencia y el voltaje pico a pico

def barrido_frecuency(name_file): #input: 'name_lecture_osc.txt', nombre de la medida

    

    vpp = []   # voltaje pico a pico, lectura de osciloscopio
    fre = []   # frecuencia, lectura de osciloscopio

    for f in frequency:

        osc.set_timebase((2/f)/10) # setea el time base del osciloscopio, para que pueda leer 2 periodos de la señal
        time.sleep(0.1) #tiempo muerto hasta que se setea

        myarray = signal(tau, fsamp, f) #utiliza la funcion "signal" para generar una señal de frecuencia f que dure un tau
        sd.play(myarray, fsamp) # la placa genera la señal, con una frecuencia de sampleo fsamp

        vpp.append(osc.peaktopeak()) #el osciloscopio guarda el voltaje pico a pico
        fre.append(osc.get_frequency()) #el osciloscopio guarda la frecuencia

        time.sleep(tau) #se espera el tiempo muerto que dura la señal y se itera a la siguiente frecuencia
        
    vpp_osc = np.array(vpp) 
    frequency_osc = np.array(fre)  

    #en orden guarda: frecuencia input, frecuencia medida por osclioscopio, voltaje pico a pico medido por osciloscopio
    np.savetxt(name_file, np.transpose([frequency, frequency_osc, vpp_osc]))
    
return frecuency, frequency_osc, vpp_osc
