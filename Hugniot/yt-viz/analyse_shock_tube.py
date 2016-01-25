#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
sys.path.append('./')
sys.path.append('../../../../')
import numpy as np
from figure_size import update_mpl_rc, get_figsize
update_mpl_rc({'backend': 'Agg'})
#update_mpl_rc({'backend': 'pgf'})
import eospac as eos
import matplotlib as mpl
from hedp.math.derivative import savgol
#print mpl.rcParams
#mpl.use('Agg')
pgf_with_pdflatex = {
    "pgf.texsystem": "pdflatex",
    "pgf.preamble": [
         r"\usepackage[utf8x]{inputenc}",
         r"\usepackage[T1]{fontenc}",
         r"\usepackage{cmbright}",
         r'\usepackage{tikz}',
         r'\usepackage{pgfplots}'
         ]
}
mpl.rcParams.update(pgf_with_pdflatex)

from scipy.constants import N_A
import matplotlib.pyplot as plt
import os.path, os
from scipy.constants import physical_constants
eV2K_cst = physical_constants['electron volt-kelvin relationship'][0]
import pandas as pd

import yt.mods


units = {'pres': 1e10, 'pele': 1e10, 'pion': 1e10, 'prad': 1e10,
         'eint': 1e10, 'eele': 1e10, 'eion': 1e10, 'erad': 1e10,
         'temp': eV2K_cst, 'tele': eV2K_cst, 'tion': eV2K_cst, 'trad': eV2K_cst,
         'dens': 1., 'velx': 1e5}
#units = {'pres': 1, 'pele': 1, 'pion': 1, 'prad': 1,
#         'eint': 1, 'eele': 1, 'eion': 1, 'erad': 1,
#         'temp': eV2K_cst, 'tele': eV2K_cst, 'tion': eV2K_cst, 'trad': eV2K_cst,
#         'dens': 1.}

def get_state(r, x0, dx=2e-4):
    states = []
    for sidx in range(2):
        x_vect  = r['x'] - (x0 + np.sign((sidx - 0.5))*dx)
        if x_vect.max()*x_vect.min()<0:
            # there is a solution
            solution = 1.0
        else:
            solution = np.nan
        ridx = np.argmin(np.abs(x_vect))
        states.append({key: solution*r[key][ridx]/units[key] for key in  units.keys()})
    return pd.DataFrame(states)


def eos_check_consistency(s, mat):
    print 'dens: {0:.3e}  tele: {1:.3e}  tion: {2:.3e}'.format(s['dens'], s['tele'], s['tion'])
    for Ylbl, Flbl, Ftab in [( 'tele', 'pele', 'Pe_DT'),
                             ( 'tion', 'pion', 'Piz_DT'),
                             ( 'tele', 'eele', 'Ue_DT'),
                             ( 'tion', 'pion', 'Uiz_DT'),
                             ]:
        Fval1 = s[Flbl]
        Fval2 =  mat.get_table(Ftab)(s['dens'], s[Ylbl]*eV2K_cst)
        print  '{0:6} | {1:.3e} {2:.3e} {3}'.format(Ftab, Fval1, float(Fval2), np.allclose(Fval1, Fval2, rtol=1e-3))

def get_shock_position(d):
    if (d['pres'].max() - d['pres'].min())/d['pres'].mean() < 0.2:
        return np.nan
    else:
        idx = np.nanargmin(savgol( d['x'], d['pres'], window_size=5, order=2, deriv=1))
        return d['x'][idx]

matf = eos.EosMaterial(83719, tables=['Piz_DT', 'Uiz_DT', 'Pe_DT', 'Ue_DT', 'Zfc_DT'],
                options={'.*': {'linear': True}},
                units='eospac', backend='eospac')

feosid = 83719
material = 'Al'

feos_opts ={'use_maxwell': True, 'use_softspheres': True,
                'maxwell_temp_arr': None, 'max_materials': 2,
                        'grid_subsample_default': 0}

#mat2 = eos.EosMaterial(3719, tables=['Piz_DT', 'Uiz_DT', 'Pe_DT', 'Ue_DT', 'Zfc_DT'],
#              options=feos_opts,
#                    units='cgs', backend='feos')



RUN_NAME = os.environ['SOURCE_TEMP']
EOS_TABLE = os.environ['EOS_TABLE']
FNAME = "frun_{0}/solidhugoniot_hdf5_chk_{1}"

res = {}


pf = yt.mods.load(FNAME.format(RUN_NAME, '0000')) 
r0 = pf.h.ortho_ray(0, (0, 0))
state0 =  get_state(r0, 1e-4, 0.5e-4)
res = {'temp_source': state0.tele[0]}

print 'Using eospac tables...'
for idx in range(2):
    eos_check_consistency(state0.ix[idx], matf)
print '='*80 +'\n'

