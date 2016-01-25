#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os.path, os
import numpy as np
sys.path.append('./')

try:
    from setup_eos import setup_eos


    eos = setup_eos()

    p = {
            "ms_chamA": eos['tab'].Pt_DT['abar'],
            "ms_chamZ": 3.333333333,
            "sim_rhoCham_l": eos['state'][0]['rho'],
            "sim_tempCham_l": eos['state'][0]['temp'],
            "sim_rhoCham_r": eos['state'][1]['rho'],
            
            "sim_tempCham_r":  eos['state'][1]['temp'],
            'tmax': eos['treal']*1.15,
            'checkpointFileIntervalTime': 0.1*eos['treal'],
            'dtmin': 0.001*eos['dt'],
            'dtmax': eos['dt'],
            'dtinit': 0.001*eos['dt'],
            # Rieman solver parameters
            'RiemannSolver': 'hllc', # Roe, HLL, HLLC, LLF, Marquina, hybrid
            'order' : 3,
            'slopeLimiter': "limited", # Slope limiters (minmod, mc, vanLeer, hybrid, limited)
            'cfl': 0.5,
            }

    print eos
except ImportError:
    print '='*80
    print ' '*10 + 'EOSPAC not avalable, using the hardcoded values for the EoS'
    print '='*80
    #if os.environ['EOS_TEST']:
    p = {'sim_rhoCham_l': 0.11931841967213115,
         'sim_tempCham_l': 679.0586399393677,
         'sim_tempCham_r': 642.5652697557431,
         'sim_rhoCham_r': 0.018048715846994537} 
    # DG1 
    if os.environ['EOS_TEST'] == 'DG1':
        p = {'sim_tempCham_r': 642.5652697557431, 'sim_rhoCham_l': 0.11931841967213115, 'sim_rhoCham_r': 0.018048715846994537, 'sim_tempCham_l': 679.0586399393677}
    elif os.environ['EOS_TEST'] == 'DG2':
        p = {'sim_tempCham_r': 642.873782473869, 'sim_rhoCham_l': 0.05769025901639344, 'sim_rhoCham_r': 0.03688501202185793, 'sim_tempCham_l': 664.9949220783527}
    elif os.environ['EOS_TEST'] == 'DG3':
        p = {'sim_tempCham_r': 642.5652697557431, 'sim_rhoCham_l': 0.05769025901639344, 'sim_rhoCham_r': 0.018048715846994537, 'sim_tempCham_l': 664.9949220783527}
    else:
        raise KeyError


    p.update({
         'dtmax': 8.627227904419322e-09,
         'dtinit': 8.627227904419322e-12,
         'ms_chamZ': 3.333333333,
         'tmax': 2.9763936270246655e-06,
         'checkpointFileIntervalTime': 2.588168371325796e-07,
         'RiemannSolver': 'hllc',
         'dtmin': 8.627227904419322e-12,
         'slopeLimiter': 'minmod',
         'ms_chamA': 6.0053, 
         'cfl': 0.5,
         'order': 3})
except:
    raise





parameters = p
for key in sorted(p):
    print key, p[key]

#print {key: p[key] for key in p if 'Cham' in key}
