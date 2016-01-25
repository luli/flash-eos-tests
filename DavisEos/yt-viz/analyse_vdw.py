#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import numpy as np
import matplotlib as mpl

from scipy.constants import N_A
import matplotlib.pyplot as plt
import os.path, os

import yt.mods

from setup_eos import setup_eos

def check_consist(tab, d):
    rho = d['dens']
    temp = d['tele']
    md = {}
    for key, attr in [('pion', 'Pt_DT'), ('eele', 'Ut_DT')]:
        md[key] = getattr(tab, attr)(rho, temp)
        pass_test = np.allclose(md[key], d[key])
        print(key, pass_test)
        if not pass_test:
            print np.abs((md[key] - d[key]))/d[key]

eos = setup_eos()
tab = eos['tab']

DAVIS_DATA = './data/DenseGas1DCases/'

open_davis = lambda field: np.loadtxt(os.path.join(DAVIS_DATA,'{0}_davis_{1}'.format(field, eos['test'])))

rho_c = tab.Pt_DT['rho_c']
temp_c = tab.Pt_DT['temp_c']
print 'temp_c', temp_c
print 'rho_c', rho_c
pres_c = tab.Pt_DT['Pt_c']


fname = "./frun_{0}_1D/daviseos_hdf5_chk_{1:04}"

pf = yt.mods.load(fname.format(eos['test'], 0)) 
r0 = pf.h.ortho_ray(0, (0, 0))
for sidx in range(2):
    print 'State', sidx
    print '-'*8
    ridx = np.argmin(np.abs(r0['x'] - (0.5 + np.sign((sidx - 0.5))*0.25)))

    for varf, vare in [('dens', 'rho'), ('tele', 'temp'), ('tion', 'temp'), ('pion', 'pres'), ('pele', 'pres'),  ('eele', 'eint') ]:
        v0, v1 = r0[varf][ridx], eos['state'][sidx][vare]
        if varf in ['eele', 'pele', 'pion', 'eion']:
           v0 *= 2
        print '{0} {1:.3e} {2:.3e} {3}'.format(varf, v0, v1, not np.allclose(v0, v1, rtol=1e-2) and 'Failed!' or ' ')


fname_comp =  fname.format(eos['test'], 10) 
if os.path.exists(fname_comp):

    FLASH_alpha = 0.6

    pf2 = yt.mods.load(fname_comp)
    r1 = pf2.h.ortho_ray(0, (0, 0))
    fig = plt.figure(figsize=get_figsize(wf=1.2, hf=0.6))
    plt.subplots_adjust(wspace=0.3, hspace=0.4)
    ax0 = plt.subplot(221)
    ax1 = plt.subplot(222)
    ax2 = plt.subplot(223)
    dd = open_davis('rho')
    ax0.plot(r0['x'], r0['dens']/rho_c, ':k', label='\scriptsize initial condition')
    ax0.plot(r1['x'], r1['dens']/rho_c, '-r', label='\scriptsize FLASH 4.2 code', drawstyle='steps', alpha=FLASH_alpha)
    ax0.plot(dd[:,0], dd[:,1], '--b', label='\scriptsize Davis~(1985)')
    ax0.set_ylabel(r'\small Density~($\rho^*$)')

    dd = open_davis('pres')
    ax1.plot(r0['x'], r0['pres']/pres_c, ':k')
    ax1.plot(r1['x'], r1['pres']/pres_c, '-r', drawstyle='steps', alpha=FLASH_alpha)
    ax1.plot(dd[:,0], dd[:,1], '--b')
    ax1.set_ylabel(r'\small Pressure~($P^*$)')

    #ax2.plot(r1['x'], np.abs(r1['velx'])/(r1['gamc']*r1['pres']/r1['dens'])**0.5, '-r')
    ax2.plot(r0['x'], tab.q['G3_vdw'](r0['dens'], r0['tele']), ':k')
    ax2.plot(r1['x'], tab.q['G3_vdw'](r1['dens'], r1['tele']), '-r', drawstyle='steps', alpha=FLASH_alpha)

    dd = open_davis('G')
    #G3_dd  = tab.q['G3_vdw'](dd[:,0]*, dd[:,1])
    ax2.plot(dd[:,0], dd[:,1], '--b')
    ax2.set_ylabel(r'\small Fundamental derivative~($\mathcal{G}$)')

    #check_consist(tab, r1)

    ax0.legend(loc=4, bbox_to_anchor=(2.15, -0.63), ncol=2)
    #ax0.grid()
    #ax1.grid()
    for axi in [ax0, ax1, ax2]:
        axi.set_xlim(0,1)
        axi.xaxis.set_ticks([0, 0.5, 1])
        axi.set_xlabel('\small Position', labelpad=4)

    #ax2.set_ylim(ymin=1e-3)

    fig.savefig('yt-viz/out/viz_{0}.pdf'.format(eos['test']), bbox_inches='tight')
else:
    fname = 'yt-viz/out/viz_{0}.pdf'.format(eos['test'])
    if os.path.exists(fname):
        os.remove(fname)


    print 'Checkpoint file not found!'


