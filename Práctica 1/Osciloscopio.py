# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 18:39:33 2019

@author: nicon
"""

import pyvisa
import numpy as np
import matplotlib.pyplot as plt

class Osciloscopio(object):

    def __init__(self, instrument = 0): #Ver cual es 1 y 0 con el generador
        self.rm = pyvisa.ResourceManager()
        if len(self.rm.list_resources()) > 0:
            self.inst = self.rm.open_resource(self.rm.list_resources()[instrument])
        else:
            self.inst = []
            print('No se detectó ningún instrumento')
        if self.inst != []:
            try:
                print('El IDN del instrumento es ', self.inst.query("*IDN?"))
            except:
                print('El instrumento no respondió cuando se le preguntó el nombre.')
        
    def data_encdg_ascii(self):
        self.inst.write('DATA:ENCDG ASCII')
        
    def data_encdg_bin(self):
        self.inst.write('DATA:ENCDG RIBinary')

    def get_data_ascii(self):
        self.data_encdg_ascii()
        read = self.inst.query_ascii_values('CURVe?')
        
        plt.plot(read)
        plt.show()
        
        return read
        
        plt.plot(read)
        plt.show()
        
        return read

    def read_voltage(self):
        
        self.data_encdg_bin()
        read = np.array(self.inst.query_binary_values('CURVe?', datatype = 'b', is_big_endian= True))
        
        ymult = self.inst.query_ascii_values('WFMPRE:YMULT?') #Vertical scale factor
        yzero = self.inst.query_ascii_values('WFMPRE:YZERO?') #Offset Voltage
        yoff = self.inst.query_ascii_values('WFMPRE:YOFF?')   #Vertical Offset

        voltage = yzero + ymult*(read - yoff)
        
       # plt.plot(voltage)
        #plt.show()
        
        return voltage
    
       
    def read_time(self):    
        xincr = self.inst.query_ascii_values('WFMPRE:XINCR?') #Horizontal sampling interval
        xzero = self.inst.query_ascii_values('WFMPRE:XZERO?')
        pt_off = self.inst.query_ascii_values('WFMPRE:PT_Off?')
        
        n = np.linspace(0,2500,2500)
        #Ver https://www.i3detroit.org/wi/images/2/2d/460-ProgrammerManual.pdf pag 2-43
        time = xzero + xincr*(n - pt_off)
        
        return time
    
    def grafico(self):
        voltage = self.read_voltage()
        time = self.read_time()
        
        vpp = 2*max(voltage)
        
        plt.plot(time, voltage)
        plt.xlabel('Time (s)')
        plt.ylabel('Voltage (V)')
        plt.show()
        
        return vpp

    
    def set_timebase(self, seconds):
        self.inst.write('HOR:DEL:SCA {}'.format(seconds))
