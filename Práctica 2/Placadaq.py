# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal.
"""

## Sensor DAQ

import nidaqmx as ndq
import matplotlib.pyplot as plt
import Generador
import time
import numpy as np
from AuxFunctions import GetFrequency, CommonSin
from Fourier import Frecuencias_FFT
from scipy import fftpack
from scipy.signal import find_peaks    
Gen = Generador.GeneradorFunciones()

    
Pantallas_0 = [] #vamos a medir dos canales, por eso armamos dos listas
Pantallas_1 = []
TiemposPantallas = []
Vpp = []

Frec = np.linspace(1, 100, 200) #kHz

#Barrido en frecuencia

for i in Frec:
	Gen.SetFrequency(str(i) + ' kHz')
	with ndq.Task() as task:
	    task.ai_channels.add_ai_voltage_chan("Dev11/ai0",  terminal_config=ndq.constants.TerminalConfiguration.RSE)
            task.ai_channels.add_ai_voltage_chan("Dev11/ai1",  terminal_config=ndq.constants.TerminalConfiguration.RSE)
	    #hay que configurar el modo RSE sino por default mide en diferencial
	    frec_sampleo = 20000 #kHz
	    N = 1000	    
	    task.timing.cfg_samp_clk_timing(frec_sampleo, sample_mode= ndq.constants.AcquisitionType.FINITE, samps_per_chan=N) 
	    #adquiero la data:
	    reading = task.read(number_of_samples_per_channel=N) #N = cantidad de puntos a adquirir
	    #espero a que termine de adquirir:
	    task.wait_until_done()
	    
            
            read_0 = reading[0]
            read_1 = reading[1]
            
            Pantallas_0.append(read_0)
            Pantallas_1.append(read_1)
            TiemposPantallas.append(np.linspace(0, N/frec_sampleo, N))
            
#Ploteo de las pantallas
          
def PloteoPantalla(x):
    print(Frec[x])
    plt.plot(TiemposPantallas[x], Pantallas[x], 'o')

#Transformada de Fourier para cada pantalla

def FourierPantalla(x, plot=False, debug = False):    

    xf, yf, Picos = Frecuencias_FFT(TiemposPantallas[x], Pantallas[x], debug = debug)
    if plot:
        plt.plot(xf, yf)
    if abs(1000*Frec[x] - Picos) > 1000:
        print('Fallo en mas de 500 hz para N = ', x, ', con frecuencia enviada de ', Frec[x])

#    if len(Picos) == 1:
    return Frec[x], Picos
#    print('Los picos son mas de uno. Para x = ', x, 'los picos son', Picos)
#    return Frec[x], 0

#Ploteo frecuencia de la placa vs frecuencia seteada en el osciloscopio
i = 0
Freal = []
Fpicos = []
while i < len(Pantallas):
    fr, fp = FourierTalPantalla(i)
    Freal.append(fr)
    Fpicos.append(fp)

    i = i + 1
plt.plot(Freal,Fpicos,'o')
        
