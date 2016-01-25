#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os.path, os
import numpy as np
sys.path.append('./')

temp_int = int(os.environ['SOURCE_TEMP'])
print 'Running with', temp_int
USE_IONMIX = False
if "imx" in os.environ['EOS_TABLE']:
    tmax = 12e-9*(5./temp_int)**0.3
    if temp_int<60:
        temp_int *= 2.
else:
    tmax = 6e-9*(5./temp_int)**0.3


p = {
        "ms_chamA": 26.98,
        "ms_chamZ": 13,
        "sim_rhoCham_l": 2.7,
        "sim_tempCham_l": 11640*temp_int,
        "sim_velxCham_l": 0,
        "sim_rhoCham_r": 2.7,
        "sim_tempCham_r": 298,
        "sim_velxCham_r": 0,
        'tmax': tmax,
        'sim_x0': 1e-4,
        'checkpointFileIntervalTime': 0,
        'checkpointFileIntervalTime': 2.5e-11,
        'eos_chamEosType' : "eos_tab",
        'eos_chamSubType' : "ionmix4",
        'eos_chamTableFile' : os.environ['EOS_TABLE']+".cn4",
        'plot_var': ['dens', 'tele', 'tion', 'eint', 'eele', 'eion',
                     'game', 'gamc', 'pres', 'pele', 'pion', 'temp', 'trad',
                     'velx']
        }


parameters = p
#for key in sorted(p):
#    print key, p[key]
