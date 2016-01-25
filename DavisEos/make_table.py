#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os.path, os
import numpy as np
sys.path.append('./')
from setup_eos import setup_eos
import opacplot2 as opp
from scipy.constants import physical_constants
eV2K_cst = physical_constants['electron volt-kelvin relationship'][0]

eos = setup_eos()

state = eos['state']
tab = eos['tab']

abar = tab.Pt_DT['abar']
zbar = 3.3333 #tab.Pt_DT['znum']

rho_min = 0.2*state[1]['rho']
rho_max = 5*state[0]['rho']
temp_min = 0.2*state[1]['temp']
temp_max = 20*state[0]['temp']

rho = np.logspace(np.log10(rho_min), np.log10(rho_max),200)
temp = np.logspace(np.log10(temp_min), np.log10(temp_max), 328)

D, T = np.meshgrid(rho, temp, indices='ij')

pres = tab.Pt_DT(D,T)
eint = tab.Ut_DT(D,T)

print abar, zbar


numDens = opp.NA * rho / abar
for filename in ['simulations/DavisEos/eos-vdv-davis.cn4', 'setup/eos-vdv-davis.cn4']:
    opp.writeIonmixFile(filename, [zbar], [1.0],
                            numDens=numDens, temps=temp/eV2K_cst,
                            eion=0.5*eint.T,
                            eele=0.5*eint.T,
                            pion=0.5*pres.T,
                            pele=0.5*pres.T,
                            zbar=zbar*np.ones(pres.shape))


# rereading the output
ionmix = opp.OpacIonmix(filename, abar/opp.NA, twot=True, man=True, verbose=False)

