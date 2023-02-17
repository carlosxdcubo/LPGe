# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 23:49:23 2023

@author: crlos
"""
from matplotlib import pyplot as plt
import gen_utils as gu
#generate a plate
text="ABC123"
city="Medellin"
plate=gu.gen_placas(text,city)
plt.imshow(plate)
plt.show()    
