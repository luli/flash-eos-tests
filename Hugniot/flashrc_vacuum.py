#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os.path, os
import numpy as np
sys.path.append('./')

tmax = 20e-9


p = {
        "ms_chamA": 26.98,
        "ms_chamZ": 13,
        "sim_rhoCham_l": 1e-3,
        "sim_tempCham_l": 298,
        "sim_velxCham_l": 0,
        "sim_rhoCham_r": 2.7,
        "sim_tempCham_r": 298,
        "sim_velxCham_r": 0,
        'tmax': tmax,
        'sim_x0': 50e-4,
        'checkpointFileIntervalTime': 0,
        'checkpointFileIntervalTime': 1e-10,
        'eos_chamEosType' : "eos_tab",
        'eos_chamSubType' : "ionmix4",
        'eos_chamTableFile' : os.environ['EOS_TABLE']+".cn4",
        'plot_var': ['dens', 'tele', 'tion', 'eint', 'eele', 'eion',
                     'game', 'gamc', 'pres', 'pele', 'pion', 'temp', 'trad',
                     'velx'],
        # Hydro options
        "cfl": 0.4,
        "order":  2,
        "RiemannSolver": "hllc",
        "slopeLimiter": 'minmod',
        }


parameters = p
#for key in sorted(p):
#    print key, p[key]
