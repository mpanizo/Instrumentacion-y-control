# -*- coding: utf-8 -*-
"""
Editor de Spyder
"""

## Sensor DAQ

import nidaqmx as ndq
import matplotlib.pyplot as plt
import Generador
import time
import numpy as np
Gen = Generador.GeneradorFunciones()

Pantallas = []
Vpp = []
Frec = np.arange(1, 100, 1)
for i in Frec:
    Gen.SetFrequency(str(i) + ' kHz')
    with ndq.Task() as task:
        task.ai_channels.add_ai_voltage_chan("Dev4/ai0")
        task.timing.cfg_samp_clk_timing(1000)
        reading = task.read(number_of_samples_per_channel=10000)
        time.sleep(0.5)
        Vpp.append(abs(max(reading)-min(reading)))
        Pantallas.append(reading)

#plt.plot(np.fft.fft(reading))
plt.plot(Frec, Vpp, 'o')
plt.plot(reading,'o')
plt.plot(Pantallas[10])



with ndq.Task() as task:
    task.ao_channels.add_ao_voltage_chan("Dev4/ao0")
task.write(1.1, auto_start=True)
