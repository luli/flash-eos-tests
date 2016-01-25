#!/usr/bin/python
# -*- coding: utf-8 -*-
import eospac as eos
from eospac.tools import *

import os.path, os
import numpy as np
from scipy.constants import physical_constants
eV2K_cst = physical_constants['electron volt-kelvin relationship'][0]

try:
    test_case = os.environ['EOS_TEST']
except:
    test_case = 'DG1'

def setup_eos():
    matid = '99999'
    tab = eos.EosMaterial(matid, ['Pt_DT', 'T_DPt', 'Ut_DT', 'St_DT', 'gamc_s'], spec=['t'],
              options={'delta': 0.0125, 'a': 5.537, 'b': 0.0305 , 'abar': 6.00530},
            units='cgs',
            backend='vdw')

    rho_c = tab.Pt_DT['rho_c']
    temp_c = tab.Pt_DT['temp_c']
    pres_c = tab.Pt_DT['Pt_c']
    #print rho_c, temp_c, pres_c

    eos_tests = {}
#st0 = {'rho': 1.01000,  'pres': 1.60770}
#st1 = {'rho': 0.59400,   'pres': 1.36136}
#eos_tests['WV1'] = [st0, st1]
    st0 = {'rho': 1.818,  'pres': 3.0, 'G':4.118}
    st1 = {'rho': 0.275, 'pres': 0.575, 'G': 0.703}
    eos_tests['DG1'] = [st0, st1]
    st0 = {'rho': 0.879,  'pres': 1.090, 'G': -0.031}
    st1 = {'rho': 0.562,  'pres': 0.885, 'G': -4.016}
    eos_tests['DG2'] = [st0, st1]
    st0 = {'rho': 0.879,  'pres': 1.090, 'G': -0.031}
    st1 = {'rho': 0.275,  'pres': 0.575, 'G': 0.703} 
    eos_tests['DG3'] = [st0, st1]


    for key in eos_tests:
        for stateid in range(2):
            eos_tests[key][stateid]['rho'] *= rho_c
            eos_tests[key][stateid]['pres'] *= pres_c
            crho = eos_tests[key][stateid]['rho']
            cpres = eos_tests[key][stateid]['pres']

            eos_tests[key][stateid]['temp'] = float(tab.T_DPt(crho, cpres))
            ctemp = eos_tests[key][stateid]['temp']
            eos_tests[key][stateid]['eint'] = float(tab.Ut_DT(crho, ctemp))
            eos_tests[key][stateid]['Gamma'] = float(tab.q['Gamma'](crho, ctemp))
            eos_tests[key][stateid]['Gamma_e'] = float(tab.q['game0'](crho, ctemp)) - 1
            eos_tests[key][stateid]['gamma'] = float(tab.q['gamc_s'](np.array([crho]), np.array([ctemp])))
            try:
                np.testing.assert_allclose(eos_tests[key][stateid]['G'], tab.q['G3_vdw'](crho, ctemp), rtol=2e-2,
                        err_msg=key+'_'+str(stateid))
            except:
                print(key+'_'+str(stateid), 'failed!')

    test_data = eos_tests[test_case]

    t_snapshot = {'DG1': 0.15, 'DG2': 0.45, 'DG3': 0.2}
    dt = {'DG1': 5e-4, 'DG2': 1.5e-3, 'DG3': 1e-3}

    treal = lambda tnorm:  tnorm*1.0*(rho_c/pres_c)**0.5 
    treal_t = treal(t_snapshot[test_case])
    treal_dt = treal(dt[test_case])
    return {'tab': tab, 'state': test_data, 'treal': treal_t, 'dt': treal_dt, 'test': test_case}