storage = {}
ts = yt.mods.TimeSeriesData.from_filenames(FNAME.format(RUN_NAME, '*'), parallel = False)
for sto, pf in ts.piter(storage=storage):
    sl = pf.h.ortho_ray(0, (0, 0))
    t = pf.current_time*1e9
    x_s = get_shock_position(sl)
    vals = get_state(sl, x_s)
    state0 = vals.ix[0]
    state1 = vals.ix[1]
    state0['t'] = t
    state1['t'] = t
    state0['x'] = x_s
    state1['x'] = x_s
    sto.result = (state0, state1)#t, get_shock_position(sl), get_state(r0, 10e-4))
#t,x = np.array(storage.values()).T
state0 = []
state1 = []
for val0, val1 in storage.values():
    state0.append(val0)
    state1.append(val1)

df0 = pd.DataFrame(state0)
df1 = pd.DataFrame(state1)


fig = plt.figure(figsize=(20,4))
ax = [plt.subplot(1,4,idx+1) for idx in range(4)]

for dfi in [df0,df1]:
    dfi['u_s'] = savgol(np.array(dfi['t']), np.array(dfi['x']), window_size=5, order=2, deriv=1)*1e4
ax[0].plot(df0['t'],df0['u_s'], '--o')
ax[1].plot(df0['t'],df0['dens'], '--o')
ax[2].plot(df0['t'],df0['tele'], '--o')
ax[3].plot(df0['t'],df0['pres'], '--o')

idx_st = np.nanargmax(df0['x'])
for df_idx, df in enumerate([df0, df1]):
    for key in ['tele', 'tion', 'trad', 'pres', 'pele', 'pion', 'velx', 'dens']:
        res['{}_{}'.format(key, df_idx)] = np.array(df[key])[idx_st-4]
mask = slice(idx_st-17,idx_st-7)
res['u_s'] = np.median(np.array(df0['u_s'])[mask])
ax[0].plot(df0['t'][mask],df0['u_s'][mask], 'ro')

if not os.path.exists('yt-viz/out/{0}'.format(EOS_TABLE)):
    os.mkdir('yt-viz/out/{0}'.format(EOS_TABLE))
pd.DataFrame([res]).to_hdf('yt-viz/hugoniot_{0}.h5'.format(EOS_TABLE),
                'df', mode='a', format='table', append=True)


fig.savefig('yt-viz/out/{0}/hugoniot_{1}.png'.format(EOS_TABLE, RUN_NAME), bbox_inches='tight')




#fname_comp =  fname.format(eos['test'], 10) 
#if os.path.exists(fname_comp):
#
#    pf2 = yt.mods.load(fname_comp)
#    r1 = pf2.h.ortho_ray(0, (0, 0))
#    fig = plt.figure(figsize=get_figsize(wf=1, hf=0.6))
#    plt.subplots_adjust(wspace=0.3, hspace=0.4)
#    ax0 = plt.subplot(221)
#    ax1 = plt.subplot(222)
#    ax2 = plt.subplot(223)
#    dd = open_davis('rho')
#    ax0.plot(r0['x'], r0['dens']/rho_c, ':k', label='\scriptsize ininital condition')
#    ax0.plot(r1['x'], r1['dens']/rho_c, '-r', label='\scriptsize FLASH code', drawstyle='steps')
#    ax0.plot(dd[:,0], dd[:,1], '--b', label='\scriptsize Davis')
#    ax0.set_ylabel('\small Density')
#
#    dd = open_davis('pres')
#    ax1.plot(r0['x'], r0['pres']/pres_c, ':k')
#    ax1.plot(r1['x'], r1['pres']/pres_c, '-r', drawstyle='steps')
#    ax1.plot(dd[:,0], dd[:,1], '--b')
#    ax1.set_ylabel('\small Pressure')
#
#    #ax2.plot(r1['x'], np.abs(r1['velx'])/(r1['gamc']*r1['pres']/r1['dens'])**0.5, '-r')
#    ax2.plot(r0['x'], tab.q['G3_vdw'](r0['dens'], r0['temp']), ':k')
#    ax2.plot(r1['x'], tab.q['G3_vdw'](r1['dens'], r1['temp']), '-r', drawstyle='steps')
#    dd = open_davis('G')
#    ax2.plot(dd[:,0], dd[:,1], '--b')
#    ax2.set_ylabel('\small Fundamental derivative')
#
#    #check_consist(tab, r1)
#
#    ax0.legend(loc=4, bbox_to_anchor=(2.3, -0.7), ncol=2)
#    #ax0.grid()
#    #ax1.grid()
#    for axi in [ax0, ax1, ax2]:
#        axi.set_xlim(0,1)
#        axi.xaxis.set_ticks([0, 0.5, 1])
#        axi.set_xlabel('\small Position', labelpad=4)
#
#    #ax2.set_ylim(ymin=1e-3)
#
#    fig.savefig('yt-viz/out/viz_{0}.pdf'.format(eos['test']), bbox_inches='tight')
#else:
#    os.remove('yt-viz/out/viz_{0}.pdf'.format(eos['test']))
#
#    print 'Checkpoint file not found!'
