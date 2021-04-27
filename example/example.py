# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 14:51:14 2021

@author: ebel
"""
if __name__ == "__main__":
    import serial.tools.list_ports as list_ports
    import PySchott
    from time import sleep
    a = list_ports.comports()
    if len(a)>0:
        print('available COM ports:')
        for x in a:
            print(x)
            try: 
                light = PySchott.Light(x.device)
                print('Schott light connected')
            except: 
                print('not a schott light')
                pass
        if light: 
            print('the show must go on !!')
            light.set_on()
            for i in range(10): 
                light.set_intensity((i+1)/10)
                sleep(.5)
            for i in range(10): 
                light.set_intensity((10-i)/10)
                sleep(.5)
            light.set_off()
            print('the show is over')
        else: 
            print('no compatible Schott light connected')
    else: 
        print('no COM port detected')

